# import streamlit as st
# import pandas as pd
# import random

# import plotly.graph_objects as go
# import time 
# from metrics_static.cpu_info import CpuInfo
# from metrics_static.ram_info import RamInfo
# from metrics_static.network_info import NetworkInfo
# from metrics_static.disk_info import DiskInfo
# from metrics_static.swap_info import SwapInfo
# # from scripts.utils.format_out import format_bytes
# import pandas as pd
# from database.logs_repository import get_last_cpu_logs, get_last_ram_logs, get_last_network_logs,  get_last_disk_logs, get_last_swap_logs
# from streamlit_autorefresh import st_autorefresh

# # Roda a cada 5 segundos (5000 milissegundos)
# st_autorefresh(interval=5000, key="auto-refresh")


# def format_bytes(bytes):
#     if bytes < 1024:
#         return f"{bytes} bytes"
#     elif bytes < 1024**2:
#         return f"{bytes / 1024:.2f} KB"
#     elif bytes < 1024**3:
#         return f"{bytes / 1024**2:.2f} MB"
#     else:
#         return f"{bytes / 1024**3:.2f} GB"
    
# info_cpu = CpuInfo()
# info_ram = RamInfo()
# info_disk = DiskInfo()
# info_swap = SwapInfo()
# info_network = NetworkInfo()

# def donut_chart(label, percent, cor):
#     fig = go.Figure(go.Pie(
#         values=[percent, 100 - percent],
#         labels=["Usado", "Livre"],
#         hole=0.6,
#         marker_colors=[cor, "#e8e8e8"],
#         textinfo="none"
#     ))
#     fig.update_layout(
#         title={
#             "text": f"{label}: {percent:.1f}%",
#             "x": 0.5,
#             "xanchor": "center"
#         },
#         showlegend=False,
#         margin=dict(t=50, b=0, l=0, r=0),
#         height=200
#     )
#     return fig

# def area_chart(title, cor):
#     y = [random.uniform(30, 80) for _ in range(20)]
#     fig = go.Figure(go.Scatter(
#         y=y,
#         fill='tozeroy',
#         mode='lines',
#         line=dict(color=cor)
#     ))
#     fig.update_layout(
#         title=title,
#         margin=dict(t=30, b=0, l=0, r=0),
#         height=180,
#         xaxis=dict(visible=False),
#         yaxis=dict(visible=False),
#     )
#     return fig

# st.set_page_config(layout="wide")
# st.title("🖥️ Sistema de Monitoramento de Recursos")

# modo = st.sidebar.selectbox("Escolha uma opçao:", ["Resumo", "Critico", "Detalhado"])

# if modo == "Resumo":
   
#         col1, col2 = st.columns(2)
#         with col1:
#             st.plotly_chart(donut_chart("CPU", info_cpu.get_cpu_usage_total(), "#FF6B6B"), use_container_width=True)
#             st.plotly_chart(donut_chart("Disco", info_disk.get_percent_disk(), "#FFA94D"), use_container_width=True)
#         with col2:
#             st.plotly_chart(donut_chart("RAM", info_ram.get_percent_memory(), "#4D96FF"), use_container_width=True)
#             st.plotly_chart(donut_chart("Swap", info_swap.get_percent_swap(), "#20C997"), use_container_width=True)

#         # Parte de baixo: gráfico de área com variação
#         col3, col4 = st.columns(2)
#         with col3:
#             st.plotly_chart(area_chart("Variação de CPU", "#FF6B6B"), use_container_width=True)
#         with col4:
#             st.plotly_chart(area_chart("Variação de RAM", "#4D96FF"), use_container_width=True)


# elif modo == "Critico":
#     col1, col2, col3, col4, col5 = st.columns(5)
#     with col1:
#         if st.button("Ver logs CPU"):
#             logs_cpu = get_last_cpu_logs()
#             df = pd.DataFrame(logs_cpu)
#             st.table(df)

#     with col2:
#         if st.button("Ver logs RAM"):
#             logs_ram = get_last_ram_logs()
#             df = pd.DataFrame(logs_ram)
#             st.table(df)

#     with col3:
#         if st.button("Ver logs Rede"):
#             logs_network = get_last_network_logs()
#             df = pd.DataFrame(logs_network)
#             st.table(df)

#     with col4:
#         if st.button("Ver logs Disco"):
#             logs_disk = get_last_disk_logs()
#             df = pd.DataFrame(logs_disk)
#             st.table(df)

#     with col5:
#         if st.button("Ver logs Swap"):
#             logs_swap = get_last_swap_logs()
#             df = pd.DataFrame(logs_swap)
#             st.table(df)

# else:
  
#     secao = st.sidebar.selectbox("Detalhar:", ["CPU", "RAM", "Rede", "Swap"])
#     if secao == "CPU":
#         st.subheader("Detalhes da CPU")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Uso Total de CPU", f'{info_cpu.get_cpu_usage_total()}%', delta_color="inverse")

#         with col2:            
#             st.metric("Quantidade de CPUs Lógicas", f'{info_cpu.get_cpu_count_logical()}')


#         col3, col4 = st.columns(2)
#         with col3:
#             st.metric("Quantidade de CPUs Físicas", f'{info_cpu.get_cpu_count_physical()}')

#         with col4:
#             st.write("Uso de cada core")
#             core_usages = info_cpu.get_cpu_usage_each()
#             formatted = "\n".join([f"Core {core}: {usage:.1f}%" for core, usage in core_usages])
#             st.code(formatted)


#     elif secao == "RAM":
#         st.subheader("Detalhes da RAM")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Total de RAM", f'{format_bytes(info_ram.get_total_memory())}', delta_color="inverse")

#         with col2:
#             st.metric("Total usado de RAM", f'{format_bytes(info_ram.get_used_memory())}', delta_color="inverse")

#         col3, col4 = st.columns(2)
#         with col3:
#             st.metric("Total livre de RAM", f'{format_bytes(info_ram.get_free_memory())}', delta_color="inverse")

#         with col4:
#             st.metric("Percentual de uso de RAM", f'{info_ram.get_percent_memory()}%', delta_color="inverse")


#     elif secao == "Rede":
#         st.subheader("Detalhes da Rede")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Bytes enviados", f'{format_bytes(info_network.get_total_sent())}', delta_color="inverse")

#         with col2:
#             st.metric("Bytes recebidos", f'{format_bytes(info_network.get_total_recv())}', delta_color="inverse")

#         col3, col4 = st.columns(2)
#         with col3:
#             st.metric("Pacotes enviados", f'{info_network.get_total_packets_sent()}')

#         with col4:
#             st.metric("Pacotes recebidos", f'{info_network.get_total_packets_recv()}')   



#     elif secao == "Swap":
#         st.subheader("Detalhes do Swap")
#         col1, col2 = st.columns(2)
#         with col1:
#             st.metric("Total de Swap", f'{format_bytes(info_swap.get_total_swap())}', delta_color="inverse")

#         with col2:
#             st.metric("Total usado de Swap", f'{format_bytes(info_swap.get_used_swap())}', delta_color="inverse")

#         col3, col4 = st.columns(2)
#         with col3:
#             st.metric("Total livre de Swap", f'{format_bytes(info_swap.get_free_swap())}', delta_color="inverse")

#         with col4:
#             st.metric("Percentual de uso de Swap", f'{info_swap.get_percent_swap()}%', delta_color="inverse")             

