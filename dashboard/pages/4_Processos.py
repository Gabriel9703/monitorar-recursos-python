import streamlit as st
from scripts.metrics_critical.monitor_process import get_process_summary_and_top
from time import sleep
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, key="auto-refresh")

def mostrar_processos():
    st.subheader("📊 Monitoramento de Processos (estilo top)")

    summary, df_top = get_process_summary_and_top(limit=10)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Processos", summary['total'])
    col2.metric("Running", summary['running'])
    col3.metric("Sleeping", summary['sleeping'])
    col4.metric("Zombie", summary['zombie'])

    st.markdown("### 🧠 Top 10 Processos por Uso de CPU")
    st.dataframe(df_top.style.format({"cpu_percent": "{:.1f}%", "memory_percent": "{:.1f}%"}), height=400)

