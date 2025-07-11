import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
from pathlib import Path
import pandas as pd
from dashboard.utils import donut_chart, area_chart
from scripts.utils.format_out import format_bytes


st_autorefresh(interval=2000, key="auto-refresh")
st.set_page_config(layout="wide")
st.title("🖥️ Sistema de Monitoramento de Recursos")
st.divider()
# st.divider()


def load_metric(metric_name):
    try:
        path = Path(f"/app/shared_metrics/{metric_name}.json")
        return json.loads(path.read_text())
    except:
        None
            

cpu_data = load_metric('cpu')
ram_data = load_metric('ram')
swap_data = load_metric('swap')
net_data = load_metric('net')
disk_data = load_metric('disk')

col50, col60 = st.columns(2,border=False, gap="small")

with col50:
    col1, col2,  = st.columns(2, border=True, gap="small")

    # Coluna CPU
    with col1:
        col4, col5 = st.columns(2)
        if cpu_data:
            col4.plotly_chart(donut_chart("CPU", cpu_data['percent'], "#414EFF"), use_container_width=True)    
            with col5:
                if 'cores' in cpu_data:
                    formatted = "\n".join([f"Core {i}: {core:.1f}%"
                                        for i, core in enumerate(cpu_data['cores'])])
                    st.code(formatted)
                else:
                    st.warning("Dados de cores não disponíveis")
        
            st.plotly_chart(area_chart("", "#062D81"), use_container_width=True)
        else:
            st.warning("Aguardando dados da CPU...")

    # Coluna RAM
    with col2:
        col4, col5 = st.columns(2)
        if ram_data:
            col4.plotly_chart(donut_chart("RAM", ram_data['percent'], "#1C50FC"), use_container_width=True)
            with col5:
                st.metric("Total de RAM", format_bytes(ram_data['total']), delta_color="inverse")
                st.metric("Total usado", format_bytes(ram_data['used']), delta_color="inverse")
        
            st.plotly_chart(area_chart("", "#12BFFE"), use_container_width=True)
        else:
            st.warning("Aguardando dados da RAM...")

    # Coluna Swap
    col39, col40 = st.columns(2, border=True)
    with col40:
        col4, col5 = st.columns(2)
        if swap_data:
            col4.plotly_chart(donut_chart("Swap", swap_data['percent'], "#001761"), use_container_width=True)
            with col5:
                st.metric("Total de Swap", format_bytes(swap_data['total']), delta_color="inverse")
                st.metric("Total usado", format_bytes(swap_data['used']), delta_color="inverse")

            st.plotly_chart(area_chart("", "#093974"), use_container_width=True)
        else:
            st.warning("Aguardando dados de Swap...")

# Coluna Disco
    with col39:
        if disk_data:
            st.plotly_chart(donut_chart("Disco", disk_data['percent'], "#093974"), use_container_width=True)
            st.metric("Espaço livre", format_bytes(disk_data['free']))
        else:
            st.warning("Aguardando dados do Disco...")

# Coluna Rede
#######################################################
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

metrics = load_process_metrics()
with col60:
    col73, col74 = st.columns([6.5, 3.5], border=False, gap="small")
    # st.subheader("📊 Monitoramento de Processos")
    if metrics:
        summary = metrics['summary']
        processes = metrics['top_processes']
        
        with col74:
        # Métricas de resumo
            
            col1, col2,  = st.columns(2,border=True)
            col1.metric("Total", summary['total'])
            col1.metric("Running", summary['running'])
            col2.metric("Sleeping", summary['sleeping'])
            col2.metric("Zombie", summary.get('zombie', 0))  # zombie pode não existir

        with col73:    
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
                use_container_width=True
            )
    else:
        st.warning("Aguardando dados de processos...")        