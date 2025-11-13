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
        This project focuses on defect analysis in the manufacturing industry. 
        The data used includes information on defect type, severity, inspection method, defect location, and repair costs. 
        This data can be used to analyze defect patterns, improve quality control processes, and assess the impact of defects on product quality and production costs.
      
       **Objectives 🎯:**
        - Analyze production defect patterns (EDA).
        - Create a prediction model for defect severity.
        - Create a prediction model for repair costs.
    """)
   
    # Load CSV
    file_path = "defect_data.csv"
    df = pd.read_csv(file_path)
    df.columns = df.columns.str.lower()

    # Ringkasan Data
    st.subheader("Data Summary")
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
    missing_text = "- There are no missing values → `All complete`." if total_missing_clean == 0 else f"There is {total_missing_clean} missing value after cleaning."

    # Tampilkan ringkasan dalam satu blok narasi
    summary_text = f"""
    - Number data : `{rows_before} Rows`, `{cols_before} Columns`.  
    - Number of duplicate rows removed: `{rows_removed} Rows`.  
    
    {missing_text}  
    - Columns `defect_date` has been changed from type `object` to `datetime`.
    """
    st.markdown(summary_text)
    # Pastikan kolom tanggal berformat datetime
    df_clean["defect_date"] = pd.to_datetime(df_clean["defect_date"], errors="coerce")
    df_valid = df_clean.dropna(subset=["defect_date"])
    df_valid["month"] = df_valid["defect_date"].dt.to_period("M")
    
    # EDA Interaktif
    st.subheader("Exploratory Data Analysis 📈")

    eda_option = st.selectbox("Select Analysis:", [
        "Trends in Defect Types",
        "Trends in Severty",
        "Trends in Inspection Methods",
        "Trends in Defect Locations",
        "Boxplot of Repair Costs"
    ])


    if eda_option == "Trends in Defect Types" and "defect_type" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "defect_type"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Trend in Number of Defects per Defect Type")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Defects")
        

        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,5), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8)
        
        ax.legend(title="Defect Type")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Trends in Severty" and "severity" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "severity"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.text(x, y, str(y), fontsize=8, ha='center', va='bottom')
        
        ax.set_title("Trends in Number of Defects Severity Level")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Defects")
        plt.xticks(rotation=45)
        ax.legend(title="Severity Level")
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Trends in Inspection Methods" and "inspection_method" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "inspection_method"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Trends in Inspection Methods")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Cases")
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,7), textcoords='offset points',
                            ha='center', va='center', fontsize=8)
        ax.legend(title="Inspection Method")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)

    elif eda_option == "Trends in Defect Location" and "defect_location" in df_clean.columns:
        trend_df = df_valid.groupby(["month", "defect_location"]).size().unstack(fill_value=0)
        fig, ax = plt.subplots(figsize=(10,5))
        
        ax.set_title("Trends in Defect Locations")
        ax.set_xlabel("Month")
        ax.set_ylabel("Number of Cases")
        
        for col in trend_df.columns:
            ax.plot(trend_df.index.astype(str), trend_df[col], marker="o", label=col)
            for x, y in zip(trend_df.index.astype(str), trend_df[col]):
                ax.annotate(str(y), xy=(x, y), xytext=(0,5), textcoords='offset points',
                            ha='center', va='bottom', fontsize=8)
        
        ax.legend(title="Defect Location")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)


    elif eda_option == "Boxplot of Repair Cost" and "repair_cost" in df_clean.columns:
        fig, ax = plt.subplots(figsize=(8,4))
        sns.boxplot(data=df_clean, y="repair_cost", ax=ax)
        ax.set_title("Distribution of Repair Costs")
        ax.set_ylabel("Repair Costs : (Rp).")
        median = df_clean["repair_cost"].median()
        ax.axhline(median, color='red', linestyle='--')
        ax.text(0, median + median*0.02, f'Median: Rp. {median:,.0f}', color='red')
        st.pyplot(fig)
        plt.close(fig)
        st.write(f"- Average Repair Cost : Rp. {df_clean['repair_cost'].mean():,.0f}")
        st.write(f"- Median Repair Cost : Rp. {median:,.0f}")
        st.write(f"- Highest Repair Costs : Rp. {df_clean['repair_cost'].max():,.0f}")
        st.write(f"- Repair Costs : Rp. {df_clean['repair_cost'].min():,.0f}")
    