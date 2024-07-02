import importlib.resources

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import streamlit as st
from dbnomics import fetch_series

package_dir = importlib.resources.files("phillips_curve")

# thème des graphiques
pio.templates.default = "ggplot2"


# Fonction pour créer une courbe de Phillips avec tendance
def create_phillips_curve(df, country):
    # Convertir les colonnes en float64
    df["unemployment_rate"] = pd.to_numeric(df["unemployment_rate"], errors="coerce")
    df["inflation_rate"] = pd.to_numeric(df["inflation_rate"], errors="coerce")

    # Supprimer les lignes contenant des valeurs NA
    df = df.dropna(subset=["unemployment_rate", "inflation_rate"])

    # Ajuster une courbe polynomiale (degré 2) pour la tendance
    z = np.polyfit(df["unemployment_rate"], df["inflation_rate"], 2)
    p = np.poly1d(z)

    # Créer une gamme de valeurs pour tracer la courbe de tendance
    x = np.linspace(df["unemployment_rate"].min(), df["unemployment_rate"].max(), 100)
    trendline = p(x)

    # Créer un DataFrame pour la courbe de tendance
    trend_df = pd.DataFrame({"unemployment_rate": x, "inflation_rate": trendline})

    # Créer le graphique
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


# Chargement des données
df_employ = fetch_series(
    [
        "ILO/UNE_DEAP_SEX_AGE_EDU_RT/USA.BA_453.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A",
        "ILO/UNE_DEAP_SEX_AGE_EDU_RT/FRA.BA_148.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A",
        "ILO/UNE_DEAP_SEX_AGE_EDU_RT/ARG.BA_150.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A",
        "ILO/UNE_DEAP_SEX_AGE_EDU_RT/JPN.BA_259.AGE_YTHADULT_YGE15.EDU_AGGREGATE_TOTAL.SEX_T.A",
    ]
)

df_infla = fetch_series(
    [
        "IMF/WEO:2024-04/USA.PCPIPCH.pcent_change",
        "IMF/WEO:2024-04/FRA.PCPIPCH.pcent_change",
        "IMF/WEO:2024-04/ARG.PCPIPCH.pcent_change",
        "IMF/WEO:2024-04/JPN.PCPIPCH.pcent_change",
    ]
)

# Sélectionner les colonnes d'intérêt
col_em = ["original_period", "Reference area", "original_value"]
col_inf = ["original_period", "WEO Country", "original_value"]

# Créer des DataFrames pour chaque pays
df_employ_fr = df_employ[df_employ["Reference area"] == "France"][col_em].rename(
    columns={"original_value": "unemployment_rate"}
)
df_employ_us = df_employ[df_employ["Reference area"] == "United States"][col_em].rename(
    columns={"original_value": "unemployment_rate"}
)
df_employ_ar = df_employ[df_employ["Reference area"] == "Argentina"][col_em].rename(
    columns={"original_value": "unemployment_rate"}
)
df_employ_jp = df_employ[df_employ["Reference area"] == "Japan"][col_em].rename(
    columns={"original_value": "unemployment_rate"}
)

df_infla_fr = df_infla[df_infla["WEO Country"] == "France"][col_inf].rename(
    columns={"original_value": "inflation_rate"}
)
df_infla_us = df_infla[df_infla["WEO Country"] == "United States"][col_inf].rename(
    columns={"original_value": "inflation_rate"}
)
df_infla_ar = df_infla[df_infla["WEO Country"] == "Argentina"][col_inf].rename(
    columns={"original_value": "inflation_rate"}
)
df_infla_jp = df_infla[df_infla["WEO Country"] == "Japan"][col_inf].rename(
    columns={"original_value": "inflation_rate"}
)

# Merger les données par Pays
df_fr = pd.merge(df_employ_fr, df_infla_fr, on="original_period").drop(
    columns=["WEO Country"]
)
df_us = pd.merge(df_employ_us, df_infla_us, on="original_period").drop(
    columns=["WEO Country"]
)
df_ar = pd.merge(df_employ_ar, df_infla_ar, on="original_period").drop(
    columns=["WEO Country"]
)
df_jp = pd.merge(df_employ_jp, df_infla_jp, on="original_period").drop(
    columns=["WEO Country"]
)

# Créer les graphiques
fig_fr = create_phillips_curve(df_fr, "France")
fig_us = create_phillips_curve(df_us, "United States")
fig_ar = create_phillips_curve(df_ar, "Argentina")
fig_jp = create_phillips_curve(df_jp, "Japan")

st.set_page_config(
    page_title="Phillips curve dashboard with DBnomics data",
    page_icon=str(package_dir / "images/favicon.png"),
)


# logo DBnomics
st.image(str(package_dir / "dbnomics.svg"), width=300)
# Interface Streamlit
st.title(":blue[Phillips Curve]")
st.subheader(":blue[**Explanations**]")
st.write(
    "\n"
    "The Phillips curve highlights an inverse relationship between the unemployment rate and inflation.\n"
    'This relationship was demonstrated by the New Zealand economist Alban William Phillips in 1958 in "The relation between unemployment and the rate of change of money wage rates in the United Kingdom, 1861-1957.\n'
    '" Originally, it was not inflation that William Phillips chose, but the year-over-year increase in wages. He based his analysis on the observation of changes in nominal wages in Great Britain from 1861 to 1957.\n'
    "William Phillips argued that economic growth leads to inflation, which in turn leads to a decrease in the unemployment rate.\n"
    "\n"
    "During periods of economic growth, with a low unemployment rate, the balance of power is in favor of employees.\n"
    "Competition between companies pushes them to increase wages, which in turn raises the prices of their products.\n"
    "Conversely, in periods of high unemployment, the balance of power is in the hands of businesses, which can lower wages.\n"
    "Employees must forgo wage increases, leading to disinflation.\n"
    "\n"
    "This curve, by representing this negative relationship, becomes one of the most important in macroeconomic analysis.\n"
    "It plays a considerable role in the choices of economic policies: states can make a trade-off between inflation and unemployment.\n"
    "\n"
    "However, since the 1970s, the phenomenon of stagflation (stagnation of economic activity, high unemployment, and rising inflation) has challenged the Phillips curve.\n"
    "High inflation and economic crisis have coexisted.\n"
    "The relationship between inflation and unemployment has become *positive*.\n"
    "This is reflected in a flattening of the Phillips curves.\n"
)

st.markdown("---")
# Options de sélection des pays
countries = st.multiselect(
    "**Select Country**",
    ["France", "United States", "Argentina", "Japan"],
    default=["France"],
)

# Afficher les graphiques sélectionnés
if "France" in countries:
    st.plotly_chart(fig_fr)

if "United States" in countries:
    st.plotly_chart(fig_us)

if "Argentina" in countries:
    st.plotly_chart(fig_ar)

if "Japan" in countries:
    st.plotly_chart(fig_jp)
# Les sources des données
st.write(":blue[**DBnomics**] **sources**.")
st.write(
    "Unemployment rate : [*link*](https://db.nomics.world/ILO/UNE_DEAP_SEX_AGE_EDU_RT?tab=list)"
)
st.write("Inflation rate : [*link*](https://db.nomics.world/IMF/WEO:2024-04?tab=list)")
