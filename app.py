import os
import json
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from bs4 import BeautifulSoup


# Streamlit layout and config

st.set_page_config(
    page_title="Market Analytics Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Live Market Schedule Dashboard")
st.markdown(
    "Fetch, filter, and visualize real-time asset market schedules with custom API integration."
)


# Sidebar
st.sidebar.header("⚙️ Data Source Selection")

# Toggle between URL or local file data
source_type = st.sidebar.radio(
    "Choose Data Input Source:", ("Remote URL API", "Local System File", "HTML Data Scraper")
)

# Render inputs based on toggle choice
if source_type == "Remote URL API":
    default_url = "https://"#"https://s.yimg.com/uc/finance/cosaic/temporaryAssets/us_market_6.0.45.json?origin=ca.finance.yahoo.com"
    url_input = st.sidebar.text_input("Data Source URL:", value=default_url)
    api_key_input = st.sidebar.text_input(
        "API Key (Optional):", type="password"
    )
elif source_type == "Local System File":
    # Set default to look for local json file in project directory
    file_input = st.sidebar.text_input(
        "File Name or Full System Path:", value="us_market.json"
    )
else:
    default_scrape_url = (
        "https://"#https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
    )
    scrape_url_input = st.sidebar.text_input(
        "Target Website URL to Scrape:", value=default_scrape_url
    )

# Refresh button
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Live Actions")
refresh_clicked = st.sidebar.button("🔄 Sync & Refresh Data", type="primary")

# Initialize session state
if "market_data" not in st.session_state:
    st.session_state.market_data = None

# Load via URL vs local file
if st.session_state.market_data is None or refresh_clicked:
    with st.spinner("Processing data stream target..."):
        if source_type == "Remote URL API":
            st.session_state.market_data = parse_market_json(
                url_input, api_key_input
            )
        elif source_type == "Local System File":
            st.session_state.market_data = read_contents(file_input)
        else:
            st.session_state.market_data = scrape_html_tables(scrape_url_input)

        if refresh_clicked and st.session_state.market_data:
            st.toast("Dashboard layout synchronized!", icon="✅")


# Main dashboard
data = st.session_state.market_data

if data:
    
    if (isinstance(data, list)
        and len(data) > 0
        and isinstance(data[0], pd.DataFrame)):
        # If data is HTML scraped data
        st.subheader("🌐 Scraped HTML Data Tables")
        st.info(f"Successfully scraped **{len(data)}** table(s) from the page.")

        # Let the user pick which table to inspect if multiple exist
        selected_table_idx = st.selectbox(
            "Select Scraped Table to View:",
            options=range(len(data)),
            format_func=lambda x: f"Table #{x + 1} ({data[x].shape[0]} rows × {data[x].shape[1]} cols)",
        )

        scraped_df = data[selected_table_idx]
        st.dataframe(scraped_df, use_container_width=True)

        # Download button for the scraped table
        csv = scraped_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 Download Table as CSV",
            data=csv,
            file_name=f"scraped_table_{selected_table_idx + 1}.csv",
            mime="text/csv",
        )

    elif isinstance(data, list):
        # If data is list, convert to pandas dataframe
        st.subheader("📋 Tabular Dataset Preview")
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        # Show raw JSON breakdown
        st.subheader("📁 Raw JSON Stream")
        st.json(data)

    elif isinstance(data, dict):
        # If data is dictionary
        st.subheader("📋 Market Metadata")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="Market Name", value=data.get("name", "N/A").upper())
        with col2:
            st.metric(label="Market Timezone", value=data.get("market_tz", "N/A"))
        with col3:
            st.metric(
                label="Hours Aligned Status",
                value=str(data.get("hours_aligned", "N/A")),
            )

        st.markdown("---")

        # Interactive plots processing
        rules = data.get("rules", [])
        if rules:
            df = pd.DataFrame(rules)

            st.subheader("📈 Visual Data Analysis")
            day_map = {
                1: "Monday",
                2: "Tuesday",
                3: "Wednesday",
                4: "Thursday",
                5: "Friday",
                6: "Saturday",
                7: "Sunday",
            }

            if "dayofweek" in df.columns:
                weekly_df = df[df["dayofweek"].notna()].copy()
                weekly_df["day_name"] = weekly_df["dayofweek"].map(day_map)
                weekly_df["name"] = weekly_df["name"].fillna("regular")

                g1, g2 = st.columns(2)
                with g1:
                    st.markdown("#### Trading Sessions Active per Weekday")
                    fig_bar = px.bar(
                        weekly_df,
                        x="day_name",
                        color="name",
                        title="Trading Windows by Day of Week",
                        labels={"day_name": "Day of Week", "name": "Session Type"},
                        barmode="group",
                        color_discrete_sequence=px.colors.qualitative.Pastel,
                    )
                    fig_bar.update_layout(xaxis={"categoryorder": "array", "categoryarray": list(day_map.values())})
                    st.plotly_chart(fig_bar, use_container_width=True)

                with g2:
                    st.markdown("#### Market Session Breakdown Proportion")
                    fig_pie = px.pie(
                        weekly_df,
                        names="name",
                        title="Proportion of Session Allocations",
                        hole=0.4,
                        color_discrete_sequence=px.colors.qualitative.Safe,
                    )
                    st.plotly_chart(fig_pie, use_container_width=True)

            st.markdown("---")

            # Tab Sheets
            st.subheader("🕒 Detailed Schedule Split")
            tab1, tab2, tab3 = st.tabs(
                [
                    "Weekly Recurring Schedule",
                    "Specific Calendar Dates / Holidays",
                    "Raw Data Payload View",
                ]
            )

            with tab1:
                if "dayofweek" in df.columns:
                    st.dataframe(
                        weekly_df.sort_values(by=["dayofweek", "open"]),
                        use_container_width=True,
                    )
                else:
                    st.info("No recurring weekly schedule segments present.")

            with tab2:
                if "date" in df.columns:
                    date_df = df[df["date"].notna()].copy()
                    if not date_df.empty:
                        st.dataframe(
                            date_df.sort_values(by="date", ascending=False),
                            use_container_width=True,
                        )
                    else:
                        st.info("No localized date exceptions found.")
                else:
                    st.info("No specific operational calendar filters found.")

            with tab3:
                st.json(data)
        else:
            st.warning("JSON parsed successfully, but structural rules are empty.")

else:
    st.info(
        "Select an option on the sidebar panel to load the layout visualizations."
    )
