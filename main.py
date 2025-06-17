from src.scrapers.scraper import ReclameAquiScraper
import schedule
import time
from flask import Flask, Response, request, jsonify
import threading
import json


app = Flask(__name__)
API_KEY = "123456"

comments_cache = {
    "vivo": [],
    "claro": [],
    "tim": []
}

URLS = {
    "vivo": "https://www.reclameaqui.com.br/empresa/vivo-celular-fixo-internet-tv/lista-reclamacoes/?pagina=1&status=NOT_ANSWERED",
    "claro": "https://www.reclameaqui.com.br/empresa/claro/lista-reclamacoes/?status=NOT_ANSWERED",
    "tim": "https://www.reclameaqui.com.br/empresa/tim-celular/lista-reclamacoes/?status=NOT_ANSWERED"
}

def scrape_and_update_cache(empresa):
    print(f"Iniciando scraping para: {empresa}")
    scraper = ReclameAquiScraper(None, URLS[empresa])
    scraper.get_comments_cloudscraper()
    print(f"Total de comentários coletados para {empresa}: {len(scraper.commentsFilter)}")
    comments_cache[empresa] = scraper.commentsFilter

def main():
    print("Iniciando scraping inicial...")
    for empresa in URLS:
        scrape_and_update_cache(empresa)
    print("Scraping inicial concluído.")

@app.route("/comments/<empresa>", methods=["GET"])
def get_comments_empresa(empresa):
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"detail": "Unauthorized"}), 401
    if empresa not in comments_cache:
        return jsonify({"detail": "Empresa não encontrada"}), 404
    # Serializa o JSON com ensure_ascii=False
    return Response(
        json.dumps({"comments": comments_cache[empresa]}, ensure_ascii=False),
        mimetype="application/json"
    )

def schedule_job():
    schedule.every(20).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    # Executa o scraping inicial em uma thread separada
    threading.Thread(target=main, daemon=True).start()
    # Inicia o agendamento em uma thread separada
    threading.Thread(target=schedule_job, daemon=True).start()
    # Inicia o Flask (servidor web)
    app.run(debug=True, threaded=True)