import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter 
import seaborn as sns
from babel.numbers import format_currency
sns.set_theme(style='dark')

st.title('E-Commers Brazilian Analysis')


def rfm_analysis():
    st.subheader("Sales Analysis")
    df = pd.read_csv(r'D:\portofolio\E-commerce-Brazilian\dashboard\ecommers.csv')
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

    revenue = st.columns(1)[0]
    with revenue:
        total_revenue = format_currency(df['payment_value'].sum(), "AUD", locale='es_CO')  # type: ignore
        st.metric("Total Revenue", value=total_revenue)    
    
    order, customer, category = st.columns(3)
    
    with order:
        total_orders = df['order_id'].count()
        st.metric("Total Orders", value=total_orders)
    with customer:
        total_customers = len(pd.unique(df['customer_id']))
        st.metric("Total Customers", value=total_customers)
    with category:
        total_category = len(pd.unique(df['product_category_group']))
        st.metric("Total Category", value=total_category)

    df['year_month'] = pd.to_datetime(df['order_purchase_timestamp']).dt.to_period('M')
    monthly_revenue = df.groupby('year_month')['payment_value'].sum().reset_index()
    monthly_revenue['year_month_str'] = monthly_revenue['year_month'].dt.strftime('%Y-%m')
    fig, ax = plt.subplots(figsize=(9, 3))

    def format_func(value, tick_number):
        return f'{value:,.0f}'

    plt.plot(monthly_revenue['year_month_str'], monthly_revenue['payment_value'])
    plt.title('Monthly Sales Trend', loc='left')
    plt.xlabel('')
    plt.ylabel('')
    plt.gca().yaxis.set_major_formatter(FuncFormatter(format_func))
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)    
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    st.pyplot(fig)

    top_product, top_city = st.columns(2)
    with top_product:
        df_product = df.groupby('product_category_group')['payment_value'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 3))
        df_product.sort_values('payment_value', ascending=False).head(5).plot.bar(x='product_category_group', y='payment_value', ax=ax, color=colors)

        ax.yaxis.set_major_formatter(FuncFormatter(format_func))

        plt.title('Top 5 Product Categories with Highest Revenue')
        plt.ylabel('')
        plt.xlabel('')
        plt.xticks(rotation=45, ha='right')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.get_legend().remove()
        plt.tight_layout()
        st.pyplot(fig)
    
    with top_city:
        df_city = df.groupby('customer_city')['payment_value'].sum().reset_index()
        fig, ax = plt.subplots(figsize=(6, 3))
        df_city.sort_values('payment_value', ascending=False).head(5).plot.bar(x='customer_city', y='payment_value', ax=ax, color=colors)
        ax.yaxis.set_major_formatter(FuncFormatter(format_func))
        plt.title('Top 5 City with Highest Revenue')
        plt.ylabel('')
        plt.xlabel('')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        plt.xticks(rotation=45, ha='right') 
        ax.get_legend().remove()
        plt.tight_layout()
        st.pyplot(fig)

    df_rfm = pd.read_csv(r'D:\portofolio\E-commerce-Brazilian\dashboard\rfm_dataset.csv')

    df_rfm_count = df_rfm['segments'].value_counts().reset_index()
    df_rfm_count.columns = ['segments', 'customer_count']

    fig, ax = plt.subplots(figsize=(5, 1))
    colors = ["#90CAF9", "#D3D3D3", "#D3D3D3"]
    sns.barplot(
        x="customer_count", 
        y="segments",
        data=df_rfm_count.sort_values(by="customer_count", ascending=False),
        palette=colors,
        ax=ax,
    
    )

    ax.set_title("Number of Customers by Segment", loc="center", fontsize=5)
    ax.set_ylabel(None)
    ax.set_xlabel(None)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.tick_params(axis='y', labelsize=5)
    ax.tick_params(axis='x', labelsize=5)
    st.pyplot(fig)

    with st.expander("Insight"):
        st.write(
            """
Sales Performance Overview:
The company has demonstrated strong growth from Q4 2016 to Q2 2018, 
with a significant revenue spike during November-December 2017, 
likely driven by increased consumer spending during the holiday season. 
However, the sharp revenue decline toward the end of 2018 requires prompt investigation, 
as it could indicate either incomplete data or a substantial market disruption.

Product Category Analysis:
Home products are the top revenue earners, significantly outpacing other categories. 
Furniture holds a solid second place, highlighting a profitable market in home-related merchandise. 
Electronics, typically a high-revenue category, ranks fifth, which may suggest an opportunity for strategic growth or a need to reassess the product line.

Geographical Revenue Distribution:
São Paulo is the leading source of revenue, which is consistent with its status as Brazil's economic center. 
There is a gap between São Paulo and the next highest contributor, Rio de Janeiro. 
The inclusion of Belo Horizonte and Brasília in the top five further emphasizes the importance of major urban centers to the company's revenue.

Customer Segmentation Insights:
The customer base is well-segmented, with Loyal Customers representing the largest group, indicating strong retention efforts. 
The significant presence of Top Customers suggests a valuable, high-spending demographic. 
Although the Loss Customers segment is smaller, it presents an opportunity for targeted re-engagement strategies.

Strategic Recommendations:
1. Focus on expanding and optimizing the home products and furniture categories to capitalize on their strong market position.
2. Investigate the sales decline in late 2018 to identify and address any underlying issues.
3. Develop strategies to transition Top Customers into Loyal Customers, enhancing their long-term value.
4. Explore strategies for market penetration in cities beyond São Paulo to diversify the revenue base.
5. Launch targeted campaigns to re-engage the Loss Customers segment and reduce further attrition.
6. Reevaluate the electronics category, considering product line expansion or targeted marketing efforts to boost its performance.
7. Leverage seasonal trends by creating targeted promotional strategies for future peak periods.
            """
        )

with st.sidebar:
    st.text('Table of Content')
    
    page = st.radio(
        "Go to",
        ["RFM Analysis"],
        label_visibility='collapsed'
    )

rfm_analysis()



