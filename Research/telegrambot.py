import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Konfigurasi
BOT_TOKEN = "contoh" # Sesuaikan dengan token dari bot telegram anda
FLASK_SERVER_URL = "http://192.168.0.0:5000/temperature"  # Sesuaikan dengan IP Komputer yang menjalankan flask


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Halo! Saya adalah bot iTCLab.\n"
        "Gunakan /temperature untuk mengecek suhu saat ini."
    )


async def get_temperature(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        response = requests.get(FLASK_SERVER_URL)
        logger.info(f"Response from server: {response.text}")

        if response.status_code == 200:
            data = response.json()
            temperature = data.get("temperature")
            if temperature is not None:
                await update.message.reply_text(f"Suhu saat ini adalah {temperature}°C")
            else:
                await update.message.reply_text("Data suhu belum tersedia")
        else:
            await update.message.reply_text(f"Gagal mengambil data suhu. Status code: {response.status_code}")

    except requests.RequestException as e:
        logger.error(f"Network error: {e}")
        await update.message.reply_text("Gagal terhubung ke server suhu")
    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text("Terjadi kesalahan saat mengambil data suhu")


def main():
    try:
        application = Application.builder().token(BOT_TOKEN).build()

        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("temperature", get_temperature))

        logger.info("Starting bot...")
        application.run_polling()

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == '__main__':
    main()
