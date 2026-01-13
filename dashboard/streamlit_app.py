import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Amazon Sales Analytics", layout="wide")

st.title("Amazon Sales Analytics Dashboard")

@st.cache_data
def load_data():
    sales_by_category = pd.read_parquet('../data/parquet/sales_by_category.parquet')
    top_rated_products = pd.read_parquet('../data/parquet/top_rated_products.parquet')
    return sales_by_category, top_rated_products

sales, products = load_data()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Products", len(sales))
col2.metric("AVG Price", f"${sales['avg_discounted_price'].mean():.2f}")
col3.metric("AVG Rating", f"{sales['avg_rating'].mean():.2f} ⭐")
col4.metric("Categories", len(sales['category'].unique()))

st.subheader("Sales by Category")
fig = px.bar(sales, x="category", y="total_products", title="Total Sales by Category", labels={"total_products":"Total Products", "category":"Category"})
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top Rated Products")
fig2 = px.scatter(products, x="product_id", y="rating", size="rating_count", color="category", hover_data=["Product_name"], title="Top Rated Products")
st.plotly_chart(fig2, use_container_width=True)

if st.button("Refresh Data"):
    st.cache_data.clear()
    st.rerun()