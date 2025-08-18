import streamlit as st
import pandas as pd
from src.database import get_schema_representation, execute_query
from src.agents import initialize_groq_client, create_sql_query_agent, format_response_agent
from src.chart_generator import generate_plot

# --- Configuração da Página ---
st.set_page_config(
    page_title="Análise com IA | Desafio Técnico",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

client = initialize_groq_client()

if 'current_query' not in st.session_state:
    st.session_state.current_query = ""
if 'query_result_df' not in st.session_state:
    st.session_state.query_result_df = None
if 'analysis_text' not in st.session_state:
    st.session_state.analysis_text = ""
if 'generated_sql' not in st.session_state:
    st.session_state.generated_sql = ""
if 'error_message' not in st.session_state:
    st.session_state.error_message = ""

# --- Interface do Usuário (Sidebar) ---
with st.sidebar:
    st.title("🤖 Assistente de Análise")
    st.markdown("""
    Este é um protótipo para o desafio técnico de estágio.
    **Como usar:**
    1.  Faça uma pergunta em linguagem natural sobre os dados.
    2.  Clique em **"Analisar"**.
    3.  A IA irá gerar e executar uma consulta SQL para encontrar a resposta.
    """)

    st.subheader("Exemplos de Perguntas:")
    st.markdown("""
    - `Liste os 5 estados com maior número de clientes.`
    - `Qual o valor total de compras por categoria de produto?`
    - `Quantas reclamações não resolvidas existem por canal de suporte?`
    - `Mostre o número de clientes que interagiram com a campanha 'Black Friday'.`
    """)

    st.divider()
    footer_html = """
    <div style="text-align: center; padding-top: 20px; color: grey; font-size: 14px;">
        <p>Feito por <a href="https://www.linkedin.com/in/gustavo-castro-06668b231/" target="_blank" style="color: grey; text-decoration: none;">Gustavo Rabutske</a></p>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


#Interface Principal
st.title("🔍 Análise de dados com agente de IA (Groq)")
st.markdown("Faça uma pergunta sobre os dados de clientes, compras, suporte ou marketing.")

#DETALHES DA APLICAÇÃO 
with st.expander("ℹ️ Como esta aplicação funciona? (Clique para expandir)"):
    st.markdown("""
    Esta aplicação utiliza uma arquitetura de **agentes de IA** para transformar perguntas em linguagem natural em insights de dados. O processo funciona em três etapas principais:

    1.  **Agente 1: O Tradutor (Text-to-SQL)**
        -   Quando você faz uma pergunta, este agente a recebe junto com um "mapa" do banco de dados (o schema).
        -   Sua única tarefa é traduzir sua pergunta em uma consulta SQL precisa.

    2.  **Agente 2: O Consultor (Executor SQL)**
        -   Este agente (uma função em Python) pega a consulta SQL gerada, conecta-se ao banco de dados `clientes_completo.db` e busca os dados exatos.

    3.  **Agente 3: O Analista (Formatador da Resposta)**
        -   Ele recebe os dados brutos do Agente 2 e sua pergunta original.
        -   Sua função é analisar a tabela de resultados e escrever o resumo em texto claro e direto que você vê na tela.

    Este fluxo garante que cada etapa do processo seja tratada por um especialista, resultando em respostas mais rápidas e precisas.
    """)


#area de input da pergunta do usuario
user_prompt = st.text_area(
    "Sua pergunta:",
    placeholder="Ex: Qual o número de reclamações não resolvidas por canal?",
    height=100,
    key="user_prompt_input"
)

analyze_button = st.button("Analisar", type="primary", use_container_width=True)


# --- Lógica de Orquestração dos Agentes ---
if analyze_button and user_prompt:
    if not client:
        st.error("Cliente da API não inicializado. Verifique suas credenciais no arquivo .env.")
    else:
        # Limpa o estado anterior
        st.session_state.query_result_df = None
        st.session_state.analysis_text = ""
        st.session_state.generated_sql = ""
        st.session_state.error_message = ""

        try:
            with st.spinner("Agente 1: Interpretando sua pergunta e gerando a consulta SQL..."):
                schema = get_schema_representation()
                sql_query = create_sql_query_agent(client, user_prompt, schema)
                st.session_state.generated_sql = sql_query

            with st.spinner("Agente 2: Executando a consulta no banco de dados..."):
                query_result_df = execute_query(sql_query)
                st.session_state.query_result_df = query_result_df

            with st.spinner("Agente 3: Gerando a análise dos resultados..."):
                if query_result_df.empty:
                    st.session_state.analysis_text = "A consulta não retornou resultados. Tente uma pergunta diferente."
                else:
                    analysis_text = format_response_agent(client, user_prompt, query_result_df)
                    st.session_state.analysis_text = analysis_text

        except (ValueError, RuntimeError) as e:
            st.session_state.error_message = str(e)
        except Exception as e:
            st.session_state.error_message = f"Ocorreu um erro inesperado no fluxo: {e}"


# --- Exibição dos Resultados ---
if st.session_state.error_message:
    st.error(f"**Ocorreu um erro:**\n\n{st.session_state.error_message}")
    if st.session_state.generated_sql:
        st.warning("**SQL Gerado (com erro):**")
        st.code(st.session_state.generated_sql, language="sql")

if st.session_state.analysis_text:
    st.divider()
    st.header("Resultados da Análise")

    col1, col2 = st.columns([0.6, 0.4])

    with col1:
        st.subheader("💡 Resumo da IA")
        st.markdown(st.session_state.analysis_text)

    with col2:
        st.subheader("📄 Dados Retornados")
        if st.session_state.query_result_df is not None and not st.session_state.query_result_df.empty:
            st.dataframe(st.session_state.query_result_df, use_container_width=True)
        else:
            st.info("Nenhum dado para exibir.")

    # Expander para detalhes técnicos
    with st.expander("Ver detalhes técnicos (Consulta SQL Gerada)"):
        st.code(st.session_state.generated_sql, language="sql")


# --- Seção de Geração de Gráficos ---
if st.session_state.query_result_df is not None and not st.session_state.query_result_df.empty:
    st.divider()
    st.header("📊 Gerador de Gráficos")

    df = st.session_state.query_result_df
    columns = df.columns.tolist()

    # Tenta identificar colunas categóricas e numéricas automaticamente
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()

    if len(categorical_cols) > 0 and len(numeric_cols) > 0:
        with st.form("graph_form"):
            st.markdown("Crie uma visualização a partir dos dados retornados.")

            c1, c2, c3 = st.columns(3)
            with c1:
                chart_type = st.selectbox("Tipo de Gráfico", ["Barras", "Pizza", "Linha"], key="chart_type")
            with c2:
                col_x_index = columns.index(categorical_cols[0])
                col_x = st.selectbox("Eixo X / Categoria", columns, index=col_x_index, key="col_x")
            with c3:
                col_y_index = columns.index(numeric_cols[0])
                col_y = st.selectbox("Eixo Y / Valor", columns, index=col_y_index, key="col_y")

            submitted = st.form_submit_button("Gerar Gráfico", use_container_width=True)
            if submitted:
                try:
                    with st.spinner("Criando visualização..."):
                        fig = generate_plot(df, chart_type, col_x, col_y)
                        st.pyplot(fig)
                except (ValueError, RuntimeError) as e:
                    st.error(f"Erro ao gerar gráfico: {e}")
    else:
        st.info("Os dados retornados não possuem a combinação necessária de colunas categóricas e numéricas para sugerir um gráfico.")