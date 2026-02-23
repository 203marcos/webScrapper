import time
import random
import cloudscraper
from bs4 import BeautifulSoup

class ReclameAquiScraper:
    def __init__(self, driver, base_url):
        self.driver = driver
        self.base_url = base_url
        self.comments = []
        self.commentsFilter = []

    def get_comments_cloudscraper(self):
        # print(f"[Scraper] Iniciando scraping: {self.base_url}")
        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
            },
        )
        response = scraper.get(self.base_url)
        # print(f"[Scraper] Status inicial: {response.status_code}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            reclamacoes = soup.find_all("a", href=True)
            # print(f"[Scraper] Links encontrados na página inicial: {len(reclamacoes)}")
            comments = []
            base_url = "https://www.reclameaqui.com.br"
            next_page_url = self.base_url

            while next_page_url:
                # print(f"[Scraper] Scraping página: {next_page_url}")
                response = scraper.get(next_page_url)
                # print(f"[Scraper] Status página: {response.status_code}")
                if response.status_code != 200:
                    # print(f"[Scraper] Falha ao acessar página: {next_page_url}")
                    break
                soup = BeautifulSoup(response.text, "html.parser")
                reclamacoes = soup.find_all("a", href=True)
                # print(f"[Scraper] Links encontrados: {len(reclamacoes)}")

                for link_tag in reclamacoes:
                    h4 = link_tag.find("h4")
                    if not h4:
                        continue
                    href = link_tag["href"]
                    if not href.startswith("http"):
                        href = base_url + href

                    # print(f"[Scraper] Visitando reclamação: {href}")
                    rec_response = scraper.get(href)
                    # print(f"[Scraper] Status reclamação: {rec_response.status_code}")
                    if rec_response.status_code != 200:
                        # print(f"[Scraper] Falha ao acessar reclamação: {href}")
                        continue
                    rec_soup = BeautifulSoup(rec_response.text, "html.parser")

                    titulo_tag = rec_soup.find(attrs={"data-testid": "complaint-title"}) or rec_soup.find("h1")
                    titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""
                    # print(f"[Scraper] Título: {titulo}")

                    descricao_tag = rec_soup.find(attrs={"data-testid": "complaint-description"})
                    if not descricao_tag:
                        for p in rec_soup.find_all("p"):
                            texto = p.get_text(strip=True)
                            if texto and not texto.startswith("Essa reclamação foi publicada há mais de"):
                                descricao_tag = p
                                break
                    descricao = descricao_tag.get_text(strip=True) if descricao_tag else ""
                    # print(f"[Scraper] Descrição: {descricao[:60]}...")

                    status = ""
                    status_div = rec_soup.find(attrs={"data-testid": "complaint-status"})
                    if status_div:
                        status_span = status_div.find("span")
                        if status_span:
                            status = status_span.get_text(strip=True)
                    if not status:
                        for span in rec_soup.find_all("span"):
                            texto = span.get_text(strip=True)
                            if texto in ["Não respondida", "Respondida", "Não resolvido", "Resolvido"]:
                                status = texto
                                break
                    # print(f"[Scraper] Status: {status}")

                    if titulo and descricao:
                        comments.append({
                            "titulo": titulo,
                            "descricao": descricao,
                            "url": href
                        })
                        # print(f"[Scraper] Comentário adicionado: {titulo}")

                    time.sleep(random.uniform(1, 2))

                next_link = soup.find("a", text="Próxima")
                if next_link and next_link["href"]:
                    next_page_url = base_url + next_link["href"]
                    # print(f"[Scraper] Próxima página: {next_page_url}")
                else:
                    next_page_url = None
                    # print(f"[Scraper] Sem próxima página.")
            self.comments = comments
            self.commentsFilter = comments
            # print(f"[Scraper] Total comentários coletados: {len(self.comments)}")
            # print(f"[Scraper] Total comentários não respondidos: {len(self.commentsFilter)}")
        else:
            # print(f"[Scraper] Falha ao acessar URL inicial: {self.base_url}")
            self.comments = []
            self.commentsFilter = []



