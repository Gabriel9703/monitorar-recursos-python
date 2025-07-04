import streamlit as st
from streamlit_autorefresh import st_autorefresh


from dashboard.utils import donut_chart, area_chart
from scripts.metrics_normal.cpu_info import CpuInfo
from scripts.metrics_normal.ram_info import RamInfo
from scripts.metrics_normal.network_info import NetworkInfo
from scripts.metrics_normal.disk_info import DiskInfo
from scripts.metrics_normal.swap_info import SwapInfo


st_autorefresh(interval=2000, key="auto-refresh")

info_cpu = CpuInfo()
info_ram = RamInfo()
info_disk = DiskInfo()
info_swap = SwapInfo()
info_network = NetworkInfo()

st.set_page_config(layout="wide")

st.title("🖥️ Sistema de Monitoramento de Recursos")
st.divider()

   
col1, col2 = st.columns(2)
with col1:
    col5, col6 = st.columns(2, border=True)
    col5.plotly_chart(donut_chart("CPU", info_cpu.get_cpu_usage_total(), "#025318"), use_container_width=True)
    col6.plotly_chart(donut_chart("RAM", info_ram.get_percent_memory(), "#11CA00"), use_container_width=True)
with col2:
    col7, col8 = st.columns(2, border=True)
    col7.plotly_chart(donut_chart("Disco", info_disk.get_percent_disk(), "#184022"), use_container_width=True)
    col8.plotly_chart(donut_chart("Swap", info_swap.get_percent_swap(),  "#0CED4C"), use_container_width=True)

col3, col4 = st.columns(2, border=True)
with col3:
    st.plotly_chart(area_chart("Variação de CPU", "#86CECF"), use_container_width=True)
with col4:
    st.plotly_chart(area_chart("Variação de RAM", "#99E9B0"), use_container_width=True)