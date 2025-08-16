import pandas as pd
import matplotlib.pyplot as plt

def generate_plot(df: pd.DataFrame, chart_type: str, col_x: str, col_y: str):
    """Gera uma figura Matplotlib a partir do DataFrame de resultados."""
    if df.empty or col_x not in df.columns or col_y not in df.columns:
        raise ValueError("Dados ou colunas inválidas para gerar o gráfico.")

    fig, ax = plt.subplots(figsize=(10, 6))

    df[col_y] = pd.to_numeric(df[col_y], errors='coerce').fillna(0)
    df = df.sort_values(by=col_y, ascending=False)

    try:
        if chart_type == 'Barras':
            df_plot = df.head(15)
            ax.bar(df_plot[col_x].astype(str), df_plot[col_y], color='cornflowerblue')
            ax.set_title(f'Análise de {col_y} por {col_x}')
            plt.xticks(rotation=45, ha='right')

        elif chart_type == 'Pizza':
            df_plot = df.head(7)
            if len(df) > 7:
                others_sum = df.iloc[7:][col_y].sum()
                df_plot.loc['Outros'] = {col_x: 'Outros', col_y: others_sum}
            
            ax.pie(df_plot[col_y], labels=df_plot[col_x], autopct='%1.1f%%', startangle=90)
            ax.set_title(f'Distribuição de {col_y} por {col_x}')
            ax.axis('equal')

        elif chart_type == 'Linha':
            df_plot = df.head(20).sort_values(by=col_x)
            ax.plot(df_plot[col_x].astype(str), df_plot[col_y], marker='o', linestyle='-', color='green')
            ax.set_title(f'Tendência de {col_y} por {col_x}')
            plt.xticks(rotation=45, ha='right')
        
        ax.set_xlabel(col_x)
        ax.set_ylabel(col_y)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()
        
        return fig

    except Exception as e:
        plt.close(fig)
        raise RuntimeError(f"Erro ao gerar o gráfico: {e}")