**Centro Universitario de los Valles (CUValles)**
**Licenciatura en Tecnologías de la Información**
**Alumno:** Angel Gabriel Ortega Arambul
**Proyecto:** Sistema de Gestión de Videojuegos - Pruebas Unitarias
---

## 1. Cobertura de Pruebas
Se implementaron 4 casos de prueba críticos divididos en tres áreas:

* **Modelos (`test_models.py`):** Validación de la creación de registros en la base de datos (SQLAlchemy) con los campos `titulo`, `genero` y `plataforma`.
* **Rutas Web (`test_routes.py`):** * Verificación de acceso a la página de inicio (Status 200).
    * Verificación de protección de rutas (Redirect 302 al intentar entrar a `/profile` sin login).
* **API REST (`test_api.py`):** Validación del endpoint `/api/juegos`, asegurando que retorne una lista en formato JSON y código de éxito 200.

## 2. Retos Encontrados y Soluciones

### Reto A: Aislamiento de la Base de Datos
**Problema:** Al correr las pruebas, se borraban o duplicaban datos en la base de datos real de MySQL (XAMPP).
**Solución:** Se implementó `sqlite:///:memory:` dentro del método `setUp`. Esto crea una base de datos temporal en la RAM que se destruye al finalizar los tests, garantizando pruebas limpias y rápidas.

### Reto B: Contexto de la Aplicación
**Problema:** Error `RuntimeError: Working outside of application context`.
**Solución:** Se utilizó `app.app_context().push()` para asegurar que SQLAlchemy tuviera acceso a la configuración de la app durante la ejecución de las pruebas unitarias.

### Reto C: Validación de Seguridad
**Problema:** Cómo probar que una ruta está protegida sin tener que simular un navegador.
**Solución:** Se utilizó el `test_client()` de Flask para capturar los encabezados de respuesta y validar que el servidor enviara una redirección (302) hacia la ruta de login. 
# Prueba de GitHub Actions