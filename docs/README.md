# Web Scraper Reclame Aqui

Este projeto é um web scraper para coletar reclamações **não respondidas** de empresas no site Reclame Aqui, utilizando a biblioteca `cloudscraper`. As informações são armazenadas em cache e disponibilizadas por uma API Flask.

## Funcionalidades

- **Scraping de Reclamações:** Coleta título, descrição, status e URL das reclamações usando a classe `ReclameAquiScraper`.
- **Cache de Comentários:** Reclamações são salvas em `comments_cache` para acesso rápido via API.
- **API Flask:** Endpoint `/comments/<empresa>` retorna reclamações de uma empresa específica. Requer autenticação via cabeçalho `x-api-key`.
- **Execução em Segundo Plano:** Scraping inicial e atualizações do cache a cada 20 minutos usando threads.

## Tecnologias

- **Flask:** API REST
- **cloudscraper:** Acesso a páginas protegidas por anti-bot
- **BeautifulSoup:** Extração de dados do HTML
- **schedule:** Agendamento de tarefas
- **threading:** Execução paralela

## Sobre as Bibliotecas

- **cloudscraper:** Simula um navegador para acessar páginas protegidas por Cloudflare.
- **BeautifulSoup:** Faz parsing do HTML para extrair dados relevantes.

## Estrutura do Projeto

```text
webScrapper/
├── main.py
├── requirements.txt
├── src/
│   ├── route/
│   │   └── routes.py
│   ├── scrapers/
│   │   └── scraper.py
│   └── service/
│       └── services.py
└── test/
  └── teste.py
```

## Como Usar

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute o servidor:**
   ```bash
   python main.py
   ```

3. **Acesse a API:**
   ```bash
   curl -H "x-api-key: 123456" http://127.0.0.1:5000/comments/vivo
   ```

4. **Teste o scraper:**
   ```bash
   python test/teste.py
   ```

## Aviso Legal

Este projeto é apenas para fins educacionais. Scraping pode violar termos de uso de sites. Verifique sempre as políticas do site antes de coletar dados.
