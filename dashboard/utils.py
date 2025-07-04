import random

import plotly.graph_objects as go


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
