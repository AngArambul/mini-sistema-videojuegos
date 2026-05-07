from flask import Flask, render_template, redirect, url_for, flash, request, jsonify, abort
from flask_login import LoginManager, login_required, current_user
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import HTTPException, BadRequest, MethodNotAllowed
import logging
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from database import db
from models import User

app = Flask(__name__)

# --- CONFIGURACIÓN DE LOGS Y SENTRY ---
sentry_sdk.init(dsn='', integrations=[FlaskIntegration()])

# Configuramos el archivo local para guardar errores críticos
file_handler = logging.FileHandler('errors.log')
file_handler.setLevel(logging.ERROR)
app.logger.addHandler(file_handler)

# --- CONFIGURACIONES BASE ---
app.config['SECRET_KEY'] = 'clave_super_secreta'
app.config['SESSION_COOKIE_SECURE'] = True
app.config['REMEMBER_COOKIE_HTTPONLY'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:hola123@localhost/videojuegos_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializamos la BD con la app
db.init_app(app)

# --- CONFIGURACIÓN DE FLASK-LOGIN ---
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.session_protection = 'strong'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- REGISTRO DEL BLUEPRINT DE AUTENTICACIÓN ---
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')

# --- REGISTRO DEL BLUEPRINT DE LA API ---
from api.routes import api_bp
app.register_blueprint(api_bp, url_prefix='/api')

# Importamos controladores
from controllers import obtener_juegos, insertar_juego, eliminar_juego
from forms import JuegoForm

# --- RUTAS DE LA APP PRINCIPAL ---
@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")

@app.route("/")
def index():
    juegos = obtener_juegos()
    form = JuegoForm()
    return render_template("index.html", juegos=juegos, form=form)

@app.route("/agregar", methods=["POST"])
@login_required
def agregar():
    form = JuegoForm()
    if form.validate_on_submit():
        try:
            insertar_juego(form.titulo.data, form.genero.data, form.plataforma.data)
            flash('Juego agregado correctamente')
        except IntegrityError:
            db.session.rollback()
            flash('Error: Ese videojuego ya está registrado en el sistema.')
            
    return redirect(url_for('index'))

@app.route("/eliminar/<int:id>")
@login_required
def eliminar(id):
    eliminar_juego(id)
    flash('Juego eliminado')
    return redirect(url_for('index'))

# --- MANEJADORES DE ERRORES WEB ---
@app.errorhandler(BadRequest)
def handle_400(e):
    return render_template('400.html'), 400

@app.errorhandler(404)
def handle_404(e):
    return render_template('404.html'), 404

@app.errorhandler(MethodNotAllowed)
def handle_405(e):
    return render_template('405.html'), 405

@app.errorhandler(500)
def handle_500(e):
    return render_template('500.html'), 500

# --- MANEJADOR DE ERRORES PARA LA API (Formato JSON) ---
@app.errorhandler(HTTPException)
def handle_api_error(e):
    if request.path.startswith('/api/'):
        response = e.get_response()
        response.data = jsonify(code=e.code, name=e.name, description=e.description).data
        response.content_type = 'application/json'
        return response
    return e

# --- RUTAS DE PRUEBA PARA FORZAR ERRORES ---
@app.route("/prueba-400")
def prueba_400():
    abort(400) # Forzamos un error de "Petición Incorrecta"

@app.route("/prueba-500")
def prueba_500():
    # Forzamos un error matemático (división entre cero) para probar si el archivo errors.log lo guarda
    resultado = 1 / 0
    return str(resultado)

if __name__ == "__main__":
    # Esto asegura que SQLAlchemy cree la tabla "usuarios" en MySQL antes de arrancar
    with app.app_context():
        db.create_all()
    app.run(debug=False
            )