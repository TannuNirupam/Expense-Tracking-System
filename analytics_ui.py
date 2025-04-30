import streamlit as st
from datetime import datetime
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://localhost:8000"

def analytics_tab():
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", datetime(2024, 8, 1))
    with col2:
        end_date = st.date_input("End Date", datetime(2024, 8, 5))

    if st.button("Get Analytics"):
        # Define payload inside the button's block
        payload = {
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d")
        }

        try:
            # Send request with the payload
            response = requests.post(f"{API_URL}/analytics", json=payload)

            if response.status_code == 200:
                result = response.json()

                # Extract the breakdown data
                breakdown = result.get("breakdown", {})

                # If breakdown data is empty or missing, show a message
                if not breakdown:
                    st.warning("No analytics data available for the selected date range.")
                    return

                # Prepare data for the table
                data = {
                    "Category": [],
                    "Total": [],
                    "Percentage": []
                }

                # Loop through the breakdown and fill the table data
                for category, values in breakdown.items():
                    data["Category"].append(category)
                    data["Total"].append(values["total"])
                    data["Percentage"].append(values["percentage"])

                # Convert the data to a DataFrame
                df = pd.DataFrame(data)

                # Display the final table
                st.table(df)

                # Plotting the bar chart
                fig, ax = plt.subplots(figsize=(10, 6))
                ax.bar(df['Category'], df['Total'], color='skyblue')

                # Set labels and title
                ax.set_xlabel('Category')
                ax.set_ylabel('Total Amount')
                ax.set_title('Expense Breakdown by Category')

                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45, ha='right')

                # Display the chart
                st.pyplot(fig)

            else:
                st.error(f"Failed to fetch analytics data: {response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
