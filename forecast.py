#                               rule-based growth model with random fluctuations

# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from page.db import get_connection

# def fetch_data(): 
#     """Fetch total monthly volume data from table"""
#     connection = get_connection()
#     query = """
#         SELECT 
#             DATE_FORMAT(timestamp, '%Y-%m') AS month, 
#             COUNT(*) AS volume
#         FROM admin_database
#         WHERE timestamp IS NOT NULL
#         GROUP BY DATE_FORMAT(timestamp, '%Y-%m')
#         ORDER BY month;  
#     """
#     try:
#         df = pd.read_sql(query, connection)
#         connection.close()

#         # Convert month column to datetime format
#         df['month'] = pd.to_datetime(df['month'])
#         return df
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
#         return pd.DataFrame()

# def forecast_with_growth(data, periods=11, growth_rate=0.05, fluctuation_range=(-0.1, 0.1)): 
#     """Forecast volume with a fixed growth rate and random fluctuation."""
#     last_value = data.iloc[-1]
#     forecast = []
    
#     for i in range(1, periods + 1):
#         growth_factor = (1 + growth_rate) + np.random.uniform(*fluctuation_range)  # Fluctuation added
#         forecast.append(last_value * (growth_factor ** i))
    
#     forecast_index = [data.index[-1] + pd.DateOffset(months=i) for i in range(1, periods + 1)]
    
#     return pd.Series(forecast, index=forecast_index)

# def forecast_page():
#     st.title("Total Volume Forecasting")

#     data = fetch_data()
#     if data.empty:
#         st.warning("⚠ No data available.")
#         return

#     # Display historical data
#     st.subheader(" Historical Monthly Data")
#     data['month_name'] = data['month'].dt.strftime('%B')  
#     data.reset_index(drop=True, inplace=True)
#     data.index += 1  
#     st.dataframe(data[['month_name', 'volume']])  

#     data.set_index('month', inplace=True)
#     actual_series = data['volume']

#     if 'forecast_series' not in st.session_state:
#         # Compute forecast only once and store it
#         st.session_state.forecast_series = forecast_with_growth(actual_series, periods=11, growth_rate=0.05)

#     forecast_series = st.session_state.forecast_series  # Use cached forecast data

#     st.subheader("Forecast for Next 6 Months")

#     # Convert forecast index to datetime format
#     forecast_series.index = pd.to_datetime(forecast_series.index)

#     # Combine actual and forecasted data
#     full_data = pd.concat([actual_series, forecast_series])
#     full_df = pd.DataFrame({'Month': full_data.index.strftime('%B'), 'Volume': full_data.values})

#     # Plot using Plotly
#     fig = px.line(full_df, x='Month', y='Volume', markers=True, title="Monthly Volume Forecast")
#     fig.update_layout(yaxis=dict(range=[0, full_data.max() * 1.1]))  
#     st.plotly_chart(fig)

#     # Button to show forecast table
#     if st.button('Show Table'):
#         forecast_df = pd.DataFrame({
#             'Month': forecast_series.index.strftime('%B'),
#             'Forecast Volume': forecast_series.values.astype(int)
#         })
#         forecast_df.index += 1  
#         st.dataframe(forecast_df)

# if __name__ == "__main__":
#     forecast_page()

#--------------------------------------------------------------------------------------------------------
#                                         Updated code

#  import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from page.db import get_connection

# def fetch_data(): 
#     """Fetch total monthly volume data from table"""
#     connection = get_connection()
#     query = """
#         SELECT 
#             DATE_FORMAT(timestamp, '%Y-%m') AS month, 
#             COUNT(*) AS volume
#         FROM admin_database
#         WHERE timestamp IS NOT NULL
#         GROUP BY DATE_FORMAT(timestamp, '%Y-%m')
#         ORDER BY month;  
#     """
#     try:
#         df = pd.read_sql(query, connection)
#         connection.close()

#         df['month'] = pd.to_datetime(df['month'])
#         return df
#     except Exception as e:
#         st.error(f"Error fetching data: {e}")
#         return pd.DataFrame()

# def forecast_with_growth(data, periods=11, growth_rate=0.05, fluctuation_range=(-0.1, 0.1)): 
#     """Forecast volume with a fixed growth rate and random fluctuation."""
#     last_value = data.iloc[-1]
#     forecast = []
    
#     for i in range(1, periods + 1):
#         growth_factor = (1 + growth_rate) + np.random.uniform(*fluctuation_range)  
#         forecast.append(last_value * (growth_factor ** i))
    
#     forecast_index = [data.index[-1] + pd.DateOffset(months=i) for i in range(1, periods + 1)]
    
#     return pd.Series(forecast, index=forecast_index)

# def generate_daily_forecast(monthly_forecast):
#     """Generate daily forecast ensuring total matches the monthly forecast"""
#     daily_data = []
#     for month, volume in monthly_forecast.items():
#         days_in_month = (month + pd.DateOffset(months=1)).replace(day=1) - month
#         base_daily_volume = volume / days_in_month.days  

#         adjusted_volumes = []
#         for day in range(1, days_in_month.days + 1):
#             date = month.replace(day=day)
#             fluctuation = np.random.uniform(-0.1, 0.1)  
#             adjusted_volume = base_daily_volume * (1 + fluctuation)

#             if date.weekday() in [5, 6]:  # Reduce weekend volume
#                 adjusted_volume *= 0.8  

#             adjusted_volumes.append(adjusted_volume)

#         # Normalize values to match the monthly total exactly
#         scale_factor = volume / sum(adjusted_volumes)
#         adjusted_volumes = [int(v * scale_factor) for v in adjusted_volumes]

#         for day, adjusted_volume in zip(range(1, days_in_month.days + 1), adjusted_volumes):
#             daily_data.append({'Date': pd.to_datetime(month.replace(day=day)), 'Forecast Volume': adjusted_volume})

#     return pd.DataFrame(daily_data)


# def forecast_page():
#     st.title("Total Volume Forecasting")

#     data = fetch_data()
#     if data.empty:
#         st.warning("⚠ No data available.")
#         return

#     st.subheader("📅 Historical Monthly Data")
#     data['month_name'] = data['month'].dt.strftime('%B')  
#     data.reset_index(drop=True, inplace=True)
#     data.index += 1  

#     if st.button("Show Monthly Table"):
#         st.dataframe(data[['month_name', 'volume']])
#         total_volume = data['volume'].sum()
#         st.success(f" **Total Monthly Volume:** {total_volume:,}")  

#     data.set_index('month', inplace=True)
#     actual_series = data['volume']

#     if 'forecast_series' not in st.session_state:
#         st.session_state.forecast_series = forecast_with_growth(actual_series, periods=11, growth_rate=0.05)

#     forecast_series = st.session_state.forecast_series  

#     st.subheader("Forecast for Next 12 Months")

#     forecast_series.index = pd.to_datetime(forecast_series.index)

#     full_data = pd.concat([actual_series, forecast_series])
#     full_df = pd.DataFrame({'Month': full_data.index.strftime('%B'), 'Volume': full_data.values})

#     fig = px.line(full_df, x='Month', y='Volume', markers=True, title="Monthly Volume Forecast")
#     fig.update_layout(yaxis=dict(range=[0, full_data.max() * 1.1]))  
#     st.plotly_chart(fig)

#     if 'daily_forecast' not in st.session_state:
#         st.session_state.daily_forecast = generate_daily_forecast(forecast_series)

#     st.subheader("📆 Show Daily Forecast Table")

#     months_available = st.session_state.daily_forecast['Date'].dt.strftime('%B').unique()
#     selected_month = st.selectbox("Select a Month", months_available)

#     if st.button("Show Daily Table"):
#             filtered_data = st.session_state.daily_forecast[
#                 st.session_state.daily_forecast['Date'].dt.strftime('%B') == selected_month
#             ].copy()
#             filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
#             filtered_data.reset_index(drop=True, inplace=True)  # Reset index
#             filtered_data.index += 1  # Start index from 1

#             st.dataframe(filtered_data)
            
#             total_daily_volume = filtered_data['Forecast Volume'].sum()
#             st.success(f"**Total Forecast Volume for {selected_month}:** {total_daily_volume:,}")
        

# if __name__ == "__main__":
#     forecast_page()

#------------------------------------------------------------------------------------------------------------
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from page.db import get_connection

def fetch_data(): 
    """Fetch total monthly volume data from table"""
    connection = get_connection()
    query = """
        SELECT 
            DATE_FORMAT(timestamp, '%Y-%m') AS month, 
            COUNT(*) AS volume
        FROM admin_database
        WHERE timestamp IS NOT NULL
        GROUP BY DATE_FORMAT(timestamp, '%Y-%m')
        ORDER BY month;  
    """
    try:
        df = pd.read_sql(query, connection)
        connection.close()

        df['month'] = pd.to_datetime(df['month'])
        return df
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return pd.DataFrame()

def forecast_with_growth(data, periods=11, growth_rate=0.05, fluctuation_range=(-0.1, 0.1)): 
    """Forecast volume with a fixed growth rate and random fluctuation."""
    last_value = data.iloc[-1]
    forecast = []
    
    for i in range(1, periods + 1):
        growth_factor = (1 + growth_rate) + np.random.uniform(*fluctuation_range)  
        forecast.append(last_value * (growth_factor ** i))
    
    forecast_index = [data.index[-1] + pd.DateOffset(months=i) for i in range(1, periods + 1)]
    
    return pd.Series(forecast, index=forecast_index)

def generate_daily_forecast(monthly_forecast):
    """Generate daily forecast ensuring total matches the monthly forecast"""
    daily_data = []
    for month, volume in monthly_forecast.items():
        days_in_month = (month + pd.DateOffset(months=1)).replace(day=1) - month
        base_daily_volume = volume / days_in_month.days  

        adjusted_volumes = []
        for day in range(1, days_in_month.days + 1):
            date = month.replace(day=day)
            fluctuation = np.random.uniform(-0.1, 0.1)  
            adjusted_volume = base_daily_volume * (1 + fluctuation)

            if date.weekday() in [5, 6]:  # Reduce weekend volume
                adjusted_volume *= 0.8  

            adjusted_volumes.append(adjusted_volume)

        # Normalize values to match the monthly total exactly
        scale_factor = volume / sum(adjusted_volumes)
        adjusted_volumes = [int(v * scale_factor) for v in adjusted_volumes]

        for day, adjusted_volume in zip(range(1, days_in_month.days + 1), adjusted_volumes):
            daily_data.append({'Date': pd.to_datetime(month.replace(day=day)), 'Forecast Volume': adjusted_volume})

    return pd.DataFrame(daily_data)


def forecast_page():
    st.title("Total Volume Forecasting")

    data = fetch_data()
    if data.empty:
        st.warning("⚠ No data available.")
        return

    st.subheader("📅 Historical Monthly Data")
    data['month_name'] = data['month'].dt.strftime('%B')  
    data.reset_index(drop=True, inplace=True)
    data.index += 1  

    if st.button("Show Monthly Table"):
        st.dataframe(data[['month_name', 'volume']])
        total_volume = data['volume'].sum()
        st.success(f" **Total Monthly Volume:** {total_volume:,}")  

    data.set_index('month', inplace=True)
    actual_series = data['volume']

    if 'forecast_series' not in st.session_state:
        st.session_state.forecast_series = forecast_with_growth(actual_series, periods=11, growth_rate=0.05)

    forecast_series = st.session_state.forecast_series  

    st.subheader("Forecast for Next 12 Months")

    forecast_series.index = pd.to_datetime(forecast_series.index)

    full_data = pd.concat([actual_series, forecast_series])
    full_df = pd.DataFrame({'Month': full_data.index.strftime('%B'), 'Volume': full_data.values})

    fig = px.line(full_df, x='Month', y='Volume', markers=True, title="Monthly Volume Forecast")
    fig.update_layout(yaxis=dict(range=[0, full_data.max() * 1.1]))  
    st.plotly_chart(fig)

    if 'daily_forecast' not in st.session_state:
        st.session_state.daily_forecast = generate_daily_forecast(forecast_series)

    st.subheader("📆 Show Daily Forecast Table")

    months_available = st.session_state.daily_forecast['Date'].dt.strftime('%B').unique()
    selected_month = st.selectbox("Select a Month", months_available)

    if st.button("Show Daily Table"):
        filtered_data = st.session_state.daily_forecast[
            st.session_state.daily_forecast['Date'].dt.strftime('%B') == selected_month
        ].copy()

        filtered_data['Date'] = filtered_data['Date'].dt.strftime('%Y-%m-%d')
        filtered_data.reset_index(drop=True, inplace=True)  # Reset index
        filtered_data.index += 1  # Start index from 1

        st.dataframe(filtered_data)

        total_daily_volume = filtered_data['Forecast Volume'].sum()
        st.success(f"**Total Forecast Volume for {selected_month}:** {total_daily_volume:,}")

        # 🔹 Plot Daily Forecast Chart
        st.subheader(f"📊 Daily Forecast Chart for {selected_month}")
        daily_fig = px.line(filtered_data, x='Date', y='Forecast Volume', markers=True,
                            title=f"Daily Forecast for {selected_month}")
        daily_fig.update_layout(xaxis_title="Date", yaxis_title="Forecast Volume",
                                xaxis=dict(tickangle=-45), yaxis=dict(range=[0, filtered_data['Forecast Volume'].max() * 1.1]))

        st.plotly_chart(daily_fig)


if __name__ == "__main__":
    forecast_page()
