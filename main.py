from src.route.routes import app
from src.service.services import start_background_jobs

if __name__ == "__main__":
    # Inicia os trabalhos em segundo plano
    start_background_jobs()
    # Inicia o Flask (servidor web)
    app.run(debug=True, threaded=True)