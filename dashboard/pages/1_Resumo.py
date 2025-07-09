import streamlit as st
from streamlit_autorefresh import st_autorefresh


from dashboard.utils import donut_chart, area_chart
from scripts.metrics_normal.cpu_info import CpuInfo
from scripts.metrics_normal.ram_info import RamInfo
from scripts.metrics_normal.network_info import NetworkInfo
from scripts.metrics_normal.disk_info import DiskInfo
from scripts.metrics_normal.swap_info import SwapInfo
from scripts.utils.format_out import format_bytes


st_autorefresh(interval=2000, key="auto-refresh")

info_cpu = CpuInfo()
info_ram = RamInfo()
info_disk = DiskInfo()
info_swap = SwapInfo()
info_network = NetworkInfo()

st.set_page_config(layout="wide")

st.title("🖥️ Sistema de Monitoramento de Recursos")
st.divider()

   
col1, col2 = st.columns([4.0, 6.0], border=False, gap="small")
with col1:
    col4, col5 = st.columns(2)
    col4.plotly_chart(donut_chart("CPU", info_cpu.get_cpu_usage_total(), "#414EFF"), use_container_width=True)    
    with col5:
        core_usages = info_cpu.get_cpu_usage_each()
        formatted = "\n".join([f"Core {core}: {usage:.1f}%" for core, usage in core_usages])
        st.code(formatted)
        
    st.plotly_chart(area_chart("", "#062D81"), use_container_width=True)

with col2:
    col4, col5 = st.columns(2)
    col4.plotly_chart(donut_chart("RAM", info_ram.get_percent_memory(), "#1C50FC"), use_container_width=True)
    with col5:
        st.metric("Total de RAM", f'{format_bytes(info_ram.get_total_memory())}', delta_color="inverse")
        st.metric("Total usado de RAM", f'{format_bytes(info_ram.get_used_memory())}', delta_color="inverse")
        
    st.plotly_chart(area_chart("", "#12BFFE"), use_container_width=True)

col3, col4 = st.columns(2, border=True)
with col3:
    st.plotly_chart(donut_chart("Disco", info_disk.get_percent_disk(), "#093974"), use_container_width=True)
with col4:
    col4, col5 = st.columns(2)
    col4.plotly_chart(donut_chart("Swap", info_swap.get_percent_swap(),  "#001761"), use_container_width=True)
    with col5:
        st.metric("Total de Swap", f'{format_bytes(info_swap.get_total_swap())}', delta_color="inverse")
        st.metric("Total usado de Swap", f'{format_bytes(info_swap.get_used_swap())}', delta_color="inverse")

    st.plotly_chart(area_chart("", "#093974"), use_container_width=True)
