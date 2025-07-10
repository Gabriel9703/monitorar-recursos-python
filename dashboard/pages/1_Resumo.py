import streamlit as st
from streamlit_autorefresh import st_autorefresh
import json
from pathlib import Path

from dashboard.utils import donut_chart, area_chart
from scripts.utils.format_out import format_bytes


st_autorefresh(interval=2000, key="auto-refresh")
st.set_page_config(layout="wide")
st.title("🖥️ Sistema de Monitoramento de Recursos")
st.divider()


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

 
col1, col2, col3, col10 = st.columns([3.0, 2.5, 2.5, 2.0], border=False, gap="small")

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
with col3:
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
with col10:
    if disk_data:
        st.plotly_chart(donut_chart("Disco", disk_data['percent'], "#093974"), use_container_width=True)
        st.metric("Espaço livre", format_bytes(disk_data['free']))
    else:
        st.warning("Aguardando dados do Disco...")