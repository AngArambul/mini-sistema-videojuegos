from app import app, db

with app.app_context():
    db.create_all()
    print("Las tablas se crearon con éxito en MySQL")