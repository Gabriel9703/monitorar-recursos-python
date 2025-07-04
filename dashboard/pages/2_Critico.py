import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

from metrics_static.cpu_info import CpuInfo
from metrics_static.ram_info import RamInfo
from metrics_static.network_info import NetworkInfo
from metrics_static.disk_info import DiskInfo
from metrics_static.swap_info import SwapInfo
from database.get_logs_db import get_last_cpu_logs, get_last_ram_logs, get_last_network_logs,  get_last_disk_logs, get_last_swap_logs



st_autorefresh(interval=10000, key="auto-refresh")



info_cpu = CpuInfo()
info_ram = RamInfo()
info_disk = DiskInfo()
info_swap = SwapInfo()
info_network = NetworkInfo()

st.set_page_config(layout="wide")
st.title("🖥️ Sistema de Monitoramento de Recursos")    

col1, col2, col3, col4, col5 = st.columns(5, border=True)
with col1:
    if st.button("Ver logs CPU"):
        logs_cpu = get_last_cpu_logs()
        df = pd.DataFrame(logs_cpu)
        st.dataframe(df)

with col2:
    if st.button("Ver logs RAM"):
        logs_ram = get_last_ram_logs()
        df = pd.DataFrame(logs_ram)
        st.table(df)

with col3:
    if st.button("Ver logs Rede"):
        logs_network = get_last_network_logs()
        df = pd.DataFrame(logs_network)
        st.table(df)

with col4:
    if st.button("Ver logs Disco"):
        logs_disk = get_last_disk_logs()
        df = pd.DataFrame(logs_disk)
        st.table(df)

with col5:
    if st.button("Ver logs Swap"):
        logs_swap = get_last_swap_logs()
        df = pd.DataFrame(logs_swap)
        st.table(df)