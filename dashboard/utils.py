import dash
from dash import dcc, html

def bytes_to_gb(value):
    return round(value / (1024 ** 3), 2)

def metric_box(label, value, unit=""):
    return html.Div([
        html.Div(label, style={'fontWeight': 'bold', 'color': '#000', 'fontSize': '12px'}),
        html.Div(f"{value} {unit}", style={'fontSize': '14px', 'color': '#000', 'marginBottom': '8px'})
    ])

def resource_card(title, graph_id, metrics_id, color, tooltip_text=""):
    # Criar o ícone de informação (se houver tooltip)
    info_icon = html.Span(
        "ⓘ",
        id=f"info-{graph_id}",
        style={
            'marginLeft': '5px',
            'cursor': 'pointer',
            'fontSize': '14px',
            'color': color
        }
    ) if tooltip_text else None

    # Criar o conteúdo principal do card
    card_content = html.Div([
        # Cabeçalho
        html.Div([
            html.H4(title, style={
                'marginBottom': '12px',
                'textAlign': 'center',
                'color': "#000000",
                'fontSize': '22px',
                'borderBottom': f'1px solid {color}',
                'paddingBottom': '1px',
                'display': 'inline-block'
            }),
            info_icon
        ], style={'textAlign': 'center'}),
        
        # Corpo do card
        html.Div([
            dcc.Graph(
                id=graph_id,
                config={'displayModeBar': False},
                style={'height': '120px', 'width': '80%'}
            ),
            html.Div(id=metrics_id, style={
                'width': '40%',
                'paddingLeft': '10px',
                'color': "#030303",
                'fontSize': '12px',
                'display': 'flex',
                'flexDirection': 'column',
                'justifyContent': 'center'
            })
        ], style={
            'display': 'flex',
            'flexDirection': 'row',
            'justifyContent': 'space-between',
            'alignItems': 'center',
            'height': 'calc(100% - 40px)'
        })
    ], style={
        'backgroundColor': "#FFFFFF",
        'borderRadius': '8px',
        'padding': '15px',
        'boxShadow': '0 4px 8px rgba(0, 0, 0, 0.3)',
        'height': '200px',
        'weight': '200px',
        'overflow': 'hidden',
        'position': 'relative'
    })

    # Se houver tooltip, envolvemos o conteúdo com o tooltip
    if tooltip_text:
        return html.Div([
            # Tooltip primeiro (importante para a ordem de renderização)
            dcc.Tooltip(
                tooltip_text,
                id=f"tooltip-{graph_id}",
                style={
                    'backgroundColor': color,
                    'color': 'white',
                    'borderRadius': '5px',
                    'padding': '10px',
                    'maxWidth': '300px'
                },
                targetable=True  # Permite que o tooltip seja acionado por elementos filhos
            ),
            # Conteúdo do card
            card_content
        ])
    else:
        return card_content
    


import logging

def setup_logger(name='monitoramento'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.WARNING)

    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] %(message)s', datefmt='%H:%M:%S'
    )
    handler.setFormatter(formatter)

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
