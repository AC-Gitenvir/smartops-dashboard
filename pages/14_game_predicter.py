# pages/14_game_predicter.py (Optimized for Streamlit)

import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import altair as alt

# --- Caching Functions for Efficiency ---

# @st.cache_data runs this function only once to load the data.
@st.cache_data
def get_data():
    """Creates and returns the training dataset."""
    data = {
        "Active_Players": [100000, 150000, 200000, 250000, 300000, 350000, 400000],
        "Avg_Session_Time": [35, 40, 50, 55, 60, 65, 70],
        "Purchase_Rate": [0.12, 0.15, 0.18, 0.22, 0.25, 0.28, 0.30],
        "Marketing_Spend": [20000, 30000, 40000, 50000, 60000, 70000, 80000],
        "Genre": [1, 2, 3, 1, 2, 3, 1],
        "Server_Cost": [5000, 6000, 8000, 9000, 10000, 12000, 14000],
        "Budget": [150000, 220000, 300000, 360000, 430000, 500000, 580000]
    }
    return pd.DataFrame(data)

# @st.cache_resource runs this function only once to train the model.
# This prevents the model from retraining every time you move a slider.
@st.cache_resource
def train_model(df):
    """Trains the Linear Regression model and returns it along with test data."""
    X = df[["Active_Players", "Avg_Session_Time", "Purchase_Rate", "Marketing_Spend", "Genre", "Server_Cost"]]
    y = df["Budget"]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    return model, X_test, y_test

# --- Main App UI ---

# Title and description
st.title("🎮 Online Game Budget Predictor")
st.write("""
This app uses a cached Linear Regression model to predict the **monthly budget** of an online game based on its key metrics.
""")

# Load data and train model using the efficient cached functions
df = get_data()
model, X_test, y_test = train_model(df)

# Get predictions for the test set to evaluate performance
y_pred = model.predict(X_test)

# --- User Input in Sidebar ---
st.sidebar.header("🔧 Input Game Features")
players = st.sidebar.number_input("Active Players", 10000, 1000000, 280000, step=10000)
session = st.sidebar.slider("Avg. Session Time (min)", 10, 120, 58)
purchase = st.sidebar.slider("Purchase Rate", 0.0, 1.0, 0.24)
marketing = st.sidebar.number_input("Marketing Spend (₹)", 0, 200000, 55000, step=1000)
# Use format_func for a cleaner selectbox: shows the name, but returns the number.
genre = st.sidebar.selectbox(
    "Game Genre",
    options=[1, 2, 3], 
    format_func=lambda x: {"1": "Action", "2": "Puzzle", "3": "RPG"}.get(str(x))
)
server = st.sidebar.number_input("Server Cost (₹)", 0, 50000, 9500, step=100)

# --- Prediction and Results ---

# Predict based on user input
input_features = np.array([[players, session, purchase, marketing, genre, server]])
predicted_budget = model.predict(input_features)[0]

# Display prediction
st.subheader("💰 Predicted Monthly Budget")
st.success(f"₹ {int(predicted_budget):,}")

# Evaluation metrics using st.metric for a better look
st.subheader("📊 Model Performance")
col1, col2 = st.columns(2)
with col1:
    st.metric("R² Score", f"{r2_score(y_test, y_pred):.2f}")
with col2:
    st.metric("Mean Squared Error", f"{mean_squared_error(y_test, y_pred):,.0f}")

# --- Interactive Chart with Altair ---
st.subheader("📈 Actual vs. Predicted Budget (Interactive)")

# Create a DataFrame for plotting
chart_data = pd.DataFrame({
    'Actual Budget': y_test,
    'Predicted Budget': y_pred
})

# Create the scatter plot
scatter = alt.Chart(chart_data).mark_circle(size=100, opacity=0.8).encode(
    x=alt.X('Actual Budget', scale=alt.Scale(zero=False)),
    y=alt.Y('Predicted Budget', scale=alt.Scale(zero=False)),
    tooltip=['Actual Budget', 'Predicted Budget']
).interactive()

# Create the reference line (y=x)
line = alt.Chart(pd.DataFrame({'x': [y_test.min(), y_test.max()], 'y': [y_test.min(), y_test.max()]})).mark_line(
    color='red',
    strokeDash=[5, 5]
).encode(x='x', y='y')

# Combine and display the chart
st.altair_chart(scatter + line, use_container_width=True)

# Show raw data
with st.expander("📄 Show Training Dataset"):
    st.dataframe(df)
