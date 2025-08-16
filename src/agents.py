import os
import streamlit as st
from groq import Groq, APIError
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

MODEL_NAME = "llama3-70b-8192"

@st.cache_resource
def initialize_groq_client():
    """Inicializa e retorna o cliente da Groq."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        return None
    return Groq(api_key=api_key)

def create_sql_query_agent(client: Groq, user_prompt: str, schema: str) -> str:
    """Agente que gera uma query SQL a partir da solicitação do usuário."""
    system_prompt = f"""
Você é um especialista em SQL para um banco de dados SQLite. Sua única função é traduzir uma pergunta em linguagem natural para uma query SQL.

**Instruções:**
1.  **Schema:** Use o schema abaixo para entender as tabelas e colunas.
    <schema>{schema}</schema>
2.  **Traduza:** Converta a pergunta do usuário em uma query SQL válida.
3.  **Saída:** Sua resposta DEVE conter APENAS o código SQL puro, sem explicações ou formatação extra.
4.  **Datas:** As datas estão no formato 'YYYY-MM-DD'. Use `strftime('%m', data_compra) = '05'` para o mês de maio, por exemplo.
5.  **Segurança:** Gere apenas queries de leitura (`SELECT`).

**Pergunta:** "Liste os 5 estados com mais clientes"
**Saída Esperada:**
SELECT estado, COUNT(id) as total_clientes FROM clientes GROUP BY estado ORDER BY total_clientes DESC LIMIT 5;
"""
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"<pergunta>{user_prompt}</pergunta>"}
            ],
            temperature=0.0,
            max_tokens=1024,
        )
        sql_query = response.choices[0].message.content.strip()
        
        if sql_query.lower().startswith("```sql"):
            sql_query = sql_query[6:]
        if sql_query.endswith("```"):
            sql_query = sql_query[:-3]
        
        return sql_query.strip()
    except APIError as e:
        raise RuntimeError(f"Erro na API da Groq (SQL Agent): {e}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado no agente de SQL: {e}")

def format_response_agent(client: Groq, user_prompt: str, query_result: pd.DataFrame) -> str:
    """Agente que gera uma resposta amigável a partir dos resultados da query."""
    system_prompt = """
Você é um Analista de Dados assistente. Sua função é interpretar os resultados de uma consulta e apresentá-los de forma clara para o usuário.

**Instruções:**
1.  **Contexto:** Você receberá a pergunta original e os dados resultantes.
2.  **Tarefa:** Escreva um resumo textual que responda diretamente à pergunta com base nos dados.
3.  **Tom:** Seja profissional e conciso. Use markdown para formatar.
"""
    data_text = query_result.to_string(index=False, max_rows=10)
    user_content = (
        f"**Pergunta Original:**\n{user_prompt}\n\n"
        f"**Dados Resultantes:**\n{data_text}\n\n"
        "**Sua Resposta (resumo em texto):**"
    )
    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.3,
            max_tokens=2048,
        )
        return response.choices[0].message.content
    except APIError as e:
        raise RuntimeError(f"Erro na API da Groq (Formatter Agent): {e}")
    except Exception as e:
        raise RuntimeError(f"Erro inesperado no agente de formatação: {e}")