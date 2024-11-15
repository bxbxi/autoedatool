import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import warnings  # Uyarıları bastırmak için

# Uyarıları kapat
warnings.filterwarnings("ignore")

# Streamlit sayfa ayarları
st.set_page_config(
    page_title="Neon EDA Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Neon tema
neon_theme = """
    <style>
    body {
        background-color: #121212;
        color: #FFFFFF;
    }
    .stButton>button {
        background-color: #282828;
        color: #0ff0fc;
        border: 1px solid #0ff0fc;
    }
    .stSidebar {
        background-color: #181818;
        color: #FFFFFF;
    }
    .css-1d391kg p {
        color: #FFFFFF;
    }
    </style>
"""
st.markdown(neon_theme, unsafe_allow_html=True)

# Başlık
st.title("🚀 Neon ve Lacivert Temalı Gelişmiş EDA Dashboard")

# Veri yükleme
uploaded_file = st.sidebar.file_uploader("Bir CSV dosyası yükleyin", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("✅ Dosya başarıyla yüklendi!")
    st.write("### Verinin İlk 10 Satırı:")
    st.write(df.head(10))

    # 1. Temel Bilgiler
    with st.expander("📋 Veri Bilgisi"):
        st.write("🔹 **Boyut**: ", df.shape)
        st.write("🔹 **Sütun Türleri**:")
        st.write(df.dtypes)

    # 2. Temel İstatistikler
    with st.expander("📊 Temel İstatistikler"):
        st.write(df.describe(include="all").transpose())

    # 3. Eksik Veri Analizi
    with st.expander("❓ Eksik Veri Analizi"):
        missing = df.isnull().sum()
        st.write(missing[missing > 0] if missing.sum() > 0 else "❌ Eksik veri yok!")
        handle_missing = st.selectbox("Eksik verilerle ne yapmak istersiniz?", ["Hiçbir şey", "Sil", "Doldur (Ortalama)"])
        if handle_missing == "Sil":
            df = df.dropna()
            st.write("Eksik veriler silindi.")
        elif handle_missing == "Doldur (Ortalama)":
            df = df.fillna(df.mean())
            st.write("Eksik veriler dolduruldu.")

    # 4. Veri Görselleştirme
    # Histogram
    with st.expander("🔹 Histogram"):
        if not df.select_dtypes(include=["int64", "float64"]).columns.empty:
            selected_column = st.selectbox("Histogram için bir sütun seçin:",
                                           df.select_dtypes(include=["int64", "float64"]).columns)
            if selected_column:
                st.write(f"### {selected_column} Histogramı")
                fig, ax = plt.subplots(facecolor="#121212")
                sns.histplot(df[selected_column], kde=True, ax=ax, color="cyan")
                ax.set_facecolor("#121212")
                st.pyplot(fig)
        else:
            st.write("⚠️ Sayısal sütun bulunamadı, histogram oluşturulamadı!")

    # Boxplot
    with st.expander("🔹 Boxplot"):
        if not df.select_dtypes(include=["int64", "float64"]).columns.empty:
            selected_column = st.selectbox("Boxplot için bir sütun seçin:",
                                           df.select_dtypes(include=["int64", "float64"]).columns, key="boxplot")
            if selected_column:
                st.write(f"### {selected_column} Kutu Grafiği")
                fig, ax = plt.subplots(facecolor="#121212")
                sns.boxplot(x=df[selected_column], ax=ax, color="cyan")
                ax.set_facecolor("#121212")
                st.pyplot(fig)
        else:
            st.write("⚠️ Sayısal sütun bulunamadı, boxplot oluşturulamadı!")

    # Korelasyon Matrisi
    with st.expander("🔹 Korelasyon Matrisi"):
        if not df.select_dtypes(include=["int64", "float64"]).columns.empty:
            st.write("Verinin sayısal sütunları arasındaki korelasyon matrisi.")
            if len(df.select_dtypes(include=["int64", "float64"]).columns) > 1:
                fig, ax = plt.subplots(figsize=(10, 6), facecolor="#121212")
                sns.heatmap(
                    df.select_dtypes(include=["int64", "float64"]).corr(),
                    annot=True,
                    cmap="coolwarm",
                    ax=ax,
                    linewidths=0.5,
                )
                ax.set_facecolor("#121212")
                st.pyplot(fig)
            else:
                st.write("⚠️ Korelasyon matrisi için yeterli sayısal sütun yok.")
        else:
            st.write("⚠️ Sayısal sütun bulunamadı, korelasyon matrisi oluşturulamadı!")

    # Dağılım Grafiği
    with st.expander("🔹 Dağılım Grafiği"):
        num_cols = df.select_dtypes(include=["int64", "float64"]).columns
        if len(num_cols) >= 2:
            col1 = st.selectbox("X ekseni için sütun seçin:", num_cols, key="scatter_x")
            col2 = st.selectbox("Y ekseni için sütun seçin:", num_cols, key="scatter_y")
            if col1 and col2:
                st.write(f"### {col1} ve {col2} Arasındaki Dağılım")
                fig, ax = plt.subplots(facecolor="#121212")
                sns.scatterplot(x=df[col1], y=df[col2], ax=ax, color="cyan")
                ax.set_facecolor("#121212")
                st.pyplot(fig)
        else:
            st.write("⚠️ Dağılım grafiği için en az 2 sayısal sütun gereklidir.")
