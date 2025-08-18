import sqlite3
import pandas as pd
import streamlit as st
import os

# Banco de dados usado para análise
DB_PATH = 'clientes_completo.db'

def get_db_connection():
    """Cria e retorna uma conexão com o banco de dados SQLite."""
    if not os.path.exists(DB_PATH):
        st.error(f"Erro: O arquivo do banco de dados '{DB_PATH}' não foi encontrado. Certifique-se de que ele está na raiz do projeto.")
        return None
    return sqlite3.connect(DB_PATH)

def get_schema_representation():
    """
    Obtém uma representação em texto do schema do banco de dados
    para ser usada no prompt da IA.
    """
    conn = get_db_connection()
    if not conn:
        return ""
        
    cursor = conn.cursor()
    
    schema_str = "Estrutura do Banco de Dados SQLite:\n\n"
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    for table_name in tables:
        table_name = table_name[0]
        schema_str += f"Tabela: {table_name}\n"
        
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        
        schema_str += "  Colunas:\n"
        for col in columns:
            col_name = col[1]
            col_type = col[2]
            schema_str += f"    - {col_name} ({col_type})\n"
        schema_str += "\n"
        
    conn.close()
    return schema_str

# --- AGENTE 2: O Executor de Dados ---
# Este é o segundo agente, o consultor de dados. Na prática, é uma função
# Python que faz o trabalho de se conectar no banco de dados. Ele recebe
# o SQL que o Agente 1 gerou, vai até o banco, executa a consulta e traz de
# volta os resultados. O retorno é um DataFrame do Pandas
@st.cache_data(ttl=3600)
def execute_query(query: str):
    """
    Executa uma query SQL no banco de dados e retorna o resultado como um DataFrame.
    """
    try:
        conn = get_db_connection()
        if not conn:
            raise ValueError("Não foi possível conectar ao banco de dados.")
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except pd.errors.DatabaseError as e:
        raise ValueError(f"Erro ao executar a query SQL: {e}. A query gerada pode estar incorreta.")
    except Exception as e:
        raise RuntimeError(f"Ocorreu um erro inesperado ao consultar o banco de dados: {e}")