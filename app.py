import streamlit as st
import requests
import pandas as pd

st.title("🛒 Novelty Item Purchase Predictor")


# --- Send to API ---
api_url = "http://128.203.123.76/predict-novelty-time"  # 🔁 Replace with your real external IP
# --- User Input ---
hour = st.slider("Hour of Day", 0, 23, 12)
day = st.selectbox("Day of the Week", ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])

# --- Convert day to int and add user_id ---
day_map = {"Sun": 0, "Mon": 1, "Tue": 2, "Wed": 3, "Thu": 4, "Fri": 5, "Sat": 6}
day_int = day_map[day]
payload = {"user_id": 1, "hour": hour, "day": day_int}

try:
    response = requests.post(api_url, json=payload)
    st.write("Status Code:", response.status_code)
    st.write("Raw Response:", response.text)
    
    try:
        prediction = response.json().get("novelty_probability", None)
        if prediction is not None:
            st.success(f"Novelty Purchase Probability: **{prediction:.2%}**")
        else:
            st.warning("No prediction returned.")
    except Exception as e:
        st.error(f"Failed to parse API response: {e}")

except Exception as e:
    st.error(f"API error: {e}")

# --- Load and Combine Datasets ---
@st.cache_data
def load_data():
    df1 = pd.read_csv("cleaned_dataset_part1.csv")
    df2 = pd.read_csv("cleaned_dataset_part2.csv")
    df = pd.concat([df1, df2], ignore_index=True)
    return df

df = load_data()

# --- Create Novelty Flag ---
df["novelty"] = (df["reordered"] == 0).astype(int)

# --- Convert day numbers to names ---
dow_map = {0: "Sun", 1: "Mon", 2: "Tue", 3: "Wed", 4: "Thu", 5: "Fri", 6: "Sat"}
df["day_name"] = df["order_dow"].map(dow_map)

# --- Visualizations ---
st.subheader("📊 Average Novelty Purchase Rate by Hour of Day")
hourly = df.groupby("order_hour_of_day")["novelty"].mean()
st.bar_chart(hourly)

st.subheader("📈 Average Novelty Purchase Rate by Day of Week")
daily = df.groupby("day_name")["novelty"].mean().reindex(["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
st.line_chart(daily)

st.subheader("Heatmap: Novelty Rate by Hour and Day")
heatmap_data = df.pivot_table(
    index="day_name",
    columns="order_hour_of_day",
    values="novelty",
    aggfunc="mean"
).reindex(index=["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"])
st.dataframe(heatmap_data.style.background_gradient(cmap="Greens"))
