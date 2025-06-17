from bs4 import BeautifulSoup
import cloudscraper

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
    },
)

url = "https://www.reclameaqui.com.br/empresa/newland-toyota/lista-reclamacoes/?status=NOT_ANSWERED"

response = scraper.get(url)
print(f"The status code is {response.status_code}")

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    titulos = [h4.text for h4 in soup.find_all("h4")]
    print("Títulos encontrados:", titulos)
else:
    print("Não foi possível acessar a página.")