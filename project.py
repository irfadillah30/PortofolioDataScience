# project.py
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

def project():
    # Judul dan deskripsi project
    st.title("Predictive Maintenance & Quality Control in Manufacturing Industry")
    st.subheader("By: Irfadillah Afni Nurvita")
    st.markdown("""
        Proyek ini berfokus pada **analisis cacat produksi** di industri manufaktur. Data yang digunakan mencakup informasi tentang jenis cacat, tingkat keparahan, 
        metode inspeksi, lokasi cacat, serta biaya perbaikan data ini dapat digunakan untuk menganalisis pola cacat,
        meningkatkan proses pengendalian kualitas, dan menilai dampak cacat terhadap kualitas produk dan biaya produksi.  

       **Tujuan  🎯 :**
        - Menganalisis pola cacat produksi (EDA).
        - Membuat model prediksi **tingkat keparahan** cacat.
        - Membuat model prediksi **biaya perbaikan**.
    """)
   
    # Load CSV
    file_path = "defect_data.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    # Ringkasan Data
    st.subheader("Ringkasan Data")
    rows_before = df.shape[0]
    cols_before = df.shape[1]

    # Hitung duplikat
    df_clean = df.drop_duplicates()
    rows_after = df_clean.shape[0]
    rows_removed = rows_before - rows_after

    # Isi missing
    for col in df_clean.select_dtypes(include=['object']).columns:
        df_clean[col] = df_clean[col].fillna('Unknown')
    for col in df_clean.select_dtypes(include=['int64','float64']).columns:
        df_clean[col] = df_clean[col].fillna(df_clean[col].median())

    # Ubah defect_date ke datetime
    if "defect_date" in df_clean.columns:
        df_clean["defect_date"] = pd.to_datetime(df_clean["defect_date"], errors="coerce")

    # Hitung missing setelah cleaning
    total_missing_clean = df_clean.isna().sum().sum()
    missing_text = "- Tidak ada missing value → `semua lengkap`." if total_missing_clean == 0 else f"Terdapat {total_missing_clean} missing value setelah cleaning."

    # Tampilkan ringkasan dalam satu blok narasi
    summary_text = f"""
    - Jumlah data : `{rows_before} baris`, `{cols_before} kolom`.  
    - Baris duplikat yang dihapus : `{rows_removed} baris`.  
    
    {missing_text}  
    - Kolom `defect_date` telah diubah dari tipe `object` ke `datetime`.
    """
    st.markdown(summary_text)
    # Pastikan kolom tanggal berformat datetime
    df_clean["defect_date"] = pd.to_datetime(df_clean["defect_date"], errors="coerce")
    df_valid = df_clean.dropna(subset=["defect_date"])
    df_valid["month"] = df_valid["defect_date"].dt.to_period("M")
    
    # EDA Interaktif
    st.subheader("Exploratory Data Analysis 📈")

    eda_option = st.selectbox("Pilih Analisis:", [
        "Tren Jenis Cacat",
        "Tren Tingkat Keparahan",
        "Tren Metode Inspeksi",
        "Tren Lokasi Cacat",
        "Boxplot Biaya Perbaikan"
    ])


    if eda_option == "Tren Jenis Cacat" and "defect_type" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "defect_type"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Tren Jumlah Cacat per Jenis Cacat")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Cacat")
        

        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,5), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8)
        
        ax.legend(title="Jenis Cacat")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Tren Tingkat Keparahan" and "severity" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "severity"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.text(x, y, str(y), fontsize=8, ha='center', va='bottom')
        
        ax.set_title("Tren Jumlah Cacat per Tingkat Keparahan")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Cacat")
        plt.xticks(rotation=45)
        ax.legend(title="Tingkat Keparahan")
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Tren Metode Inspeksi" and "inspection_method" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "inspection_method"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Tren Metode Inspeksi")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Kasus")
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,7), textcoords='offset points',
                            ha='center', va='center', fontsize=8)
        ax.legend(title="Metode Inspeksi")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

    elif eda_option == "Tren Lokasi Cacat" and "defect_location" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "defect_location"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Tren Lokasi Cacat")
        ax.set_xlabel("Bulan")
        ax.set_ylabel("Jumlah Kasus")
        
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,5), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8)
        
        ax.legend(title="Lokasi Cacat")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Boxplot Biaya Perbaikan" and "repair_cost" in df_clean.columns:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.boxplot(data=df_clean, y="repair_cost", ax=ax)
        ax.set_title("Distribusi Biaya Perbaikan")
        ax.set_ylabel("Biaya Perbaikan (Rp)")
        median = df_clean["repair_cost"].median()
        ax.axhline(median, color='red', linestyle='--')
        ax.text(0, median + median*0.02, f'Median: Rp. {median:,.0f}', color='red')
        st.pyplot(fig)
        plt.close(fig)
        st.write(f"- Rata-rata Biaya Perbaikan: Rp. {df_clean['repair_cost'].mean():,.0f}")
        st.write(f"- Median Biaya Perbaikan: Rp. {median:,.0f}")
        st.write(f"- Biaya Perbaikan Tertinggi: Rp. {df_clean['repair_cost'].max():,.0f}")
        st.write(f"- Biaya Perbaikan Terendah: Rp. {df_clean['repair_cost'].min():,.0f}")
    