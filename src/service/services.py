from src.scrapers.scraper import ReclameAquiScraper
import schedule
import time
import threading

comments_cache = {
    "vivo": [],
    "claro": [],
    "tim": []
}

URLS = {
    # Aqui seria o ideal passar a URL de cada empresa, já na lista de não respondidas
    # para evitar o scraping de todas as reclamações, mas como o Reclame Aqui...
    # mas caso queira no back end, também faz a filtragem por não respondidas.
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

def schedule_job():
    schedule.every(20).minutes.do(main)
    while True:
        schedule.run_pending()
        time.sleep(1)

def start_background_jobs():
    threading.Thread(target=main, daemon=True).start()
    threading.Thread(target=schedule_job, daemon=True).start()