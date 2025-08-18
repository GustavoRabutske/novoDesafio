# 🤖 AI Data Agent: Análise de dados em linguagem natural

Este projeto é a minha solução para o **Desafio Técnico**. A ideia foi criar uma ferramenta inteligente e intuitiva que transforma perguntas do dia a dia em análises de dados.

Imagine poder "conversar" com seu banco de dados, perguntando em português claro e recebendo não apenas tabelas, mas insights e gráficos que contam uma história. É exatamente isso que este projeto faz.

---

## 🎯 Qual o Objetivo?

O coração deste projeto é uma aplicação web, construída com Streamlit, que permite a qualquer pessoa fazer perguntas em linguagem natural sobre uma base de dados. Por trás da interface simples, uma orquestração de agentes de IA trabalha para traduzir, buscar e explicar os dados, tornando a análise acessível a todos, sem a necessidade de escrever uma única linha de código SQL.

## ✨ Como a Mágica Acontece: A Arquitetura de Agentes

Para que a aplicação funcionasse de forma fluida e inteligente, optei por um fluxo de agentes, onde cada "especialista" tem uma única e clara responsabilidade.

**O Fluxo:**
`Sua Pergunta` -> **Agente 1: O Tradutor** -> `Consulta SQL` -> **Agente 2: O Executor** -> `Dados Brutos` -> **Agente 3: O Analista** -> `Sua Resposta!`

-   **Agente 1: O Tradutor (Text-to-SQL)**
    -   **Missão:** Este agente é um especialista em SQL. Ele recebe a sua pergunta e um "mapa" do banco de dados. Sua única tarefa é traduzir o que você pediu para uma consulta SQL precisa e segura.
    -   **Tecnologia:** Usei o modelo `llama3-70b-8192` via API da Groq, com um prompt cuidadosamente elaborado para garantir que o SQL gerado seja sempre correto.

-   **Agente 2: O Executor de Dados**
    -   **Missão:** Na verdade, este agente é uma função Python eficiente. Ele pega a consulta SQL do primeiro agente, conecta-se ao banco de dados `clientes_completo.db`, executa a busca e retorna os dados em um DataFrame do Pandas.
    -   **Tecnologia:** As bibliotecas `sqlite3` e `pandas`.

-   **Agente 3: O Analista e Comunicador**
    -   **Missão:** Este agente recebe os dados brutos e a sua pergunta original. Ele analisa as informações e gera um resumo em texto claro, objetivo e amigável, exatamente como um analista de dados faria ao apresentar.
    -   **Tecnologia:** Novamente, o `llama3-70b-8192`, desta vez treinado para ser um comunicador de insights.

## 🛠️ Tecnologias no Projeto

-   **Linguagem:** Python
-   **Inteligência Artificial:** Groq API (Modelo Llama 3 70B)
-   **Frontend:** Streamlit
-   **Banco de Dados:** SQLite
-   **Manipulação de Dados:** Pandas
-   **Visualização de Dados:** Matplotlib




## ⚙️ Como Executar o Projeto

**Pré-requisitos:**
-   Python 3.8+

**Passos:**

1.  **Instale todas as dependências de uma só vez:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Opcional, mas recomendado: Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows: .\\venv\\Scripts\\activate
    # No macOS/Linux: source venv/bin/activate
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

Este projeto é um protótipo funcional, mas que pode crescer e muito em funcionalidades. Aqui estão algumas ideias para torná-lo ainda mais poderoso:

-   **Agente Corretor de SQL:** Implementar um "quarto agente" que, em caso de erro na execução da consulta, analisa o erro e tenta corrigir o SQL gerado pelo primeiro agente antes de retornar um erro para o usuário.
-   **Cache Inteligente:** Armazenar as perguntas já feitas e seus resultados. Se um usuário fizer a mesma pergunta ou muito parecida, a resposta seria instantânea, economizando tempo e processamento da API.
-   **Pergunta de acompanhamento:** Adicionar uma opção de continuar a conversa com a IA através de pergunta de acompanhamento, onde após a análise inicial, eu poderia continuar realizando outras perguntas com base na análise anterior.
-   **Visualizações Mais Avançadas:** Integrar com bibliotecas como Plotly ou Altair para permitir a criação de gráficos ainda mais interativos e detalhados.

