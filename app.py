import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
from algorithms.PrefixSpan import PrefixSpan

# Cấu hình trang
st.set_page_config(
    page_title="PrefixSpan Pattern Mining Demo",
    layout="wide"
)

st.title("🛍️ Demo Khai thác Mẫu Tuần tự với PrefixSpan")
st.markdown("---")

# Khởi tạo session state
if 'transaction_history' not in st.session_state:
    st.session_state.transaction_history = pd.DataFrame(
        columns=['Customer_ID', 'Timestamp', 'Items']
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
            new_transaction = {
                'Customer_ID': customer_id,
                'Items': ', '.join(selected_products),
                'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            st.session_state.transaction_history = pd.concat([
                st.session_state.transaction_history,
                pd.DataFrame([new_transaction])
            ], ignore_index=True)
            st.success("Đã thêm giao dịch mới!")

# Layout chính
col1, col2 = st.columns([2, 1])

# Hiển thị lịch sử giao dịch
with col1:
    st.subheader("📋 Lịch sử giao dịch theo thời gian")
    if not st.session_state.transaction_history.empty:
        st.dataframe(st.session_state.transaction_history.sort_values('Timestamp', ascending=False),
                    use_container_width=True)
    else:
        st.info("Chưa có giao dịch nào. Hãy thêm giao dịch mới từ sidebar!")

# Phân tích mẫu tuần tự
with col2:
    st.subheader("📊 Phân tích mẫu tuần tự")
    min_support = st.slider(
        "Chọn giá trị min support",
        min_value=1,
        max_value=100,
        value=3,
        step=1
    )
    
    if not st.session_state.transaction_history.empty:
        # Chuẩn bị dữ liệu cho PrefixSpan
        sequences = []
        for customer in st.session_state.transaction_history['Customer_ID'].unique():
            customer_sequences = st.session_state.transaction_history[
                st.session_state.transaction_history['Customer_ID'] == customer
            ].sort_values('Timestamp')
            
            sequence = [
                [item.strip() for item in items.split(',')]
                for items in customer_sequences['Items']
            ]
            sequences.append(sequence)
        
        # Áp dụng PrefixSpan
        prefixspan = PrefixSpan(min_support)
        patterns = prefixspan.mine_sequential_patterns(sequences)
        
        if patterns:
            # Chuyển kết quả sang DataFrame để hiển thị
            patterns_df = pd.DataFrame([
                {
                    'Pattern': ' -> '.join([', '.join(itemset) for itemset in pattern]),
                    'Support': count
                }
                for pattern, count in patterns.items()
            ])
            patterns_df = patterns_df.sort_values('Support', ascending=False)
            
            st.dataframe(patterns_df, use_container_width=True)
            
            # Visualize top patterns
            fig = px.bar(
                patterns_df.head(10),
                x='Pattern',
                y='Support',
                title='Top 10 mẫu tuần tự phổ biến nhất'
            )
            fig.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("Không tìm thấy mẫu tuần tự với giá trị min support đã chọn")

# Thống kê
if not st.session_state.transaction_history.empty:
    st.markdown("---")
    st.subheader("📈 Thống kê tổng quan")
    
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric(
            "Số khách hàng",
            st.session_state.transaction_history['Customer_ID'].nunique()
        )
    
    with stat_col2:
        total_transactions = len(st.session_state.transaction_history)
        st.metric("Tổng số giao dịch", total_transactions)
    
    with stat_col3:
        avg_items = st.session_state.transaction_history['Items'].apply(
            lambda x: len(x.split(','))
        ).mean()
        st.metric("Trung bình số items/giao dịch", f"{avg_items:.2f}")

# Nút reset
if st.button("🔄 Reset dữ liệu"):
    st.session_state.transaction_history = pd.DataFrame(
        columns=['Customer_ID', 'Timestamp', 'Items']
    )
    st.success("Đã xóa toàn bộ dữ liệu!")
    st.rerun()
