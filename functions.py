import os
import json
import pandas as pd
import plotly.express as px
import requests
import streamlit as st
from bs4 import BeautifulSoup


# File reading function

def read_contents(file_path):

    # Check if path exists
    if os.path.exists(file_path):
        try:
            # Read file contents
            with open(file_path, "r") as file:
                contents = file.read()

            # Standardise Python/JS boolean capitalization
            fixed_contents = contents.replace(": True", ": true").replace(
                ": False", ": false"
            )

            # Convert text into Python dictionary/JSON object
            return json.loads(fixed_contents)

        except Exception as e:
            st.error(f"Error reading or parsing local file: {e}")
            return None
        
    # If no path exists
    else:
        st.error(f"File path does not exist: {file_path}")
        return None
    

# Parsing function

def parse_market_json(url, api_key=None):
    # Attempt standard JSON parse
    try:
        # Construct headers if an API key is provided
        headers = {}
        if api_key:
            headers = {"Authorization": f"Bearer {api_key}"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        
        return response.json()
    
    except json.JSONDecodeError:
        # Standardise boolean capitalization
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


# Beatifulsoup HTML data scraper

def scrape_html_tables(url):
    """Scrapes raw HTML from a target web page and extracts all <table> elements

    into a list of Pandas DataFrames using BeautifulSoup.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/115.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Parse raw HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, "lxml")
        tables = soup.find_all("table")

        if not tables:
            st.warning("No HTML <table> elements were found on this web page.")
            return None

        # Convert each BeautifulSoup <table> tag into a Pandas DataFrame
        scraped_dfs = []
        for index, table in enumerate(tables):
            try:
                # pd.read_html can take the string representation of a BS4 table
                df_list = pd.read_html(str(table))
                if df_list:
                    scraped_dfs.append(df_list[0])
            except Exception:
                continue

        return scraped_dfs if scraped_dfs else None

    except requests.exceptions.RequestException as e:
        st.error(f"Failed to scrape website: {e}")
        return None

