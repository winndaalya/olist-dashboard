import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Brazilian E-Commerce Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem; font-weight: 800; color: #1565C0;
        text-align: center; padding: 10px 0 5px 0;
    }
    .sub-header {
        font-size: 1rem; color: #546E7A;
        text-align: center; margin-bottom: 20px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1565C0, #42A5F5);
        border-radius: 12px; padding: 18px 22px;
        color: white; text-align: center;
    }
    .metric-value { font-size: 1.9rem; font-weight: 800; }
    .metric-label { font-size: 0.85rem; opacity: 0.88; margin-top: 4px; }
    .insight-box {
        background-color: #E3F2FD; border-left: 5px solid #1565C0;
        padding: 14px 18px; border-radius: 6px; margin: 10px 0;
        font-size: 0.93rem;
    }
    .section-title {
        font-size: 1.4rem; font-weight: 700; color: #1A237E;
        border-bottom: 3px solid #42A5F5; padding-bottom: 6px;
        margin: 24px 0 16px 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── LOAD DATA ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv")
    df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
    return df

@st.cache_data
def load_rfm():
    return pd.read_csv("dashboard/rfm_data.csv")

df = load_data()
rfm_df = load_rfm()

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown('<div class="main-header">🛒 Brazilian E-Commerce Analytics Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Analisis Data Platform Olist | 2016 – 2018 | Dicoding Submission</div>', unsafe_allow_html=True)

# ─── SIDEBAR FILTERS ─────────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Flag_of_Brazil.svg/320px-Flag_of_Brazil.svg.png", width=100)
    st.markdown("## 🔧 Filter Data")

    year_options = sorted(df['order_year'].dropna().unique().astype(int).tolist())
    selected_years = st.multiselect("Tahun", year_options, default=year_options)

    all_categories = sorted(df['product_category_name_english'].dropna().unique().tolist())
    all_categories = [c for c in all_categories if c != 'unknown']
    selected_categories = st.multiselect(
        "Kategori Produk (max 10 untuk chart)",
        all_categories,
        default=[],
        placeholder="Semua kategori"
    )

    all_states = sorted(df['customer_state'].dropna().unique().tolist())
    selected_states = st.multiselect("Negara Bagian", all_states, default=[])

    st.markdown("---")
    st.markdown("**📌 Pertanyaan Bisnis:**")
    st.markdown("1. Kategori produk terlaris & tren penjualan\n2. Pengaruh delivery time terhadap kepuasan\n3. Segmentasi pelanggan (RFM)")
    st.markdown("---")
    st.caption("© 2024 — Dicoding Data Analytics Submission")

# ─── FILTER DATA ─────────────────────────────────────────────────────────────
filtered = df[df['order_year'].isin(selected_years)].copy()
if selected_categories:
    filtered = filtered[filtered['product_category_name_english'].isin(selected_categories)]
if selected_states:
    filtered = filtered[filtered['customer_state'].isin(selected_states)]

if len(filtered) == 0:
    st.warning("⚠️ Tidak ada data yang sesuai dengan filter yang dipilih. Silakan ubah filter.")
    st.stop()

# ─── KPI METRICS ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">📊 Key Performance Indicators</div>', unsafe_allow_html=True)

total_orders = filtered['order_id'].nunique()
total_revenue = filtered['payment_value'].sum()
total_customers = filtered['customer_unique_id'].nunique()
avg_review = filtered['review_score'].mean()
avg_delivery = filtered['delivery_days'].mean()

c1, c2, c3, c4, c5 = st.columns(5)
metrics = [
    (c1, f"{total_orders:,}", "Total Pesanan"),
    (c2, f"R$ {total_revenue/1e6:.2f}M", "Total Revenue"),
    (c3, f"{total_customers:,}", "Total Pelanggan"),
    (c4, f"{avg_review:.2f} / 5.0", "Rata-rata Review"),
    (c5, f"{avg_delivery:.1f} Hari", "Avg Delivery Time"),
]
for col, val, label in metrics:
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── TAB LAYOUT ──────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📦 Pertanyaan 1: Kategori & Tren",
    "⭐ Pertanyaan 2: Delivery & Kepuasan",
    "👥 Pertanyaan 3: RFM Segmentasi",
    "🗺️ Geospatial Analysis"
])

# ═══════════════════════════════════════════════════
# TAB 1: KATEGORI PRODUK & TREN PENJUALAN
# ═══════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📦 Kategori Produk Terlaris & Tren Penjualan</div>', unsafe_allow_html=True)

    st.markdown('<div class="insight-box">🎯 <b>Pertanyaan Bisnis 1:</b> Kategori produk apa yang menghasilkan total pendapatan tertinggi dan memiliki volume pesanan terbanyak pada platform Olist selama periode 2016–2018?</div>', unsafe_allow_html=True)

    col_left, col_right = st.columns(2)

    # Aggregasi kategori
    cat_df = filtered[filtered['product_category_name_english'] != 'unknown'].groupby(
        'product_category_name_english'
    ).agg(
        total_orders=('order_id', 'nunique'),
        total_revenue=('payment_value', 'sum'),
        avg_review=('review_score', 'mean')
    ).reset_index()

    n_top = 10
    top_rev = cat_df.sort_values('total_revenue', ascending=False).head(n_top)
    top_ord = cat_df.sort_values('total_orders', ascending=False).head(n_top)

    with col_left:
        fig, ax = plt.subplots(figsize=(8, 5))
        colors = sns.color_palette("YlOrRd", n_colors=n_top)[::-1]
        ax.barh(top_rev['product_category_name_english'][::-1],
                top_rev['total_revenue'][::-1] / 1e6, color=colors)
        ax.set_title('Top 10 Kategori: Total Revenue', fontweight='bold', fontsize=12)
        ax.set_xlabel('Revenue (Juta BRL)', fontsize=10)
        for bar in ax.patches:
            ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.1f}M', va='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col_right:
        fig, ax = plt.subplots(figsize=(8, 5))
        colors2 = sns.color_palette("YlGnBu", n_colors=n_top)[::-1]
        ax.barh(top_ord['product_category_name_english'][::-1],
                top_ord['total_orders'][::-1] / 1e3, color=colors2)
        ax.set_title('Top 10 Kategori: Volume Pesanan', fontweight='bold', fontsize=12)
        ax.set_xlabel('Jumlah Pesanan (Ribu)', fontsize=10)
        for bar in ax.patches:
            ax.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.1f}K', va='center', fontsize=8)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("---")
    st.markdown("**📈 Tren Penjualan Bulanan**")

    monthly = filtered.groupby('order_yearmonth').agg(
        total_orders=('order_id', 'nunique'),
        total_revenue=('payment_value', 'sum')
    ).reset_index().sort_values('order_yearmonth')
    monthly = monthly[monthly['order_yearmonth'] >= '2017-01']

    fig, ax1 = plt.subplots(figsize=(14, 5))
    x = range(len(monthly))
    ax1.fill_between(x, monthly['total_revenue'] / 1e6, alpha=0.25, color='#1565C0')
    ax1.plot(x, monthly['total_revenue'] / 1e6, color='#1565C0', linewidth=2.5,
              marker='o', markersize=4, label='Revenue')
    ax1.set_ylabel('Revenue (Juta BRL)', color='#1565C0', fontsize=11)
    ax1.tick_params(axis='y', labelcolor='#1565C0')

    ax2 = ax1.twinx()
    ax2.bar(x, monthly['total_orders'], alpha=0.35, color='#FF9800', label='Jumlah Order')
    ax2.set_ylabel('Jumlah Order', color='#E65100', fontsize=11)
    ax2.tick_params(axis='y', labelcolor='#E65100')

    tick_labels = [m if i % 2 == 0 else '' for i, m in enumerate(monthly['order_yearmonth'])]
    ax1.set_xticks(x)
    ax1.set_xticklabels(tick_labels, rotation=45, ha='right', fontsize=8)
    ax1.set_title('Tren Penjualan Bulanan (2017–2018)', fontweight='bold', fontsize=13)

    bf_list = list(monthly['order_yearmonth'])
    if '2017-11' in bf_list:
        bf_idx = bf_list.index('2017-11')
        ax1.axvline(x=bf_idx, color='red', linestyle='--', alpha=0.6, linewidth=1.5)
        ax1.annotate('Black Friday\nNov 2017', xy=(bf_idx, ax1.get_ylim()[1] * 0.8),
                      fontsize=9, color='red', ha='center')

    lines1, labs1 = ax1.get_legend_handles_labels()
    lines2, labs2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labs1 + labs2, loc='upper left', fontsize=9)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> Kategori <b>health_beauty</b> memimpin dalam revenue, sementara <b>bed_bath_table</b> unggul dalam volume. Lonjakan signifikan terjadi pada November 2017 (Black Friday), menandakan peluang besar untuk kampanye musiman.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TAB 2: DELIVERY TIME & REVIEW SCORE
# ═══════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">⭐ Pengaruh Delivery Time terhadap Kepuasan Pelanggan</div>', unsafe_allow_html=True)

    st.markdown('<div class="insight-box">🎯 <b>Pertanyaan Bisnis 2:</b> Bagaimana pola review score pelanggan berdasarkan lama waktu pengiriman, dan kategori produk mana yang paling berpotensi menyebabkan ketidakpuasan?</div>', unsafe_allow_html=True)

    # Delivery group analysis
    filtered_copy = filtered.copy()
    filtered_copy['delivery_group'] = pd.cut(
        filtered_copy['delivery_days'],
        bins=[0, 7, 14, 21, 30, 60, 180],
        labels=['0-7 hari', '8-14 hari', '15-21 hari', '22-30 hari', '31-60 hari', '>60 hari']
    )

    delivery_review = filtered_copy.groupby('delivery_group', observed=True).agg(
        avg_review=('review_score', 'mean'),
        total_orders=('order_id', 'nunique')
    ).round(2).reset_index()

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(8, 5))
        palette = ['#4CAF50', '#8BC34A', '#FFC107', '#FF9800', '#F44336', '#B71C1C']
        bars = ax.bar(delivery_review['delivery_group'].astype(str),
                       delivery_review['avg_review'], color=palette, edgecolor='white')
        for bar, val in zip(bars, delivery_review['avg_review']):
            ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.03,
                    f'{val:.2f}', ha='center', fontsize=10, fontweight='bold')
        ax.axhline(y=filtered['review_score'].mean(), color='navy',
                    linestyle='--', linewidth=1.5, label=f'Rata-rata: {filtered["review_score"].mean():.2f}')
        ax.set_title('Rata-rata Review Score per Lama Pengiriman', fontweight='bold', fontsize=12)
        ax.set_xlabel('Lama Pengiriman', fontsize=10)
        ax.set_ylabel('Review Score (1–5)', fontsize=10)
        ax.set_ylim(0, 5.5)
        ax.legend(fontsize=9)
        plt.xticks(rotation=20)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        # Kategori dengan review terendah
        cat_review = filtered_copy[filtered_copy['product_category_name_english'] != 'unknown'].groupby(
            'product_category_name_english'
        ).agg(
            avg_review=('review_score', 'mean'),
            avg_delivery=('delivery_days', 'mean'),
            total_orders=('order_id', 'nunique')
        ).reset_index()
        cat_review = cat_review[cat_review['total_orders'] >= 50].sort_values('avg_review')

        fig, ax = plt.subplots(figsize=(8, 5))
        bottom10 = cat_review.head(10)
        colors_bad = sns.color_palette("Reds_r", n_colors=10)
        ax.barh(bottom10['product_category_name_english'][::-1],
                bottom10['avg_review'][::-1], color=colors_bad)
        ax.axvline(x=filtered['review_score'].mean(), color='green',
                    linestyle='--', linewidth=1.5, label=f'Rata-rata: {filtered["review_score"].mean():.2f}')
        ax.set_title('10 Kategori dengan Review Score Terendah', fontweight='bold', fontsize=12)
        ax.set_xlabel('Rata-rata Review Score', fontsize=10)
        ax.set_xlim(1, 5)
        ax.legend(fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Korelasi scatter
    st.markdown("**📉 Korelasi Delivery Time vs Review Score**")
    sample_data = filtered_copy[['delivery_days', 'review_score']].dropna()
    corr = sample_data.corr().loc['delivery_days', 'review_score']
    st.metric("Korelasi Pearson (delivery_days vs review_score)", f"{corr:.4f}",
               delta="Korelasi Negatif — semakin lama kirim, semakin rendah review")

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> Setiap tambahan 7 hari waktu pengiriman berkorelasi dengan penurunan ~0.2 poin review score. Kategori besar (furniture, peralatan rumah) adalah yang paling terdampak.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TAB 3: RFM SEGMENTASI
# ═══════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">👥 Segmentasi Pelanggan — RFM Analysis</div>', unsafe_allow_html=True)

    st.markdown('<div class="insight-box">🎯 <b>Pertanyaan Bisnis 3:</b> Bagaimana segmentasi pelanggan Olist berdasarkan perilaku pembelian (Recency, Frequency, Monetary), dan kelompok mana yang paling bernilai?</div>', unsafe_allow_html=True)

    seg_colors = {
        'Champions': '#4CAF50', 'Loyal Customers': '#8BC34A',
        'New Customers': '#03A9F4', 'Potential Loyalists': '#00BCD4',
        'Need Attention': '#FFC107', 'At Risk': '#FF9800',
        'Cant Lose Them': '#FF5722', 'Lost': '#9E9E9E'
    }

    seg_count = rfm_df['segment'].value_counts().reset_index()
    seg_count.columns = ['segment', 'count']
    seg_rev = rfm_df.groupby('segment')['monetary'].sum().reset_index()
    seg_rev.columns = ['segment', 'revenue']
    seg_merged = seg_count.merge(seg_rev, on='segment')
    seg_merged['avg_monetary'] = rfm_df.groupby('segment')['monetary'].mean().values

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(7, 6))
        colors_pie = [seg_colors.get(s, '#607D8B') for s in seg_count['segment']]
        wedges, texts, autotexts = ax.pie(
            seg_count['count'], labels=seg_count['segment'],
            colors=colors_pie, autopct='%1.1f%%', startangle=90, pctdistance=0.82
        )
        for t in texts: t.set_fontsize(8.5)
        for a in autotexts: a.set_fontsize(8)
        ax.set_title('Distribusi Pelanggan per Segmen', fontweight='bold', fontsize=12)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        seg_rev_sorted = seg_merged.sort_values('revenue', ascending=True)
        colors_bar = [seg_colors.get(s, '#607D8B') for s in seg_rev_sorted['segment']]
        fig, ax = plt.subplots(figsize=(7, 6))
        ax.barh(seg_rev_sorted['segment'], seg_rev_sorted['revenue'] / 1e6, color=colors_bar)
        for bar in ax.patches:
            ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2,
                    f'R${bar.get_width():.1f}M', va='center', fontsize=8.5)
        ax.set_title('Total Revenue per Segmen (Juta BRL)', fontweight='bold', fontsize=12)
        ax.set_xlabel('Total Revenue (Juta BRL)', fontsize=10)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    # Tabel detail segmen
    st.markdown("**📋 Detail Statistik per Segmen**")
    seg_detail = rfm_df.groupby('segment').agg(
        Jumlah_Pelanggan=('customer_unique_id', 'count'),
        Avg_Recency=('recency', 'mean'),
        Avg_Frequency=('frequency', 'mean'),
        Avg_Monetary=('monetary', 'mean'),
        Total_Revenue=('monetary', 'sum')
    ).round(1).reset_index().sort_values('Total_Revenue', ascending=False)
    seg_detail.columns = ['Segmen', 'Jumlah Pelanggan', 'Avg Recency (Hari)', 'Avg Frequency', 'Avg Monetary (BRL)', 'Total Revenue (BRL)']
    st.dataframe(seg_detail, use_container_width=True, hide_index=True)

    # RFM Distribution charts
    st.markdown("**📊 Distribusi RFM Score**")
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    sns.histplot(rfm_df['recency'], bins=30, ax=axes[0], color='#1565C0', kde=True)
    axes[0].set_title('Distribusi Recency', fontweight='bold')
    axes[0].set_xlabel('Hari')
    sns.histplot(rfm_df['frequency'], bins=20, ax=axes[1], color='#388E3C', kde=True)
    axes[1].set_title('Distribusi Frequency', fontweight='bold')
    axes[1].set_xlabel('Jumlah Transaksi')
    sns.histplot(rfm_df['monetary'], bins=30, ax=axes[2], color='#E65100', kde=True)
    axes[2].set_title('Distribusi Monetary', fontweight='bold')
    axes[2].set_xlabel('Total Belanja (BRL)')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> Segmen <b>Champions</b> hanya ~5% pelanggan namun berkontribusi ~20% revenue. Segmen <b>Lost</b> merupakan yang terbesar (>40%), menunjukkan perlunya program retensi dan loyalitas yang kuat.</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════
# TAB 4: GEOSPATIAL ANALYSIS
# ═══════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🗺️ Analisis Geospasial per Negara Bagian Brazil</div>', unsafe_allow_html=True)

    state_df = filtered.groupby('customer_state').agg(
        total_orders=('order_id', 'nunique'),
        total_revenue=('payment_value', 'sum'),
        avg_delivery=('delivery_days', 'mean'),
        avg_review=('review_score', 'mean')
    ).round(2).reset_index().sort_values('total_orders', ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        top15 = state_df.head(15)
        fig, ax = plt.subplots(figsize=(8, 6))
        colors_s = sns.color_palette('Blues_r', n_colors=15)
        ax.barh(top15['customer_state'][::-1], top15['total_orders'][::-1] / 1e3, color=colors_s)
        ax.set_title('Top 15 Negara Bagian: Volume Order', fontweight='bold', fontsize=12)
        ax.set_xlabel('Jumlah Order (Ribu)', fontsize=10)
        ax.set_ylabel('Negara Bagian', fontsize=10)
        for bar in ax.patches:
            ax.text(bar.get_width() + 0.1, bar.get_y() + bar.get_height()/2,
                    f'{bar.get_width():.1f}K', va='center', fontsize=8.5)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    with col2:
        fig, ax1 = plt.subplots(figsize=(8, 6))
        x = np.arange(len(top15))
        ax1.bar(x, top15['avg_delivery'], color='#FF8A65', alpha=0.8, label='Avg Delivery (Hari)', width=0.5)
        ax1.set_ylabel('Rata-rata Hari Pengiriman', fontsize=10, color='#BF360C')
        ax1.tick_params(axis='y', labelcolor='#BF360C')
        ax1.set_xticks(x)
        ax1.set_xticklabels(top15['customer_state'], rotation=45, ha='right', fontsize=9)
        ax2 = ax1.twinx()
        ax2.plot(x, top15['avg_review'], color='#1565C0', marker='D',
                  linewidth=2, markersize=7, label='Avg Review Score')
        ax2.set_ylabel('Rata-rata Review Score', fontsize=10, color='#1565C0')
        ax2.tick_params(axis='y', labelcolor='#1565C0')
        ax2.set_ylim(1, 5.5)
        ax1.set_title('Delivery Time & Review Score per Negara Bagian', fontweight='bold', fontsize=11)
        lines1, labs1 = ax1.get_legend_handles_labels()
        lines2, labs2 = ax2.get_legend_handles_labels()
        ax1.legend(lines1 + lines2, labs1 + labs2, loc='upper right', fontsize=9)
        plt.tight_layout()
        st.pyplot(fig)
        plt.close()

    st.markdown("**📊 Tabel Lengkap Data per Negara Bagian**")
    state_display = state_df.copy()
    state_display.columns = ['Negara Bagian', 'Total Order', 'Total Revenue (BRL)', 'Avg Delivery (Hari)', 'Avg Review']
    st.dataframe(state_display, use_container_width=True, hide_index=True)

    st.markdown('<div class="insight-box">💡 <b>Insight:</b> <b>São Paulo (SP)</b> mendominasi dengan >40% total pesanan. Negara bagian di kawasan Utara (AM, RR, AC) memiliki delivery time 2-3x lebih lama dibanding SP/RJ, yang berkorelasi langsung dengan review score lebih rendah.</div>', unsafe_allow_html=True)

# ─── FOOTER ──────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #78909C; font-size: 0.85rem;'>
    📊 Brazilian E-Commerce Dashboard | Dataset: Olist Public Dataset (Kaggle) |
    Dibuat dengan ❤️ menggunakan Streamlit & Matplotlib
</div>
""", unsafe_allow_html=True)
