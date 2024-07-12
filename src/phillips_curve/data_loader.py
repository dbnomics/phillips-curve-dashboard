import pandas as pd
from dbnomics import fetch_series


def load_data(country):
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

    col_em = ["original_period", "Reference area", "original_value"]
    col_inf = ["original_period", "WEO Country", "original_value"]

    country_map = {
        "France": ("FRA", "France"),
        "United States": ("USA", "United States"),
        "Argentina": ("ARG", "Argentina"),
        "Japan": ("JPN", "Japan"),
    }

    employ_code, infla_code = country_map[country]

    df_employ_country = df_employ[df_employ["Reference area"] == country][
        col_em
    ].rename(columns={"original_value": "unemployment_rate"})
    df_infla_country = df_infla[df_infla["WEO Country"] == country][col_inf].rename(
        columns={"original_value": "inflation_rate"}
    )

    df_country = pd.merge(
        df_employ_country, df_infla_country, on="original_period"
    ).drop(columns=["WEO Country"])

    return df_country
