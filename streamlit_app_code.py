import streamlit as st
import pandas as pd
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="Nassau Candy Distributor Analysis",
    page_icon="🍬",
    layout="wide"
)

# App Title & Description
st.title("🍬 Nassau Candy Distributor Data Analysis")
st.markdown("An interactive analytics dashboard to explore sales performance, profitability, and top products.")

# Cache data loading for optimal performance
@st.cache_data
def load_data():
    df = pd.read_csv("Nassau Candy Distributor.csv")
    # Clean column names
    df.columns = df.columns.str.strip()
    # Convert date if present
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'], errors='coerce')
    return df

try:
    df = load_data()

    # Sidebar Filters
    st.sidebar.header("🔍 Filter Dashboard")
    
    # Division Filter
    divisions = df['Division'].unique().tolist() if 'Division' in df.columns else []
    selected_divisions = st.sidebar.multiselect("Select Division", options=divisions, default=divisions)
    
    # Region Filter
    regions = df['Region'].unique().tolist() if 'Region' in df.columns else []
    selected_regions = st.sidebar.multiselect("Select Region", options=regions, default=regions)

    # Filter Dataframe
    filtered_df = df.copy()
    if selected_divisions:
        filtered_df = filtered_df[filtered_df['Division'].isin(selected_divisions)]
    if selected_regions:
        filtered_df = filtered_df[filtered_df['Region'].isin(selected_regions)]

    # Top Key Metrics
    st.subheader("📊 Key Performance Indicators (KPIs)")
    col1, col2, col3, col4 = st.columns(4)

    total_sales = filtered_df['Sales'].sum() if 'Sales' in filtered_df.columns else 0
    total_profit = filtered_df['Gross Profit'].sum() if 'Gross Profit' in filtered_df.columns else 0
    total_units = filtered_df['Units'].sum() if 'Units' in filtered_df.columns else 0
    total_cost = filtered_df['Cost'].sum() if 'Cost' in filtered_df.columns else 0

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Units Sold", f"{int(total_units):,}")
    col4.metric("Total Cost", f"${total_cost:,.2f}")

    st.markdown("---")

    # Visualizations Section
    col_left, col_right = st.columns(2)

    with col_left:
        if 'Division' in filtered_df.columns and 'Sales' in filtered_df.columns:
            div_sales = filtered_df.groupby('Division')['Sales'].sum().reset_index()
            fig_div = px.bar(
                div_sales, 
                x='Division', 
                y='Sales', 
                title="<b>Sales by Division</b>",
                color='Division',
                text_auto='.2s'
            )
            st.plotly_chart(fig_div, use_container_width=True)

    with col_right:
        if 'Product Name' in filtered_df.columns and 'Sales' in filtered_df.columns:
            top_products = filtered_df.groupby('Product Name')['Sales'].sum().reset_index()
            top_products = top_products.sort_values(by='Sales', ascending=False).head(10)
            fig_prod = px.bar(
                top_products, 
                x='Sales', 
                y='Product Name', 
                orientation='h',
                title="<b>Top 10 Products by Sales</b>",
                color='Sales',
                color_continuous_scale='Viridis'
            )
            fig_prod.update_layout(yaxis={'categoryorder': 'total ascending'})
            st.plotly_chart(fig_prod, use_container_width=True)

    # Detailed Data Table
    st.markdown("---")
    st.subheader("📋 Dataset Overview")
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Error loading or processing data: {e}")
    st.info("Please make sure 'Nassau Candy Distributor.csv' is placed in the same folder as 'app.py'.")