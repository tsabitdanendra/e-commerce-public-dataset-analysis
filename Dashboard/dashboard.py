import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

data = pd.read_csv('main_data.csv')

st.title("E-Commerce Public Dataset Analysis")


tab1, tab2, tab3, tab4 = st.tabs(["Order", "Payment", "Review","RFM Analysis"])

with tab1:

    st.subheader('Trend Pembelian Tiap Tahun')
    chartTab1, expTab1 = st.columns(2)

    with chartTab1:
        getTahunPembelian = data.groupby('tahunPembelian').size().reset_index(name='jumlah')        
        selected_years = [2016, 2017, 2018]
        filtered_data = getTahunPembelian[getTahunPembelian['tahunPembelian'].isin(selected_years)]
        
        fig, ax = plt.subplots()

        # bar chart
        ax.bar(filtered_data['tahunPembelian'], filtered_data['jumlah'], color='blue', label='Jumlah Pembelian')

        # line chart
        ax.plot(filtered_data['tahunPembelian'], filtered_data['jumlah'], marker='o', color='red', label='Pertumbuhan')

        # Label dan judul
        ax.set_xlabel('Tahun Pembelian')
        ax.set_ylabel('Jumlah Pembelian')
        ax.set_title('Jumlah Pembelian Tiap Tahun')

        ax.set_xticks(selected_years)

        ax.legend()        
        st.pyplot(fig)
        
    with expTab1:
        with st.expander("Penjelasan"):
            st.write('''Bar chart di samping membandingkan tahun dengan jumlah order yang dilakukan customer.
            Seperti yang dapat dilihat jumlah pembelian customer meningkat setiap tahunnya. 
            Terjadi peningkatan yang signifikan dari tahun 2016 ke tahun 2017, dan dari tahun 2017 ke 2018, kembali 
            terjadi peningkatan walaupun tidak seperti peningkatan sebelumnya. Garis merah menunjukkan trend pembelian customer.''')

with tab2:
    
    st.subheader("Jumlah Metode Pembayaran")
    chartTab2, expTab2 = st.columns(2)

    with chartTab2:    
    
        totalPayment = data.groupby('payment_type').size().reset_index(name='count')
        
        fig, ax = plt.subplots(figsize=(8, 8))
        sns.barplot(x='payment_type', y='count', data=totalPayment, palette='viridis', ax=ax)
        ax.set_xlabel('Metode Pembayaran')
        ax.set_ylabel('Jumlah Transaksi')
        ax.set_title('Total Transaksi Berdasarkan Metode Pembayaran')
        
        st.pyplot(fig)

    with expTab2:
        with st.expander("Penjelasan"):
            st.write('''Bar chart di samping membandingkan metode pembayaran dengan jumlah transaksi yang dilakukan customer.
            Seperti yang dapat dilihat, terdapat 5 jenis metode pembayaran yang digunakan customer. Metode pembayaran yang paling banyak digunakan
            adalah credit card dan yang paling sedikit adalah debit card. Ada juga metode pembayaran yang tidak didefiniskan oleh customer yang
            jumlahnya lebih sedikit dari debit card.''')


with tab3:

    col1, col2 = st.columns(2)

    with col1:
        st.subheader('Persebaran Review Score')
        reviews = data.groupby('review_score').agg({'review_score': 'count'}).rename(columns={'review_score': 'count'})
        
        dataReviews = {'Review Score': reviews.index, 'Count': reviews['count']}
        df_reviews = pd.DataFrame(dataReviews)        
        
        fig, ax = plt.subplots(figsize=(8, 8))
        wedges, texts, autotexts = ax.pie(df_reviews['Count'], labels=df_reviews['Review Score'].astype(int), autopct='%1.1f%%', startangle=90, colors=['purple', 'orange', 'yellow', 'green', 'red'])
        
        ax.axis('equal')
        
        ax.legend(wedges, [f'{score}: {count}' for score, count in zip(df_reviews['Review Score'].astype(int), df_reviews['Count'])], title='Review Score', loc='center left', bbox_to_anchor=(1, 0.5))
        
        st.pyplot(fig)   
        with st.expander("Penjelasan"):
            st.write('''Pie chart di atas menunjukkan persebaran Review Score (Rating 1-5) yang diberikan oleh customer untuk 
            setiap review dari order yang telah mereka lakukan. Terlihat bahwa Rating dengan Review Score 5 memiliki persentase
            terbanyak dengan 57.7%, diikuti dengan Review Score 4 dengan mengisi 19.3% dari populasi. Selain itu Rating dengan
            Review Score 2 merupakan Review Score yang paling sedikit.''')

    with col2:

        st.subheader('Perbandingan Review')

        reviewsCompare = data.groupby('review_status').agg({'review_status':'count'})
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.bar(reviewsCompare.index, reviewsCompare['review_status'], color=['red', 'green'])

        # Label dan judul
        ax.set_xlabel('Review Status')
        ax.set_ylabel('Jumlah Review')
        ax.set_title('Perbandingan Review dan Not Review')
    
        st.pyplot(fig)
        with st.expander("Penjelasan"):
                st.write('''Bar chart di atas menunjukkan perbandingan antara customer yang memberikan review dan tidak memberikan 
                review pada order yang mereka lakukan. Terlihat bahwa customer yang memberikan review jauh lebih banyak daripada
                customer yang tidak memberikan review.''')

with tab4:

    st.subheader("RFM Analysis")
    data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
    current_date = max(data['order_purchase_timestamp'])

    # Group by sesuai RFM
    rfm_data = data.groupby('customer_id').agg({
        'order_purchase_timestamp': lambda x: (current_date - x.max()).days, 
        'order_id': 'count', 
        'payment_value': 'sum'
    }).rename(columns={
        'order_purchase_timestamp': 'Recency',
        'order_id': 'Frequency',
        'payment_value': 'Monetary'
    }).reset_index()

    # Top 5/RFM analysis
    rfm_data_recency_sorted = rfm_data.sort_values(by='Recency', ascending=True).head(5)
    rfm_data_frequency_sorted = rfm_data.sort_values(by='Frequency', ascending=False).head(5)
    rfm_data_monetary_sorted = rfm_data.sort_values(by='Monetary', ascending=False).head(5)

    # parse index ke string
    rfm_data_recency_sorted.index = rfm_data_recency_sorted.index.astype(str)
    rfm_data_frequency_sorted.index = rfm_data_frequency_sorted.index.astype(str)
    rfm_data_monetary_sorted.index = rfm_data_monetary_sorted.index.astype(str)

    fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(15, 5))

    # Recency
    axes[0].bar(rfm_data_recency_sorted.index, rfm_data_recency_sorted['Recency'], color='blue')
    axes[0].set_title('Recency')
    axes[0].set_yticks(range(0, 21, 5))
    axes[0].set_xlabel('customer_id')

    # Frequency
    axes[1].bar(rfm_data_frequency_sorted.index, rfm_data_frequency_sorted['Frequency'], color='green')
    axes[1].set_title('Frequency')
    axes[1].set_xlabel('customer_id')

    # Monetary
    axes[2].bar(rfm_data_monetary_sorted.index, rfm_data_monetary_sorted['Monetary'], color='orange')
    axes[2].set_title('Monetary')
    axes[2].set_xlabel('customer_id')

    # Label
    fig.suptitle('Top 5 setiap kategori RFM analysis (customer_id)')    
    st.pyplot(fig)

    with st.expander("Penjelasan"):
        st.write('''Hasil dari RFM Analysis ditunjukkan melalui 3 Bar Chart di atas. Bar Chart sebelah kiri menunjukkan transaksi 
        terakhir yang dilakukan customer (Recency), Bar Chart yang di tengah menunjukkan order yang paling banyak dilakukan oleh 
        customer yang sama (Frequency), dan Bar Chart yang di sebelah kanan menunjukkan pengeluaran yang paling banyak dikeluarkan
        oleh customer (Monetary). Pada Recency, Nilai yang paling tinggi adalah 18 hari terakhir. Pada Frequency, nilai yang paling tinggi
        adalah 29 kali. Pada Monetary, nilai yang paling tinggi adalah sekitar 13.000 Brazil Real. ''')


