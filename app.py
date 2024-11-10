import streamlit as st
import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import numpy as np
from datetime import datetime
import plotly.express as px

# Cấu hình trang
st.set_page_config(
    page_title="Demo Sequence Pattern Mining",
    layout="wide"
)

# Tiêu đề ứng dụng
st.title("🛍️ Demo Phân tích Mẫu Mua sắm")
st.markdown("---")

# Khởi tạo session state
if 'transactions' not in st.session_state:
    st.session_state.transactions = []
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = pd.DataFrame(
        columns=['Transaction_ID', 'Customer_ID', 'Items', 'Timestamp']
    )

# Danh sách sản phẩm mẫu
SAMPLE_PRODUCTS = [
    "Laptop", "Smartphone", "Headphones", "Mouse", "Keyboard",
    "Monitor", "Tablet", "Printer", "Camera", "Speaker"
]

# Sidebar cho thông tin khách hàng
with st.sidebar:
    st.header("🛒 Thông tin mua hàng")
    customer_id = st.text_input("ID Khách hàng", value="CUST001")
    selected_products = st.multiselect("Chọn sản phẩm", SAMPLE_PRODUCTS)
    
    if st.button("Thêm giao dịch"):
        if selected_products:
            transaction_id = f"T{len(st.session_state.transaction_history) + 1:03d}"
            new_transaction = {
                'Transaction_ID': transaction_id,
                'Customer_ID': customer_id,
                'Items': ', '.join(selected_products),
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.transaction_history = pd.concat([
                st.session_state.transaction_history,
                pd.DataFrame([new_transaction])
            ], ignore_index=True)
            st.success("Đã thêm giao dịch mới!")

# Hiển thị lịch sử giao dịch
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📋 Lịch sử giao dịch")
    if not st.session_state.transaction_history.empty:
        st.dataframe(st.session_state.transaction_history, use_container_width=True)
    else:
        st.info("Chưa có giao dịch nào. Hãy thêm giao dịch mới từ sidebar!")

# Phân tích mẫu
with col2:
    st.subheader("📊 Phân tích mẫu phổ biến")
    min_support = st.slider(
        "Chọn giá trị min support",
        min_value=0.1,
        max_value=1.0,
        value=0.3,
        step=0.1
    )
    
    if not st.session_state.transaction_history.empty:
        # Chuẩn bị dữ liệu cho phân tích
        transactions = [
            set(items.split(', '))
            for items in st.session_state.transaction_history['Items']
        ]
        
        te = TransactionEncoder()
        te_ary = te.fit_transform(transactions)
        df = pd.DataFrame(te_ary, columns=te.columns_)
        
        # Tìm mẫu phổ biến
        frequent_patterns = fpgrowth(df, min_support=min_support, use_colnames=True)
        if not frequent_patterns.empty:
            frequent_patterns['itemsets'] = frequent_patterns['itemsets'].apply(lambda x: ', '.join(list(x)))
            frequent_patterns['support'] = frequent_patterns['support'].round(3)
            st.dataframe(frequent_patterns, use_container_width=True)
            
            # Visualize top patterns
            if len(frequent_patterns) > 0:
                fig = px.bar(
                    frequent_patterns.head(10),
                    x='itemsets',
                    y='support',
                    title='Top 10 mẫu phổ biến nhất'
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Không tìm thấy mẫu phổ biến với giá trị min support đã chọn")

# Thêm phần thống kê
if not st.session_state.transaction_history.empty:
    st.markdown("---")
    st.subheader("📈 Thống kê tổng quan")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric(
            "Tổng số giao dịch",
            len(st.session_state.transaction_history)
        )
    
    with stat_col2:
        unique_customers = st.session_state.transaction_history['Customer_ID'].nunique()
        st.metric("Số khách hàng", unique_customers)
    
    with stat_col3:
        all_items = []
        for items in st.session_state.transaction_history['Items']:
            all_items.extend(items.split(', '))
        st.metric("Tổng số sản phẩm đã bán", len(all_items))
    
    with stat_col4:
        unique_items = len(set(all_items))
        st.metric("Số loại sản phẩm", unique_items)

# Nút reset
if st.button("🔄 Reset dữ liệu"):
    st.session_state.transaction_history = pd.DataFrame(
        columns=['Transaction_ID', 'Customer_ID', 'Items', 'Timestamp']
    )
    st.success("Đã xóa toàn bộ dữ liệu!")
    st.rerun()