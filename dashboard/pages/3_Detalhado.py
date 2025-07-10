# import streamlit as st
# from streamlit_autorefresh import st_autorefresh

# from scripts.metrics_normal.cpu_info import CpuInfo
# from scripts.metrics_normal.ram_info import RamInfo
# from scripts.metrics_normal.network_info import NetworkInfo
# from scripts.metrics_normal.disk_info import DiskInfo
# from scripts.metrics_normal.swap_info import SwapInfo
# from scripts.utils.format_out import format_bytes


# st_autorefresh(interval=1000, key="auto-refresh")
# st.set_page_config(layout="wide")
# st.title("🖥️ Sistema de Monitoramento de Recursos")
   
# info_cpu = CpuInfo()
# info_ram = RamInfo()
# info_disk = DiskInfo()
# info_swap = SwapInfo()
# info_network = NetworkInfo()
  
# secao = st.sidebar.selectbox("Detalhar:", ["RAM", "Swap", "CPU","Rede"])

# if secao == "RAM":
#     st.subheader("Detalhes da RAM")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Total de RAM", f'{format_bytes(info_ram.get_total_memory())}', delta_color="inverse")

#     with col2:
#         st.metric("Total usado de RAM", f'{format_bytes(info_ram.get_used_memory())}', delta_color="inverse")

#     col3, col4 = st.columns(2)
#     with col3:
#         st.metric("Total livre de RAM", f'{format_bytes(info_ram.get_free_memory())}', delta_color="inverse")

#     with col4:
#         st.metric("Percentual de uso de RAM", f'{info_ram.get_percent_memory()}%', delta_color="inverse")



# elif secao == "Swap":
#     st.subheader("Detalhes do Swap")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Total de Swap", f'{format_bytes(info_swap.get_total_swap())}', delta_color="inverse")

#     with col2:
#         st.metric("Total usado de Swap", f'{format_bytes(info_swap.get_used_swap())}', delta_color="inverse")

#     col3, col4 = st.columns(2)
#     with col3:
#         st.metric("Total livre de Swap", f'{format_bytes(info_swap.get_free_swap())}', delta_color="inverse")

#     with col4:
#         st.metric("Percentual de uso de Swap", f'{info_swap.get_percent_swap()}%', delta_color="inverse")  

# elif secao == "CPU":
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


# elif secao == "Rede":
#     st.subheader("Detalhes da Rede")
#     col1, col2 = st.columns(2)
#     with col1:
#         st.metric("Bytes enviados", f'{format_bytes(info_network.get_total_sent())}', delta_color="inverse")

#     with col2:
#         st.metric("Bytes recebidos", f'{format_bytes(info_network.get_total_recv())}', delta_color="inverse")

#     col3, col4 = st.columns(2)
#     with col3:
#         st.metric("Pacotes enviados", f'{info_network.get_total_packets_sent()}')

#     with col4:
#         st.metric("Pacotes recebidos", f'{info_network.get_total_packets_recv()}')   



