from src.route.routes import app
from src.service.services import start_background_jobs

if __name__ == "__main__":
    # Inicia os trabalhos em segundo plano
    start_background_jobs()
    # Inicia o Flask (servidor web) na porta 3038 e aceita conexões externas
    app.run(host="0.0.0.0", port=3038, debug=True, threaded=True)