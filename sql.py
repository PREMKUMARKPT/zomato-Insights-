import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px

# 🚀 Function to Connect to MySQL Database
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="gateway01.ap-southeast-1.prod.aws.tidbcloud.com",
            user="7Z3SRE1xmB2xsHv.root",
            password="593g7sDIAPe2H7Og",
            database="PROJECT_1"
        )
        return conn
    except mysql.connector.Error as err:
        st.error(f"Database connection failed: {err}")
        return None

# 📌 SQL Queries Dictionary (More Queries Added)
queries = {
    "📊 Peak Order Hours": """ 
        SELECT HOUR(order_datetime) AS hour, COUNT(*) AS total_orders 
        FROM orders 
        GROUP BY hour 
        ORDER BY total_orders DESC;
    """,
    "🍽️ Most Ordered Cuisine Type": """
        SELECT r.cuisine_type, COUNT(*) AS total_orders 
        FROM orders o 
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
        GROUP BY r.cuisine_type 
        ORDER BY total_orders DESC;
    """,
    "🏆 Top 10 Restaurants": """
        SELECT r.name, COUNT(*) AS total_orders 
        FROM orders o 
        JOIN restaurants r ON o.restaurant_id = r.restaurant_id 
        GROUP BY r.name 
        ORDER BY total_orders DESC 
        LIMIT 10;
    """,
    "💰 Average Order Value": """
        SELECT AVG(total_amount) AS avg_order_value FROM orders;
    """,
    "🚚 Average Delivery Time": """
        SELECT AVG(TIMESTAMPDIFF(MINUTE, o.order_datetime, d.delivery_time)) AS avg_delivery_time 
        FROM orders o 
        JOIN delivery d ON o.order_id = d.order_id 
        WHERE d.status = 'Delivered';
    """,
    "📅 Daily Order Trend": """
        SELECT DATE(order_datetime) AS order_date, COUNT(*) AS total_orders 
        FROM orders 
        GROUP BY order_date 
        ORDER BY order_date;
    """,
    "🛵 Most Active Delivery Agents": """
        SELECT d.delivery_agent, COUNT(*) AS deliveries 
        FROM delivery d 
        GROUP BY d.delivery_agent 
        ORDER BY deliveries DESC 
        LIMIT 5;
    """,
    "🏙️ Cities with Most Orders": """
        SELECT c.city, COUNT(*) AS total_orders 
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id 
        GROUP BY c.city 
        ORDER BY total_orders DESC;
    """,
    "👥 Most Frequent Customers": """
        SELECT c.name, COUNT(*) AS total_orders 
        FROM customers c 
        JOIN orders o ON c.customer_id = o.customer_id 
        GROUP BY c.name 
        ORDER BY total_orders DESC 
        LIMIT 10;
    """,
    "⚡ Fastest Delivered Orders": """
        SELECT o.order_id, TIMESTAMPDIFF(MINUTE, o.order_datetime, d.delivery_time) AS delivery_time 
        FROM orders o 
        JOIN delivery d ON o.order_id = d.order_id 
        WHERE d.status = 'Delivered' 
        ORDER BY delivery_time ASC 
        LIMIT 5;
    """
}

# 🎨 Streamlit UI Design
st.title("📊 Zomato - Food Delivery Insights")
st.write("Select a query to analyze food delivery trends.")

# 🔍 User selects a query
query_name = st.selectbox("Choose a Query", list(queries.keys()))

# 🏁 Run Query Button
if st.button("Run Query"):
    conn = get_db_connection()
    
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute(queries[query_name])
            data = cursor.fetchall()
            columns = [i[0] for i in cursor.description]  # Fetch column names

            df = pd.DataFrame(data, columns=columns)

            # 📊 Display Data
            st.dataframe(df)

            # 📈 Generate Bar Chart for Visual Queries
            if len(df) > 0:
                fig = px.bar(df, x=df.columns[0], y=df.columns[1], title=query_name, text_auto=True)
                st.plotly_chart(fig)

            # 📥 Download as CSV
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("Download CSV", csv, f"{query_name}.csv", "text/csv")

        except mysql.connector.Error as err:
            st.error(f"SQL Execution Error: {err}")

        finally:
            cursor.close()
            conn.close()
