import pandas as pd
import streamlit as st
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
import joblib

# -----------------------
# Baca data
# -----------------------
file_path = "defect_data.csv"
df = pd.read_csv(file_path)
df.columns = df.columns.str.lower()

# Tambahkan bulan & tahun
if "defect_date" in df.columns:
    df['defect_date'] = pd.to_datetime(df['defect_date'], errors='coerce')
    df['month'] = df['defect_date'].dt.month
    df['year'] = df['defect_date'].dt.year

# -----------------------
# Fungsi training severity
# -----------------------
def train_severity_model():
    features = ["defect_type", "defect_location", "inspection_method"]
    target = "severity"
    X = df[features].copy()
    y = df[target].copy()
    encoders = {}
    for col in features + [target]:
        le = LabelEncoder()
        if col == target:
            y = le.fit_transform(y)
        else:
            X[col] = le.fit_transform(X[col])
        encoders[col] = le
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, "severity_model.pkl")
    joblib.dump(encoders, "severity_encoders.pkl")
    return model, encoders

# -----------------------
# Fungsi training repair
# -----------------------
def train_repair_model():
    features = ["defect_type", "defect_location", "inspection_method", "severity"]
    target = "repair_cost"
    X = df[features].copy()
    y = df[target].copy()
    encoders = {}
    for col in features:
        if X[col].dtype == "object":
            le = LabelEncoder()
            X[col] = le.fit_transform(X[col])
            encoders[col] = le
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    joblib.dump(model, "repair_model.pkl")
    joblib.dump(encoders, "repair_encoders.pkl")
    return model, encoders

# -----------------------
# Fungsi prediksi interaktif
# -----------------------
def prediction():
    st.subheader("Predicted Severity & Repair Costs")

    # ---------------- Load / Train Model ----------------
    try:
        model_sev = joblib.load("severity_model.pkl")
        encoders_sev = joblib.load("severity_encoders.pkl")
    except:
        model_sev, encoders_sev = train_severity_model()

    try:
        model_repair = joblib.load("repair_model.pkl")
        encoders_repair = joblib.load("repair_encoders.pkl")
    except:
        model_repair, encoders_repair = train_repair_model()

    # ---------------- Pilihan interaktif ----------------
    defect_options = df['defect_type'].unique()
    location_options = df['defect_location'].unique()
    month_options = list(range(1, 13))
    year_options = sorted(df['year'].dropna().unique())
    
    # Tambahkan simulasi tahun depan
    current_year = pd.Timestamp.now().year
    for y in range(current_year, current_year + 3):
        if y not in year_options:
            year_options.append(y)
    year_options = sorted(year_options)

    selected_defect = st.selectbox("Select the defect type:", defect_options)
    selected_location = st.selectbox("Select the Location Of the Defect:", location_options)
    selected_month = st.selectbox("Month Options:", month_options)
    selected_year = st.selectbox("Year Options:", year_options)

    if st.button("Prediksi"):
        # Filter data sesuai pilihan user
        df_sample = df[(df['defect_type'] == selected_defect) &
                       (df['defect_location'] == selected_location) &
                       (df['month'] == selected_month) &
                       (df['year'] == selected_year)]

        if df_sample.empty:
            st.warning("Performing Simulation Predictions.")
            # Buat 1 baris dummy untuk prediksi
            df_sample = pd.DataFrame([{
                "defect_type": selected_defect,
                "defect_location": selected_location,
                "inspection_method": df['inspection_method'].mode()[0],
                "severity": df['severity'].mode()[0]
            }])

       # ================= Prediksi Severity =================
        features_sev = ["defect_type", "defect_location", "inspection_method"]
        sample_sev = df_sample[features_sev].copy()
        for col in features_sev:
            sample_sev[col] = encoders_sev[col].transform(sample_sev[col])
        pred_sev = model_sev.predict(sample_sev)
        # Transform prediksi kembali ke kategori asli
        pred_sev_labels = encoders_sev['severity'].inverse_transform(pred_sev)
        df_sample['predicted_severity'] = pred_sev_labels

        # Hitung jumlah per kategori severity
        severity_counts = df_sample['predicted_severity'].value_counts()

        # ================= Prediksi Repair Cost =================
        features_repair = ["defect_type", "defect_location", "inspection_method", "severity"]
        sample_repair = df_sample[features_repair].copy()
        for col in features_repair:
            if col in encoders_repair:
                sample_repair[col] = encoders_repair[col].transform(sample_repair[col])
            elif col == "severity":
                le = encoders_sev["severity"]
                sample_repair[col] = le.transform(sample_repair[col])
        pred_repair = model_repair.predict(sample_repair)
        df_sample['predicted_repair_cost'] = pred_repair
        total_cost = df_sample['predicted_repair_cost'].sum()

        # ================= Tampilkan Hasil =================
        st.subheader("Prediction Results")
        st.write(f"Number of Cases : **{len(df_sample)}**")
        
        st.write("Severity Levels (per kategori) :")
        for sev, count in severity_counts.items():
            st.write(f"- {sev} : {count} Cases")
        
        st.write(f"Total Repair Costs : **Rp. {total_cost:,.0f}**")