import streamlit as st
from pathlib import Path
import json
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Atualiza a cada 5 segundos
st_autorefresh(interval=3000, key="process_refresh")

# No início do arquivo do dashboard
st.markdown("""
<style>
    .stDataFrame div[data-testid="stDataFrameContainer"] {
        font-family: monospace;
    }
    .stDataFrame th {
        background-color: #0E1117;
        color: white;
    }
    .stDataFrame tr:nth-child(even) {
        background-color: #262730;
    }
</style>
""", unsafe_allow_html=True)
def load_process_metrics():
    try:
        path = Path("/app/shared_metrics/processes.json")
        return json.loads(path.read_text())
    except:
        return None

# Layout do Dashboard
st.subheader("📊 Monitoramento de Processos")

metrics = load_process_metrics()

if metrics:
    summary = metrics['summary']
    processes = metrics['top_processes']
    
    # Métricas de resumo
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total", summary['total'])
    col2.metric("Running", summary['running'])
    col3.metric("Sleeping", summary['sleeping'])
    col4.metric("Zombie", summary.get('zombie', 0))  # zombie pode não existir
    
    # Tabela de processos
    st.markdown("### 🏆 Top 10 Processos (CPU)")
    df = pd.DataFrame(processes)
    
    # Formatação das colunas
    df['cpu_percent'] = df['cpu_percent'].apply(lambda x: f"{x:.1f}%")
    df['memory_percent'] = df['memory_percent'].apply(lambda x: f"{x:.1f}%")
    
    # Exibe a tabela com estilo
    st.dataframe(
        df[['pid', 'name', 'username', 'cpu_percent', 'memory_percent', 'status']],
        column_config={
            "pid": "PID",
            "name": "Nome",
            "username": "Usuário",
            "cpu_percent": "CPU %",
            "memory_percent": "Memória %",
            "status": "Status"
        },
        hide_index=True,
        use_container_width=False
    )
else:
    st.warning("Aguardando dados de processos...")