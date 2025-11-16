import streamlit as st
import pandas as pd

st.set_page_config(page_title="MHT CET College Predictor", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("final_clean_dataset.csv")

df = load_data()

st.title("🎓 MHT-CET College Predictor (Cutoff Based)")
st.write("Predict eligible engineering colleges based on Percentile, Category, and Branch.")

# Inputs
percentile = st.number_input("Enter Your Percentile", min_value=0.0, max_value=100.0, value=90.0)

category = st.selectbox(
    "Select Category",
    sorted(df["Category"].unique())
)

branch = st.selectbox(
    "Select Branch",
    sorted(df["Branch"].unique())
)

# Prediction function
def predict_colleges(percentile, category, branch):
    filt = df[
        (df["Category"] == category) &
        (df["Branch"] == branch)
    ]

    eligible = filt[filt["Percentile"] <= percentile]
    eligible = eligible.sort_values(by="Percentile", ascending=False)

    # Add chance level
    def chance(student_p, cutoff_p):
        diff = student_p - cutoff_p
        if diff >= 5:
            return "🟢 SAFE"
        elif diff >= 0:
            return "🟡 POSSIBLE"
        else:
            return "🔴 RISKY"

    eligible["Chance"] = eligible["Percentile"].apply(lambda x: chance(percentile, x))

    return eligible

# Run prediction
if st.button("Predict Colleges"):
    result = predict_colleges(percentile, category, branch)
    
    if result.empty:
        st.error("No colleges found for this percentile.")
    else:
        st.success(f"Found {len(result)} eligible colleges!")
        st.dataframe(result[["College", "Branch", "Category", "Percentile", "Chance"]])
