import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_phillips_curve(df, country):
    df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")
    df["inflation_rate"] = pd.to_numeric(df["inflation_rate"], errors="coerce")

    df = df.dropna(subset=["unemployment_rate", "inflation_rate"])

    z = np.polyfit(df["unemployment_rate"], df["inflation_rate"], 2)
    p = np.poly1d(z)

    x = np.linspace(df["unemployment_rate"].min(), df["unemployment_rate"].max(), 100)
    trendline = p(x)

    trend_df = pd.DataFrame({"unemployment_rate": x, "inflation_rate": trendline})

    fig = px.scatter(
        df,
        x="unemployment_rate",
        y="inflation_rate",
        title=f"Phillips Curve for {country}",
        labels={
            "unemployment_rate": "Unemployment Rate (%)",
            "inflation_rate": " Inflation Rate (%)",
        },
        hover_data={"original_period": True},
        color_discrete_sequence=["darkblue"],
        width=1200,
        height=500,
    )

    fig.add_trace(
        go.Scatter(
            x=trend_df["unemployment_rate"],
            y=trend_df["inflation_rate"],
            mode="lines",
            name="Tendency",
            line=dict(color="deeppink"),
        )
    )

    return fig 

def create_phillips_example():
    np.random.seed(42)
    unemployment_rate = np.linspace(2, 10, 50)  
    inflation_rate = 15 - 1.5 * unemployment_rate + np.random.normal(0, 1, 50)

    df = pd.DataFrame({
    "Unemployment Rate (%)": unemployment_rate,
    "Inflation Rate (%)": inflation_rate
    })

    fig = go.Figure()

    fig.add_trace(go.Scatter(
    x=df["Unemployment Rate (%)"],
    y=df["Inflation Rate (%)"],
    mode='lines+markers',
    line=dict(color='gold', width=2),
    marker=dict(color='gold', size=6),
    name='Phillips Curve'
    ))

    fig.update_layout(
    title='Phillips Curve in Theory',
    xaxis_title='Unemployment Rate (%)',
    yaxis_title='Inflation Rate (%)',
    plot_bgcolor='white',
    font=dict(size=12),
    )

    return fig
