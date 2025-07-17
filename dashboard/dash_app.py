import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
from dashboard.config import read_metric_safely
from dashboard.utils import resource_card, metric_box, bytes_to_gb
import plotly.express as px
from datetime import datetime
import pytz
import pandas as pd
app = dash.Dash(__name__, update_title=None)
app.title = "Painel de Recursos"

# ---------- LAYOUT ----------

app.layout = html.Div([
    html.Div([
        html.H1("💻 Painel de Monitoramento"),
        html.Div(id='live-clock'),
        html.Div("127.0.0.1:8050", className='server-address'),
    ]),

    dcc.Interval(id='interval', interval=1000),

    html.Div([
        html.Div([
            resource_card("CPU", "cpu-gauge", "cpu-metrics", "#01D169", "Uso percentual da CPU"),
            resource_card("RAM", "ram-gauge", "ram-metrics", "#01D169", "Uso de memória RAM"),
        ], className='resource-column'),

        html.Div([
            resource_card("SWAP", "swap-gauge", "swap-metrics", "#01D169", "Uso de memória SWAP"),
            resource_card("DISCO", "disk-gauge", "disk-metrics", "#01D169", "Uso de espaço em disco"),
        ], className='resource-column'),

        html.Div([
            dcc.Tooltip(
                "Monitoramento em tempo real das temperaturas do hardware. Valores acima da linha vermelha indicam condições críticas.",
                id="temp-tooltip",
                targetable=True,
                className='temp-tooltip'
            ),
            html.Div([
                html.H3("🌡️ Sensores de Temperatura"),
                html.Div(id='temp-metrics'),
                dcc.Graph(id='temp-area-chart', config={'displayModeBar': False})
            ], className='temp-container')
        ], className='resource-column')
    ], className='main-container')
])

@app.callback(
    Output('live-clock', 'children'),
    Input('interval', 'n_intervals')
)
def update_clock(n):
    return html.Div(
        datetime.now(pytz.timezone('America/Sao_Paulo')).strftime('%H:%M:%S - %d/%m/%Y'),
        id="clock-text",
        className="clock-animation")

@app.callback(
    Output('temp-area-chart', 'figure'),
    Output('temp-metrics', 'children'),
    Input('interval', 'n_intervals')
)
def update_temp_chart(n):
    try:
        temp_data = read_metric_safely("temp.json")
        if not temp_data or 'temperatures' not in temp_data:
            return go.Figure(), []

        cores = []
        temps = []
        critical_points = []
        metrics = []

        # Organiza sensores e coleta dados
        for sensor_type in sorted(temp_data['temperatures']):  # ordena para consistência
            for sensor in temp_data['temperatures'][sensor_type]:
                raw_label = sensor.get('label', '').strip()
                label = raw_label or sensor_type

                # --- Conversão para nomes amigáveis ---
                if 'Package' in label:
                    label = "CPU"
                elif 'Core' in label:
                    label = label.replace("Core", "Núcleo")
                elif 'acpitz' in sensor_type.lower():
                    label = "Sensor Interno"
                elif 'coretemp' in sensor_type.lower():
                    label = f"Núcleo {raw_label[-1]}" if raw_label else "Sensor CPU"
                else:
                    label = label.title()
                current = sensor.get('current', 0)
                high = sensor.get('high')
                critical = sensor.get('critical')
                cores.append(label)
                temps.append(current)

                if critical:
                    critical_points.append(critical)

                # Cor condicional se ultrapassou o limite crítico
                color = '#FF5733' if critical and current > critical else '#020E78'

                # Cria as mini métricas
                metrics.append(
                    html.Div([
                        html.Div(label, style={
                            'fontSize': '13px',
                            'color': '#000'
                        }),
                        html.Div(f"{current}°C", style={
                            'fontWeight': 'bold',
                            'fontSize': '13px',
                            'color': '#020E78'
                            
                        }),
                        html.Div(f"High: {high or '—'}", style={
                            'fontSize': '11px',
                            'color': '#999'
                        }),
                        html.Div(f"Crit: {critical or '—'}", style={
                            'fontSize': '11px',
                            'color': '#C00'
                        })
                    ], style={
                        'padding': '8px',
                        'borderRadius': '6px',
                        'backgroundColor': False,
                        'boxShadow': '0 1px 3px rgba(0,0,0,0.08)'
                    })
                )

        # Cria o gráfico de área 
        df = pd.DataFrame({'Sensor': cores, 'Temperatura': temps})
        fig = px.area(
            df,
            x='Sensor',
            y='Temperatura',
            labels={'Sensor': '', 'Temperatura': 'Temperatura (°C)'}
        )

        fig.update_traces(
            fill='tozeroy',
            line=dict(color='#FF5733', width=2),
            fillcolor='rgba(255, 87, 51, 0.3)'
        )

        if critical_points:
            fig.add_hline(
                y=max(critical_points),
                line_dash="dash",
                line_color="red",
                annotation_text="Limite Crítico",
                annotation_position="bottom right",
                annotation_font_size=10,
                annotation_font_color="red"
            )

        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font={'color': '#000'},
            margin=dict(l=20, r=20, t=10, b=10),
            height=250,   
            yaxis=dict(showgrid=True, gridcolor='rgba(0,0,0,0.1)'),
            xaxis=dict(showticklabels=False)
        )

        return fig, metrics

    except Exception as e:
        print(f"Erro ao ler temperaturas: {e}")
        return go.Figure(), []


@app.callback(
    Output('cpu-gauge', 'figure'),
    Output('cpu-metrics', 'children'),
    Output('ram-gauge', 'figure'),
    Output('ram-metrics', 'children'),
    Output('swap-gauge', 'figure'),
    Output('swap-metrics', 'children'),
    Output('disk-gauge', 'figure'),
    Output('disk-metrics', 'children'),
    Input('interval', 'n_intervals')
)
def update_metrics(n):
    cpu = read_metric_safely("cpu.json")
    ram = read_metric_safely("ram.json")
    swap = read_metric_safely("swap.json")
    disk = read_metric_safely("disk.json")
    
    # ----- CPU -----
    cpu_percent = cpu.get('percent', 0)
    cpu_cores = cpu.get('cores', [])
    cpu_logical = cpu.get('logical', 0)
    cpu_physical = cpu.get('physical', 0)

    cpu_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=cpu_percent,
        number={'suffix': '%', 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#fff'},
            'bar': {'color': "#22E63C", 'thickness': 0.3},
            'bgcolor': '#333',
            'borderwidth': 5,
            'bordercolor': '#444',
            'steps': [
                {'range': [0, 50], 'color': '#333'},
                {'range': [50, 80], 'color': '#222'},
                {'range': [80, 100], 'color': '#111'}],
        }
    ))
    cpu_fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#000"}
    )
    
    cpu_metrics = html.Div([
        # metric_box("Núcleos físicos", cpu_physical),
        # metric_box("Núcleos lógicos", cpu_logical),
        html.Div("Uso por núcleo:", style={'fontWeight': 'bold', 'marginTop': '5px', 'color': '#000', 'fontSize': '12px'}),
        html.Div([
            html.Span(f"{p}% ", style={'color': '#000', 'fontSize': '11px'}) 
            for i, p in enumerate(cpu_cores)
        ], style={'display': 'flex', 'flexWrap': 'wrap', 'gap': '5px', 'marginTop': '5px'})
    ])

    # ----- RAM -----
    ram_percent = ram.get('percent', 0)
    ram_total = bytes_to_gb(ram.get('total', 0))
    ram_used = bytes_to_gb(ram.get('used', 0))
    ram_available = bytes_to_gb(ram.get('available', 0))

    ram_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=ram_percent,
        number={'suffix': '%', 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#444'},
            'bar': {'color':  "#22E63C", 'thickness': 0.3},
            'bgcolor': '#333',
            'borderwidth': 2,
            'bordercolor': '#444',
            'steps': [
                {'range': [0, 50], 'color': '#333'},
                {'range': [50, 80], 'color': '#222'},
                {'range': [80, 100], 'color': '#111'}],
        }
    ))
    ram_fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#000"}
    )
    ram_metrics = html.Div([
        metric_box("Total", ram_total, "GB"),
        metric_box("Usada", ram_used, "GB"),
        metric_box("Disponível", ram_available, "GB")
    ])

    # ----- SWAP -----
    swap_percent = swap.get('percent', 0)
    swap_total = bytes_to_gb(swap.get('total', 0))
    swap_used = bytes_to_gb(swap.get('used', 0))
    swap_free = bytes_to_gb(swap.get('free', 0))

    swap_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=swap_percent,
        number={'suffix': '%', 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#444'},
            'bar': {'color':  "#22E63C", 'thickness': 0.3},
            'bgcolor': '#333',
            'borderwidth': 2,
            'bordercolor': '#444',
            'steps': [
                {'range': [0, 50], 'color': '#333'},
                {'range': [50, 80], 'color': '#222'},
                {'range': [80, 100], 'color': '#111'}],
        }
    ))
    swap_fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#000"}
    )
    swap_metrics = html.Div([
        metric_box("Total", swap_total, "GB"),
        metric_box("Usada", swap_used, "GB"),
        metric_box("Livre", swap_free, "GB")
    ])

    # ----- DISCO -----
    disk_percent = disk.get('percent', 0)
    disk_total = bytes_to_gb(disk.get('total', 0))
    disk_used = bytes_to_gb(disk.get('used', 0))
    disk_free = bytes_to_gb(disk.get('free', 0))

    disk_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=disk_percent,
        number={'suffix': '%', 'font': {'size': 24}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': '#444'},
            'bar': {'color':  "#22E63C", 'thickness': 0.3},
            'bgcolor': '#333',
            'borderwidth': 2,
            'bordercolor': '#444',
            'steps': [
                {'range': [0, 50], 'color': '#333'},
                {'range': [50, 80], 'color': '#222'},
                {'range': [80, 100], 'color': '#111'}],
        }
    ))
    disk_fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        font={'color': "#000"}
    )
    disk_metrics = html.Div([
        metric_box("Total", disk_total, "GB"),
        metric_box("Usado", disk_used, "GB"),
        metric_box("Livre", disk_free, "GB")
    ])

    return cpu_fig, cpu_metrics, ram_fig, ram_metrics, swap_fig, swap_metrics, disk_fig, disk_metrics

# app.run(debug=True)
app.run(host="0.0.0.0", port=8050)