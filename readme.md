# 🤖 AI Data Agent: Análise de dados com LangChain

Este projeto é a minha solução para o **Desafio Técnico**. A ideia foi criar uma ferramenta inteligente e intuitiva que transforma perguntas do dia a dia em análises de dados, agora estruturada com o framework de agentes **LangChain**.

Imagine poder "conversar" com seu banco de dados, perguntando em português claro e recebendo não apenas tabelas, mas insights e gráficos que contam uma história. É exatamente isso que este projeto faz.

---

## 🎯 Qual o Objetivo?

O coração deste projeto é uma aplicação web, construída com Streamlit, que permite a qualquer pessoa fazer perguntas em linguagem natural sobre uma base de dados. Por trás da interface simples, uma orquestração de **cadeias (chains) do LangChain** trabalha para traduzir, buscar e explicar os dados, tornando a análise acessível a todos.

## ✨ Como a Mágica Acontece: A Arquitetura com LangChain

Para que a aplicação funcionasse de forma fluida e inteligente, optei por um fluxo de agentes orquestrado pelo LangChain, onde cada "especialista" é um componente de uma cadeia modular.

**O Fluxo:**
`Sua Pergunta` -> **Chain 1: O Tradutor** -> `Consulta SQL` -> **Agente 2: O Executor** -> `Dados Brutos` -> **Chain 2: O Analista** -> `Sua Resposta!`

-   **Agente 1: O Tradutor (Text-to-SQL Chain)**
    -   **Missão:** Este agente é uma "chain" do LangChain. Ele combina um template de prompt (com as instruções e o schema do banco), o modelo de linguagem e um parser de saída. Sua única tarefa é traduzir o que você pediu para uma consulta SQL precisa e segura.
    -   **Tecnologia:** `LangChain` para orquestração, `ChatGroq` como modelo (`llama3-70b-8192`) e `ChatPromptTemplate` para engenharia de prompt.

-   **Agente 2: O Executor de Dados**
    -   **Missão:** Este agente é uma função Python. Ele pega a consulta SQL da primeira chain, conecta-se ao banco de dados `clientes_completo.db`, executa a busca e retorna os dados em um DataFrame do Pandas.
    -   **Tecnologia:** As bibliotecas `sqlite3` e `pandas`.

-   **Agente 3: O Analista e Comunicador (Formatter Chain)**
    -   **Missão:** Uma segunda chain do LangChain que recebe os dados brutos e a sua pergunta original. Ela analisa as informações e gera um resumo em texto claro, objetivo e amigável.
    -   **Tecnologia:** Novamente, `LangChain` com `ChatGroq`, treinado para ser um comunicador de insights.

## 🛠️ Tecnologias no Projeto

-   **Linguagem:** Python
-   **Framework de Agentes:** LangChain
-   **Inteligência Artificial:** Groq API (Modelo Llama 3 70B)
-   **Frontend:** Streamlit
-   **Banco de Dados:** SQLite
-   **Manipulação de Dados:** Pandas
-   **Visualização de Dados:** Matplotlib

## ⚙️ Como Executar o Projeto

**Pré-requisitos:**
-   Python 3.8+
-   Uma chave de API da Groq salva em um arquivo `.env` como `GROQ_API_KEY="SUA_CHAVE_AQUI"`

**Siga os passos no terminal do projeto:**

1.  **Opcional, mas recomendado: Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows: .\\venv\\Scripts\\activate
    # No macOS/Linux: source venv/bin/activate
    ```

2.  **Instale todas as dependências de uma só vez:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute a aplicação:**
    ```bash
    streamlit run app.py
    ```

## 📝 Exemplos de Perguntas que Testei

-   `Liste os 5 estados com maior número de clientes.`
-   `Quantos clientes interagiram com campanhas de WhatsApp em 2024?`
-   `Qual o valor total de vendas por canal de compra, ordenado do maior para o menor?`
-   `Qual o número de reclamações não resolvidas por canal?`
-   `Liste os 10 clientes que mais gastaram no total.`

## 💡 Insights que Descobri com a Ferramenta

Ao usar a aplicação, pude extrair alguns insights interessantes que mostram o potencial da ferramenta para uma estratégia de Growth:

1.  **Canal de Vendas:** Ao perguntar "Qual o total de quantidade de vendas realizadas por canal", é possível notar que a maioria das compras acontece no 'site' com 331 vendas, seguido pelo 'app' com 323 e pela 'loja física' com 322.
2.  **Eficácia de Campanhas:** A pergunta `Quantos clientes interagiram com a campanha 'Black Friday'?` revela rapidamente o engajamento de uma ação específica, permitindo avaliar o ROI de campanhas de marketing quase em tempo real.
3.  **Pontos de Atrito no Suporte:** Ao visualizar as `reclamações não resolvidas por canal`, a equipe pode identificar qual canal de suporte (email, telefone, chat) está com mais problemas e precisa de mais atenção ou recursos.
4.  **Perfil do Cliente de Alto Valor:** A simples pergunta `Liste os 10 clientes que mais gastaram` pode ser o ponto de partida para a criação de um programa de fidelidade ou para ações de marketing direcionadas a esse público específico.

## 🚀 Próximos Passos e Melhorias

-   **SQL Agent Toolkit:** Para uma evolução, seria possível usar o `create_sql_agent` do próprio LangChain, que pode não apenas gerar, mas também executar e, em alguns casos, corrigir o SQL automaticamente.
-   **Cache Inteligente:** Armazenar as perguntas já feitas e seus resultados. O LangChain oferece mecanismos de cache que podem ser integrados para tornar as respostas repetidas instantâneas.
-   **Memória Conversacional:** Adicionar memória para permitir perguntas de acompanhamento, como "E desses clientes, quais são da profissão X?". O LangChain possui módulos de memória (`ConversationBufferMemory`) para isso.
-   **Visualizações Mais Avançadas:** Integrar com bibliotecas como Plotly ou Altair para permitir a criação de gráficos ainda mais interativos e detalhados.