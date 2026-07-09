import json
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# -----------------------------------------------------------------------------
# 1. CORE PARSING FUNCTION (With API Key Support)
# -----------------------------------------------------------------------------


def parse_market_json(url, api_key=None):
    try:
        # Construct headers if an API key is provided
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Attempt standard JSON parse
        return response.json()
    except json.JSONDecodeError:
        # Fallback for Python-style capitalization anomalies (e.g., ": True")
        raw_text = response.text
        fixed_text = raw_text.replace(": True", ": true").replace(
            ": False", ": false"
        )
        try:
            return json.loads(fixed_text)
        except Exception as e:
            st.error(f"Failed to parse repaired text: {e}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"An error occurred while fetching the URL: {e}")
        return None


# -----------------------------------------------------------------------------
# 2. STREAMLIT UI LAYOUT & CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Market Analytics Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Live Market Schedule Dashboard")
st.markdown(
    "Fetch, filter, and visualize real-time asset market schedules with custom API integration."
)

# --- Sidebar Configuration Panel ---
st.sidebar.header("⚙️ Configuration & Auth")

default_url = "https://s.yimg.com/uc/finance/cosaic/temporaryAssets/us_market_6.0.45.json?origin=ca.finance.yahoo.com"
url_input = st.sidebar.text_input("Data Source URL:", value=default_url)

# API Key input field (masked for security)
api_key_input = st.sidebar.text_input(
    "API Key (Optional):", type="password", help="Passes key into Bearer Headers"
)

# Real-time Refresh controls
st.sidebar.markdown("---")
st.sidebar.subheader("🔄 Live Actions")
refresh_clicked = st.sidebar.button("🔄 Refresh Live Data", type="primary")

# Initialize session state for tracking data updates dynamically
if "market_data" not in st.session_state:
    st.session_state.market_data = None

# Trigger fetch on initial app load OR when refresh button is pressed
if st.session_state.market_data is None or refresh_clicked:
    with st.spinner("Fetching live data streams..."):
        st.session_state.market_data = parse_market_json(
            url_input, api_key_input
        )
        if refresh_clicked and st.session_state.market_data:
            st.toast("Data refreshed successfully!", icon="✅")

# --- Main Dashboard Display ---
data = st.session_state.market_data

if data:
    # Metadata Metrics Card row
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

    # Rules Array Processing
    rules = data.get("rules", [])
    if rules:
        df = pd.DataFrame(rules)

        # -----------------------------------------------------------------------------
        # 3. PLOTLY VISUALIZATION COMPONENT
        # -----------------------------------------------------------------------------
        st.subheader("📈 Visual Data Analysis")

        # Map day integers to clean readable string values for graphs
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

            # Chart 1: Distribution of trading sessions by day
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

        # --- Data Presentation Tables ---
        st.subheader("🕒 Detailed Schedule Split")
        tab1, tab2, tab3 = st.tabs(
            [
                "Weekly Recurring Schedule",
                "Specific Calendar Dates / Holidays",
                "Raw JSON Stream",
            ]
        )

        with tab1:
            if "dayofweek" in df.columns:
                st.dataframe(
                    weekly_df.sort_values(by=["dayofweek", "open"]),
                    use_container_width=True,
                )
            else:
                st.info("No recurring weekly 'dayofweek' rules found.")

        with tab2:
            if "date" in df.columns:
                date_df = df[df["date"].notna()].copy()
                if not date_df.empty:
                    st.dataframe(
                        date_df.sort_values(by="date", ascending=False),
                        use_container_width=True,
                    )
                else:
                    st.info("No historical exception dates found.")
            else:
                st.info("No calendar exception dates found.")

        with tab3:
            st.json(data)
    else:
        st.warning("No operational schedules ('rules') found inside this file.")
else:
    st.info("Provide a valid configuration setup and click 'Refresh Live Data'.")
    