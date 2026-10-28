import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(
    page_title="Global Development Analytics Dashboard",
    page_icon="??",
    layout="wide",
)


@st.cache_data
def load_data() -> pd.DataFrame:
    df = px.data.gapminder()
    df["gdp"] = df["gdpPercap"] * df["pop"]
    return df


def format_number(value: float) -> str:
    if value >= 1_000_000_000_000:
        return f"{value / 1_000_000_000_000:.2f}T"
    if value >= 1_000_000_000:
        return f"{value / 1_000_000_000:.2f}B"
    if value >= 1_000_000:
        return f"{value / 1_000_000:.2f}M"
    return f"{value:,.0f}"


def main() -> None:
    st.title("Global Development Analytics Dashboard")
    st.caption(
        "BCA Final Year Project using Gapminder real-world country data (1952-2007)."
    )

    df = load_data()

    with st.sidebar:
        st.header("Filters")
        years = sorted(df["year"].unique())
        selected_year = st.selectbox("Select Year", years, index=len(years) - 1)

        continents = sorted(df["continent"].unique())
        selected_continents = st.multiselect(
            "Select Continents",
            options=continents,
            default=continents,
        )

        country_options = sorted(df["country"].unique())
        selected_countries = st.multiselect(
            "Select Countries (Optional)",
            options=country_options,
            default=[],
        )

    filtered_df = df[df["continent"].isin(selected_continents)]
    if selected_countries:
        filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

    year_df = filtered_df[filtered_df["year"] == selected_year]

    total_population = year_df["pop"].sum()
    weighted_life_exp = np.average(year_df["lifeExp"], weights=year_df["pop"])
    weighted_gdp_per_capita = np.average(year_df["gdpPercap"], weights=year_df["pop"])
    total_gdp = year_df["gdp"].sum()

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Countries", f"{year_df['country'].nunique()}")
    c2.metric("Population", format_number(total_population))
    c3.metric("Avg Life Expectancy", f"{weighted_life_exp:.1f} years")
    c4.metric("Avg GDP/Capita", f"${weighted_gdp_per_capita:,.0f}")

    st.markdown("---")

    left, right = st.columns(2)

    with left:
        st.subheader("GDP Per Capita vs Life Expectancy")
        scatter = px.scatter(
            year_df,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            size_max=45,
            log_x=True,
            labels={
                "gdpPercap": "GDP Per Capita (log scale)",
                "lifeExp": "Life Expectancy",
            },
        )
        st.plotly_chart(scatter, use_container_width=True)

    with right:
        st.subheader("Population Share by Continent")
        continent_pop = (
            year_df.groupby("continent", as_index=False)["pop"].sum().sort_values("pop")
        )
        bar = px.bar(
            continent_pop,
            x="pop",
            y="continent",
            orientation="h",
            text_auto=".2s",
            labels={"pop": "Population", "continent": "Continent"},
            color="continent",
        )
        bar.update_layout(showlegend=False)
        st.plotly_chart(bar, use_container_width=True)

    t1, t2 = st.columns(2)

    with t1:
        st.subheader("Life Expectancy Trend")
        trend_life = (
            filtered_df.groupby("year")
            .apply(lambda x: np.average(x["lifeExp"], weights=x["pop"]))
            .reset_index()
            .rename(columns={0: "weighted_lifeExp"})
        )
        fig_life = px.line(
            trend_life,
            x="year",
            y="weighted_lifeExp",
            markers=True,
            labels={"weighted_lifeExp": "Weighted Life Expectancy"},
        )
        st.plotly_chart(fig_life, use_container_width=True)

    with t2:
        st.subheader("GDP Trend")
        trend_gdp = filtered_df.groupby("year", as_index=False)["gdp"].sum()
        fig_gdp = px.area(
            trend_gdp,
            x="year",
            y="gdp",
            labels={"gdp": "Total GDP"},
        )
        fig_gdp.update_yaxes(tickprefix="$", separatethousands=True)
        st.plotly_chart(fig_gdp, use_container_width=True)

    st.subheader("World Map: GDP Per Capita")
    map_fig = px.choropleth(
        year_df,
        locations="iso_alpha",
        color="gdpPercap",
        hover_name="country",
        color_continuous_scale="Viridis",
        labels={"gdpPercap": "GDP/Capita"},
    )
    st.plotly_chart(map_fig, use_container_width=True)

    st.subheader("Top 10 Countries by Total GDP")
    top_10 = year_df.sort_values("gdp", ascending=False).head(10)
    fig_top = px.bar(
        top_10,
        x="country",
        y="gdp",
        color="continent",
        labels={"gdp": "Total GDP", "country": "Country"},
        text_auto=".2s",
    )
    fig_top.update_yaxes(tickprefix="$", separatethousands=True)
    st.plotly_chart(fig_top, use_container_width=True)

    st.subheader("Filtered Data Table")
    display_df = year_df[["country", "continent", "year", "lifeExp", "pop", "gdpPercap", "gdp"]]
    st.dataframe(display_df.sort_values("gdp", ascending=False), use_container_width=True)

    st.download_button(
        label="Download Filtered Data (CSV)",
        data=display_df.to_csv(index=False).encode("utf-8"),
        file_name=f"gapminder_filtered_{selected_year}.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.info(
        f"Estimated total GDP in selected view: ${format_number(total_gdp)} | "
        f"Records shown: {len(display_df)}"
    )


if __name__ == "__main__":
    main()
