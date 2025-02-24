import pandas as pd
from config import get_driver
from src.scrapers.scraper import ReclameAquiScraper


def main():
    # Inicia o WebDriver
    driver = get_driver()

    # Instancia o Scraper
    scraper = ReclameAquiScraper(driver)

    # Abre a aba principal do Reclame Aqui
    scraper.open_reclame_aqui_home()

    # Faz a busca por Energia Elétrica
    scraper.search_for_electricity()

    # Extrai os links e as notas das melhores empresas
    scraper.get_best_companies()

    # Clica na aba de piores empresas e extrai seus links e notas
    scraper.click_worst_companies_tab()
    scraper.get_worst_companies()

    print("Melhores empresas:", scraper.best_companies_links)
    print("Piores empresas:", scraper.worst_companies_links)

    # Extrai os dados para cada empresa e sobrescreve a nota com a extraída na listagem
    resultado_melhores = []
    for company in scraper.best_companies_links:
        dados = scraper.extract_company_data(company["url"])
        dados["Nota da Empresa"] = company["nota"]
        resultado_melhores.append(dados)

    resultado_piores = []
    for company in scraper.worst_companies_links:
        dados = scraper.extract_company_data(company["url"])
        dados["Nota da Empresa"] = company["nota"]
        resultado_piores.append(dados)

    # Exporta para Excel em planilhas separadas
    with pd.ExcelWriter("resultados.xlsx") as writer:
        df_melhores = pd.DataFrame(resultado_melhores)
        df_melhores.to_excel(
            writer, sheet_name="Melhores Empresas", index=False)

        df_piores = pd.DataFrame(resultado_piores)
        df_piores.to_excel(writer, sheet_name="Piores Empresas", index=False)

    print("Dados salvos em resultados.xlsx")

    # Encerra o WebDriver
    scraper.close_driver()


if __name__ == "__main__":
    main()
