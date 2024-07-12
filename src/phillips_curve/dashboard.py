import importlib.resources

import streamlit as st
from charts import create_phillips_curve, create_phillips_example
from data_loader import load_data
from streamlit_option_menu import option_menu

package_dir = importlib.resources.files("phillips_curve")


def main() -> None:
    st.set_page_config(
        page_title="Phillips curve dashboard with DBnomics data",
        page_icon=str(package_dir / "images/favicon.png"),
    )

    st.image(str(package_dir / "images/dbnomics.svg"), width=300)
    # Interface Streamlit
    st.title(":blue[Phillips Curve]")

    def local_css(file_name):
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    local_css(package_dir / "assets/styles.css")

    st.markdown(
        """
        <style>
        hr {
            height: 1px;
            border: none;
            color: #333;
            background-color: #333;
            margin-top: 3px;
            margin-bottom: 3px;
        }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("---")

    with st.sidebar:
        selected = option_menu(
            menu_title="Menu",
            options=[
                "Explanations",
                "Phillips Curve Charts",
                "Sources",
            ],
            icons=["book", "bar-chart", "search"],
            menu_icon=":",
            default_index=0,
        )

    if selected == "Explanations":
        st.subheader(":blue[**Explanations**]")
        st.write(
            "\n"
            "The Phillips curve highlights an inverse relationship between the unemployment rate and inflation.\n"
        )

        #Plot Fake Phillips Curve 

        fig = create_phillips_example()
        st.plotly_chart(fig)

        st.write(
            "This relationship was demonstrated by the New Zealand economist Alban William Phillips in 1958 in \"The relation between unemployment and the rate of change of money wage rates in the United Kingdom, 1861-1957\".\n"
            "Originally, it was not (price) inflation that William Phillips chose, but wage inflation. He based his analysis on the observation of changes in nominal wages in Great Britain from 1861 to 1957.\n"
            "William Phillips argued that economic growth leads to inflation, which in turn leads to a decrease in the unemployment rate.\n"
            "\n"
            "During periods of economic growth, with a low unemployment rate, the balance of power is in favor of employees.\n"
            "Competition between companies pushes them to increase wages, which in turn raises the prices of their products.\n"
            "Conversely, in periods of high unemployment, the balance of power is in the hands of businesses, which can lower wages.\n"
            "Employees must forgo wage increases, leading to disinflation.\n"
            "\n"
            "This curve, by representing this negative relationship, becomes one of the most important in macroeconomic analysis.\n"
            "It plays a considerable role in the choices of economic policies: central banks can make a trade-off between inflation and unemployment.\n"
            "\n"
            "However, since the 1970s, the Phillips curve has been challenged.\n"
            "First, the phenomenon of stagflation (stagnation of economic activity, high unemployment, and rising inflation) shifted the Phillips curve to the right, meaning that high inflation and economic crisis coexisted.\n"
            "Then, since the 1990s, and especially since the Great Recession, a flattening of the Phillips curve has occurred.\n"
            "This means that achieving the same decrease of inflation as before requires a stronger increase of unemployment.\n"
        )

    if selected == "Phillips Curve Charts":
        countries = st.multiselect(
            "**Select Country**",
            ["France", "United States", "Argentina", "Japan"],
            default=["France"],
        )
        if countries:
            for country in countries:
                df_country = load_data(country)
                fig_country = create_phillips_curve(df_country, country)
                st.plotly_chart(fig_country)

    if selected == "Sources":
        st.subheader("**Data**")
        st.write(
            "- [Unemployment rate](https://db.nomics.world/ILO/UNE_DEAP_SEX_AGE_EDU_RT?tab=list)\n"
            "\n"
            "- [Inflation rate](https://db.nomics.world/IMF/WEO:2024-04?tab=list)\n"
        )
        st.markdown("---")
        st.write("[Source Code](https://github.com/dbnomics/phillips-curve-dashboard)")
        st.write("[DBnomics](https://db.nomics.world)")


if __name__ == "__main__":
    main()
