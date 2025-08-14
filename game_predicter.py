import streamlit as st
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# Title and description
st.title("🎮 Online Game Budget Predictor")
st.write("""
This app uses Linear Regression to predict the **monthly budget** of an online game based on:
- Active players
- Session time
- Purchase rate
- Marketing spend
- Genre (1: Action, 2: Puzzle, 3: RPG)
- Server cost
""")

# Create the dataset
data = {
    "Active_Players": [100000, 150000, 200000, 250000, 300000, 350000, 400000],
    "Avg_Session_Time": [35, 40, 50, 55, 60, 65, 70],
    "Purchase_Rate": [0.12, 0.15, 0.18, 0.22, 0.25, 0.28, 0.30],
    "Marketing_Spend": [20000, 30000, 40000, 50000, 60000, 70000, 80000],
    "Genre": [1, 2, 3, 1, 2, 3, 1],
    "Server_Cost": [5000, 6000, 8000, 9000, 10000, 12000, 14000],
    "Budget": [150000, 220000, 300000, 360000, 430000, 500000, 580000]
}
df = pd.DataFrame(data)

# Train model
X = df[["Active_Players", "Avg_Session_Time", "Purchase_Rate", "Marketing_Spend", "Genre", "Server_Cost"]]
y = df["Budget"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
model = LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Input from user
st.sidebar.header("🔧 Input Game Features")
players = st.sidebar.number_input("Active Players", 10000, 1000000, 280000, step=10000)
session = st.sidebar.slider("Avg. Session Time (min)", 10, 120, 58)
purchase = st.sidebar.slider("Purchase Rate", 0.0, 1.0, 0.24)
marketing = st.sidebar.number_input("Marketing Spend (₹)", 0, 200000, 55000, step=1000)
genre = st.sidebar.selectbox("Game Genre", [("Action", 1), ("Puzzle", 2), ("RPG", 3)])
server = st.sidebar.number_input("Server Cost (₹)", 0, 50000, 9500, step=100)

# Predict
input_features = np.array([[players, session, purchase, marketing, genre[1], server]])
predicted_budget = model.predict(input_features)[0]

# Display prediction
st.subheader("💰 Predicted Monthly Budget")
st.success(f"₹ {int(predicted_budget):,}")

# Evaluation metrics
st.subheader("📊 Model Performance")
st.write(f"**R² Score**: {r2_score(y_test, y_pred):.2f}")
st.write(f"**Mean Squared Error**: {mean_squared_error(y_test, y_pred):,.0f}")

# Graph
st.subheader("📈 Actual vs Predicted Budget")
fig, ax = plt.subplots()
sns.scatterplot(x=y_test, y=y_pred, s=100, color="skyblue", ax=ax)
ax.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
ax.set_xlabel("Actual Budget")
ax.set_ylabel("Predicted Budget")
st.pyplot(fig)

# Show raw data
with st.expander("📄 Show Training Dataset"):
    st.dataframe(df)
