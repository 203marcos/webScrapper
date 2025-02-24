from bs4 import BeautifulSoup


class ReclameAquiParser:
    # Classe responsável por analisar o HTML de uma página de empresa no Reclame Aqui e extrair os dados
    def extract_company_data(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # Variáveis dos percentuais
        overall_rating = "N/D"
        reclamacoes_respondidas = "N/D"
        nota_consumidor = "N/D"
        voltariam_negocio = "N/D"
        indice_solucao = "N/D"

        performance_div = soup.find("div", class_="go267425901")
        if performance_div:
            metrics = performance_div.find_all("div", class_="go4263471347")
            for metric in metrics:
                text = metric.get_text(separator=" ", strip=True)
                if "Respondeu" in text:
                    strong_tag = metric.find("strong")
                    reclamacoes_respondidas = strong_tag.get_text(
                        strip=True) if strong_tag else "N/D"
                elif "nota média dos consumidores" in text:
                    strong_tags = metric.find_all("strong")
                    if len(strong_tags) > 1:
                        nota_consumidor = strong_tags[1].get_text(strip=True)
                    elif strong_tags:
                        nota_consumidor = strong_tags[0].get_text(strip=True)
                elif "voltariam a fazer negócio" in text:
                    strong_tag = metric.find("strong")
                    voltariam_negocio = strong_tag.get_text(
                        strip=True) if strong_tag else "N/D"
                elif "resolveu" in text.lower():
                    strong_tag = metric.find("strong")
                    indice_solucao = strong_tag.get_text(
                        strip=True) if strong_tag else "N/D"

        return {
            "Nota da Empresa": overall_rating,
            "Reclamações Respondidas": reclamacoes_respondidas,
            "Nota do Consumidor": nota_consumidor,
            "Voltariam a fazer negócio": voltariam_negocio,
            "Índice de Solução": indice_solucao
        }
