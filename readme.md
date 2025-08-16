# 🤖 AI Data Agent: Análise de Dados com Linguagem Natural

Este projeto é uma solução para o Desafio Técnico de Estágio em Automação com IA, que consiste em um protótipo funcional que utiliza um fluxo de agentes de IA para interpretar comandos em linguagem natural, consultar um banco de dados SQLite e gerar insights valiosos.

---

## 🎯 Objetivo do Projeto

O objetivo é criar uma aplicação web simples com Streamlit onde um usuário pode fazer perguntas em linguagem natural sobre uma base de dados fornecida. A aplicação deve orquestrar agentes de IA para traduzir a pergunta em uma consulta SQL, executá-la e apresentar a resposta de forma clara e amigável.

## ✨ Arquitetura e Fluxo de Agentes

O projeto implementa uma orquestração simples de agentes, onde cada um tem uma responsabilidade clara, garantindo um fluxo de trabalho modular e eficiente.

**Orquestração:**
`Pergunta do Usuário` -> **Agente 1** -> `Consulta SQL` -> **Agente 2** -> `Dados (DataFrame)` -> **Agente 3** -> `Resposta Formatada`

-   **Agente 1: Intérprete de Linguagem Natural (Text-to-SQL)**
    -   **Responsabilidade:** Recebe a solicitação do usuário e o *schema* do banco de dados. Sua única função é traduzir essa pergunta em uma consulta SQL válida para o SQLite.
    -   **Tecnologia:** Utiliza o modelo `llama3-70b-8192` através da API da Groq, com um prompt rigoroso para garantir a precisão do SQL gerado.

-   **Agente 2: Consultor de Dados (Executor SQL)**
    -   **Responsabilidade:** Uma função Python que recebe a consulta SQL gerada, conecta-se ao banco de dados `clientes_completo.db`, executa a query e retorna os resultados em um DataFrame do Pandas.
    -   **Tecnologia:** `sqlite3` e `pandas`.

-   **Agente 3: Formatador da Resposta (Analista de Dados)**
    -   **Responsabilidade:** Recebe os dados do Agente 2 e a pergunta original. Sua função é analisar os dados e gerar um resumo textual claro e objetivo.
    -   **Tecnologia:** Utiliza novamente o `llama3-70b-8192` para interpretar os dados e comunicar os insights.

## 🛠️ Tecnologias Utilizadas

-   **Linguagem:** Python
-   **Inteligência Artificial:** Groq API com o modelo Llama 3 70B
-   **Frontend:** Streamlit
-   **Banco de Dados:** SQLite
-   **Manipulação de Dados:** Pandas
-   **Visualização:** Matplotlib

## ⚙️ Instruções de Execução

**Pré-requisitos:**
-   Python 3.8+
-   Uma chave de API da Groq.

**Passos:**

1.  **Clone o repositório e navegue até a pasta do projeto.**

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # Windows: .\\venv\\Scripts\\activate | macOS/Linux: source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure suas credenciais:**
    -   Crie um arquivo chamado `.env` na raiz do projeto.
    -   Adicione sua chave da API da Groq:
        ```
        GROQ_API_KEY="SUA_CHAVE_API_AQUI"
        ```

5.  **Posicione o Banco de Dados:**
    -   Certifique-se de que o arquivo `clientes_completo.db` está na mesma pasta que o `app.py`.

6.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📝 Exemplos de Consultas Testadas

-   `Liste os 5 estados com maior número de clientes que compraram via app em maio.`
-   `Quantos clientes interagiram com campanhas de WhatsApp em 2024?`
-   `Qual o valor total de vendas por canal de compra, ordenado do maior para o menor?`
-   `Qual o número de reclamações não resolvidas por canal? Gere um gráfico de pizza.`
-   `Liste os 10 clientes que mais gastaram no total.`

**Desenvolvido por Gustavo Rabutske**