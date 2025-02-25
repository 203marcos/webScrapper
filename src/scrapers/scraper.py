import time
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from src.scrapers.parser import ReclameAquiParser


class ReclameAquiScraper:
    def __init__(self, driver):
        self.driver = driver
        self.base_url = "https://www.reclameaqui.com.br"
        self.parser = ReclameAquiParser()
        # Agora, as listas armazenam dicionários com 'url' e 'nota'
        self.best_companies_links = []
        self.worst_companies_links = []

    def open_reclame_aqui_home(self):
        self.driver.execute_script(
            "window.open('https://www.reclameaqui.com.br/', '_blank')")
        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.execute_script("window.scrollTo(0, 500);")

    def search_for_electricity(self):
        input_element = self.driver.find_element(
            By.XPATH, '//*[@id="homeRankings"]/div/div/div[2]/astro-island/div/div[1]/div/div[1]/input')
        ActionChains(self.driver).move_to_element(
            input_element).pause(1).click().perform()
        input_element.clear()
        input_element.send_keys("Energia elétrica")
        time.sleep(5)
        button = self.driver.find_element(
            By.XPATH, "//button[@title='Energia elétrica']")
        ActionChains(self.driver).move_to_element(
            button).pause(1).click().perform()
        time.sleep(5)

    def get_best_companies(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listas = soup.find_all("div", class_="list svelte-lzrvt6")
        if listas:
            melhores = listas[0].find_all(
                "a", {"data-testid": "listing-ranking"}, href=True)
            self.best_companies_links = []
            for melhor in melhores[:3]:
                url = melhor["href"]
                rating_span = melhor.find(
                    "span", class_="text-sm font-bold text-black")
                rating = rating_span.get_text(
                    strip=True) if rating_span else "N/D"
                self.best_companies_links.append({"url": url, "nota": rating})

    def click_worst_companies_tab(self):
        link_piores = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id="homeRankings"]/div/div/div[2]/astro-island/div/div[2]/ul/li[2]')
            )
        )
        link_piores.click()
        time.sleep(5)

    def get_worst_companies(self):
        soup = BeautifulSoup(self.driver.page_source, "html.parser")
        listas = soup.find_all("div", class_="list svelte-lzrvt6")
        if listas:
            piores = listas[0].find_all(
                "a", {"data-testid": "listing-ranking"}, href=True)
            self.worst_companies_links = []
            for pior in piores[:3]:
                url = pior["href"]
                rating_span = pior.find(
                    "span", class_="text-sm font-bold text-black")
                rating = rating_span.get_text(
                    strip=True) if rating_span else "N/D"
                self.worst_companies_links.append({"url": url, "nota": rating})

    def extract_company_data(self, url):
        # Garante a URL completa
        full_url = url if url.startswith("http") else self.base_url + url
        self.driver.get(full_url)
        time.sleep(5)
        html = self.driver.page_source
        data = self.parser.extract_company_data(html)
        data["URL"] = full_url  # Adiciona a URL aos dados retornados
        return data
