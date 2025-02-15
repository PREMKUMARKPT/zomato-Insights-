import streamlit as st
import mysql.connector
import pandas as pd

# Connect to MySQL
def get_connection():
    return mysql.connector.connect(
        host="your_host",
        user="your_user",
        password="your_password",
        database="PROJECT_1",
        port=4000
    )

# Function to run SQL queries
def run_query(query):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    return result

# Streamlit UI
st.title("📊 Zomato Data Insights Dashboard")

# Show total customers
st.subheader("👥 Total Customers")
total_customers = run_query("SELECT COUNT(*) FROM Customers;")
st.metric(label="Total Customers", value=total_customers[0][0])

# Show total orders
st.subheader("🛒 Total Orders")
total_orders = run_query("SELECT COUNT(*) FROM Orders;")
st.metric(label="Total Orders", value=total_orders[0][0])

# Show top 5 restaurants by order count
st.subheader("🏆 Top 5 Restaurants")
top_restaurants = run_query("""
    SELECT r.restaurant_name, COUNT(o.order_id) AS total_orders
    FROM Orders o
    JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
    GROUP BY r.restaurant_name ORDER BY total_orders DESC LIMIT 5;
""")
df_top_restaurants = pd.DataFrame(top_restaurants, columns=["Restaurant", "Total Orders"])
st.dataframe(df_top_restaurants)

# Show total revenue generated
st.subheader("💰 Total Revenue")
total_revenue = run_query("SELECT SUM(total_amount) FROM Orders;")
st.metric(label="Total Revenue", value=f"₹ {total_revenue[0][0]:,.2f}")

# Show popular payment modes
st.subheader("💳 Payment Mode Usage")
payment_modes = run_query("""
    SELECT payment_mode, COUNT(*) FROM Orders
    GROUP BY payment_mode ORDER BY COUNT(*) DESC;
""")
df_payment_modes = pd.DataFrame(payment_modes, columns=["Payment Mode", "Usage Count"])
st.bar_chart(df_payment_modes.set_index("Payment Mode"))

# Show delivery time analysis
st.subheader("🚚 Average Delivery Time by Vehicle Type")
delivery_times = run_query("""
    SELECT vehicle_type, AVG(delivery_time) FROM Deliveries GROUP BY vehicle_type;
""")
df_delivery_times = pd.DataFrame(delivery_times, columns=["Vehicle Type", "Avg Delivery Time"])
st.bar_chart(df_delivery_times.set_index("Vehicle Type"))

st.write("📌 More insights coming soon...")
