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
        scraper = cloudscraper.create_scraper(
            browser={
                "browser": "chrome",
                "platform": "windows",
            },
        )
        response = scraper.get(self.base_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            # Busca todos os <a> que possuem um <h4> dentro (link da reclamação)
            reclamacoes = soup.find_all("a", href=True)
            comments = []
            base_url = "https://www.reclameaqui.com.br"
            next_page_url = self.base_url

            while next_page_url:
                response = scraper.get(next_page_url)
                if response.status_code != 200:
                    break
                soup = BeautifulSoup(response.text, "html.parser")
                reclamacoes = soup.find_all("a", href=True)

                for link_tag in reclamacoes:
                    h4 = link_tag.find("h4")
                    
                    if not h4:
                        continue
                    href = link_tag["href"]
                    if not href.startswith("http"):
                        href = base_url + href

                    # Visita a página individual da reclamação
                    rec_response = scraper.get(href)
                    if rec_response.status_code != 200:
                        continue
                    rec_soup = BeautifulSoup(rec_response.text, "html.parser")

                    # Título
                    titulo_tag = rec_soup.find(attrs={"data-testid": "complaint-title"}) or rec_soup.find("h1")
                    titulo = titulo_tag.get_text(strip=True) if titulo_tag else ""

                    # Descrição
                    descricao_tag = rec_soup.find(attrs={"data-testid": "complaint-description"})
                    if not descricao_tag:
                        # fallback: primeiro <p> relevante
                        for p in rec_soup.find_all("p"):
                            texto = p.get_text(strip=True)
                            if texto and not texto.startswith("Essa reclamação foi publicada há mais de"):
                                descricao_tag = p
                                break
                    descricao = descricao_tag.get_text(strip=True) if descricao_tag else ""

                    # Status
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

                    if titulo and descricao and status:
                        comments.append({
                            "titulo": titulo,
                            "descricao": descricao,
                            "status": status,
                            "url": href
                        })

                    time.sleep(random.uniform(1, 2))

                # Procura o link da próxima página
                next_link = soup.find("a", text="Próxima")
                if next_link and next_link["href"]:
                    next_page_url = base_url + next_link["href"]
                else:
                    next_page_url = None
            
            self.comments = comments
            self.commentsFilter = [
                c for c in comments if c["status"] == "Não respondida"]
        else:
            self.comments = []
            self.commentsFilter = []



