import random

import streamlit as st
from streamlit_autorefresh import st_autorefresh

import plotly.graph_objects as go
from metrics_static.cpu_info import CpuInfo
from metrics_static.ram_info import RamInfo
from metrics_static.network_info import NetworkInfo
from metrics_static.disk_info import DiskInfo
from metrics_static.swap_info import SwapInfo


st_autorefresh(interval=2000, key="auto-refresh")



info_cpu = CpuInfo()
info_ram = RamInfo()
info_disk = DiskInfo()
info_swap = SwapInfo()
info_network = NetworkInfo()


def donut_chart(label, percent, cor):
    fig = go.Figure(go.Pie(
        values=[percent, 100 - percent],
        labels=["Usado", "Livre"],
        hole=0.6,
        marker_colors=[cor, "#e8e8e8"],
        textinfo="none"
    ))
    fig.update_layout(
        title={
            "text": f"{label}: {percent:.1f}%",
            "x": 0.5,
            "xanchor": "center"
        },
        showlegend=False,
        margin=dict(t=50, b=0, l=0, r=0),
        height=200
    )
    return fig

def area_chart(title, cor):
    y = [random.uniform(30, 80) for _ in range(20)]
    fig = go.Figure(go.Scatter(
        y=y,
        fill='tozeroy',
        mode='lines',
        line=dict(color=cor)
    ))
    fig.update_layout(
        title=title,
        margin=dict(t=30, b=0, l=0, r=0),
        height=180,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
    )
    return fig

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

# Parte de baixo: gráfico de área com variação
col3, col4 = st.columns(2, border=True)
with col3:
    st.plotly_chart(area_chart("Variação de CPU", "#86CECF"), use_container_width=True)
with col4:
    st.plotly_chart(area_chart("Variação de RAM", "#99E9B0"), use_container_width=True)