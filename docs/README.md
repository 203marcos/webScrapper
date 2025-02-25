# RPA Reclame Aqui

Este projeto implementa um Robotic Process Automation (RPA) para extrair informações do site Reclame Aqui. O objetivo é coletar dados das melhores e piores empresas do setor de energia elétrica e gerar um arquivo Excel com essas informações.

## Funcionalidades

- *Automação de Navegação:* Utiliza Selenium para navegar pelo site e evitar mecanismos de bloqueio (ex.: Cloudflare).
- *Extração de Dados:* Busca e seleciona a categoria "Energia elétrica", extraindo links das melhores e piores empresas.
- *Parsing de Conteúdo:* Utiliza BeautifulSoup para analisar o HTML e coletar métricas como:
  - Nota da Empresa
  - Reclamações Respondidas
  - Nota do Consumidor
  - Voltariam a fazer negócio
  - Índice de Solução
- *Geração de Relatório:* Cria um arquivo Excel com planilhas separadas para as melhores e piores empresas.

## Estrutura do Projeto

RPA_RECLAMEAQUI/
├─ .venv/
├─ docs/
│  └─ README.md                 # Este arquivo
├─ src/
│  ├─ scrapers/
│  │  ├─ parser.py              # Lógica de parsing do HTML
│  │  └─ scraper.py             # Lógica de navegação e extração
│  └─ chromedriver.exe          # Driver do Chrome 
├─ tests/
│  └─ pytest.py                 # Testes automatizados 
├─ .gitignore                  # Arquivo para ignorar arquivos/pastas indesejadas no Git
├─ config.py                   # Configuração do WebDriver
├─ main.py                     # Script principal que orquestra a execução
└─ requirements.txt            # Lista de dependências do projeto


## Pré-requisitos

- *Python 3.x* instalado.
- *Google Chrome* instalado.
- *ChromeDriver:* Certifique-se de que o ChromeDriver esteja instalado e seja compatível com a versão do Chrome em seu sistema. Você pode deixá-lo na pasta src/ ou configurá-lo no PATH.

## Instalação

1. *Clone o repositório:*
   ```bash
   git clone <URL_DO_REPOSITÓRIO>
   cd RPA_RECLAMEAQUI

	2.	Crie e ative um ambiente virtual (opcional, mas recomendado):

    •   No Windows:

python -m venv .venv
.venv\Scripts\activate

	•	No Linux/Mac:

python3 -m venv .venv
source .venv/bin/activate



	3.	Instale as dependências:

pip install -r requirements.txt



Uso

Para executar o projeto, rode o script principal:

python main.py

O script abrirá o navegador, realizará a extração dos dados e gerará o arquivo resultados.xlsx na raiz do projeto.

Considerações
	•	Manutenção: Se o layout ou as classes CSS do site Reclame Aqui mudarem, pode ser necessário atualizar os seletores no código.
	
