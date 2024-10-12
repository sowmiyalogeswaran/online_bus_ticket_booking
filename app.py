import streamlit as st
import mysql.connector
import pandas as pd

# Database connection
def create_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='3008',
        auth_plugin='mysql_native_password',
        database='redbus'
    )

# Fetching distinct state names (routes)
def fetch_states(my_connection):
    query = "SELECT DISTINCT Route_Name FROM bus_routes"
    df_states = pd.read_sql(query, my_connection)
    return df_states['Route_Name'].tolist()

# Fetching bus data for selected state
def fetch_buses_for_state(my_connection, selected_state):
    query = "SELECT * FROM bus_routes WHERE Route_Name = %s"
    df_buses = pd.read_sql(query, my_connection, params=(selected_state,))
    return df_buses

# Streamlit UI
st.set_page_config(page_title="Online Bus Booking", layout='wide')

# Title of the app
st.title("Online Bus Tickets Booking App")

# Sidebar: Select State (Route Name)
my_connection = create_connection()
states = fetch_states(my_connection)
selected_state = st.sidebar.selectbox('Select a State:', states)

# Sidebar: Filter by Price, Bus Type, Star Rating
if selected_state:
    # Fetch bus data for the selected state
    bus_data = fetch_buses_for_state(my_connection, selected_state)
    
    if not bus_data.empty:
        # Sidebar Filters
        st.sidebar.subheader("Filter Options")
        
        # Sort by Price
        price_sort_order = st.sidebar.radio("Sort by Price:", ["Low to High", "High to Low"])
        price_sort_order_sql = "ASC" if price_sort_order == "Low to High" else "DESC"
        
        # Filter by Star Rating
        star_ratings = bus_data['Star_Rating'].unique().tolist()
        selected_ratings = st.sidebar.multiselect('Filter by Star Rating', star_ratings)
        
        # Filter by Bus Type
        bus_types = bus_data['Bus_Type'].unique().tolist()
        selected_bus_types = st.sidebar.multiselect('Filter by Bus Type', bus_types)
        
        # Sort and filter bus data
        bus_data = bus_data.sort_values(by='Price', ascending=True if price_sort_order == 'Low to High' else False)
        if selected_ratings:
            bus_data = bus_data[bus_data['Star_Rating'].isin(selected_ratings)]
        if selected_bus_types:
            bus_data = bus_data[bus_data['Bus_Type'].isin(selected_bus_types)]
        
        # Display filtered bus data
        st.subheader(f"Available Buses for {selected_state}")
        st.write(bus_data)


    else:
        st.write(f"No buses found for the state: {selected_state}")

# Close the database connection
my_connection.close()

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("Developed by Sowmiya lakshmee. All rights reserved.", unsafe_allow_html=True)
