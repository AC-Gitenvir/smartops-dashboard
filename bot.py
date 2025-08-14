import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import streamlit as st

# Replace this with your actual Telegram bot token
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"

# --- Telegram Bot Command ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Hello Ayush! Your Streamlit-integrated bot is now live!")

# --- Function to Run Bot ---
async def run_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    await app.run_polling()

# --- Streamlit Interface ---
st.title("🤖 Telegram Bot Controller")
st.write("Click the button below to start the bot. Then open Telegram and type `/start` to test it.")

if st.button("Start Telegram Bot"):
    st.write("🚀 Launching bot... please wait...")

    try:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        loop.create_task(run_bot())
        st.success("✅ Bot started! Now open your Telegram and use /start.")
    except Exception as e:
        st.error(f"❌ Bot failed: {e}")
