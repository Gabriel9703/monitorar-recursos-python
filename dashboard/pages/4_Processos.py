# import streamlit as st
# from scripts.metrics_critical.monitor_process import get_processes_sumary_for_app 
# from streamlit_autorefresh import st_autorefresh




# st_autorefresh(interval=5000, key="auto-refresh")

# summary, df_top = get_processes_sumary_for_app()

# st.subheader("📊 Monitoramento de Processos")


# col1, col2, col3, col4 = st.columns(4)
# col1.metric("Total de Processos", summary['total'])
# col2.metric("Running", summary['running'])
# col3.metric("Sleeping", summary['sleeping'])
# col4.metric("Zombie", summary['zombie'])

# st.markdown("### 🧠 Top 10 Processos por Uso de CPU")
# col5, col6 = st.columns([7.0, 3.0]) 
# col5.dataframe(df_top.style.format({"cpu_percent": "{:.1f}%", "memory_percent": "{:.1f}%"}), hide_index=True)

