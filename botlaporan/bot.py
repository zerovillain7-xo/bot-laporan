import os
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("8611942129:AAHZD97OSsFHouhL4f3miPxd5PFsv35skhA")

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)
sheet = client.open("NamaSheetKamu").sheet1

def ambil(pattern, text):
    hasil = re.search(pattern, text)
    return hasil.group(1).strip() if hasil else ""

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if "REPORT INSTALASI BARU IKR" not in text:
        return

    data = [
        ambil(r"Hari, Tanggal:\s*(.*)", text),
        ambil(r"Nama Team:\s*(.*)", text),
        ambil(r"Nama Teknisi:\s*(.*)", text),
        ambil(r"Nama Pelanggan:(.*)", text),
        ambil(r"ID Pelanggan:(.*)", text),
        ambil(r"Nomor HP:(.*)", text),
        ambil(r"Desa/Kelurahan:(.*)", text),
        ambil(r"Kecamatan:(.*)", text),
        ambil(r"Kabupaten/Kota:(.*)", text),
        ambil(r"Type WO:(.*)", text),
        ambil(r"Status:(.*)", text),
        ambil(r"Merk ONT:(.*)", text),
        ambil(r"MAC:(.*)", text),
        ambil(r"SN:(.*)", text),
        ambil(r"PORT:(.*)", text),
        ambil(r"Kecepatan Internet:(.*)", text),

        # Material
        ambil(r"Kabel Precon:(.*)", text),
        ambil(r"Cable Marker:(.*)", text),
        ambil(r"Cable Ties:(.*)", text),
        ambil(r"Clamp:(.*)", text),
        ambil(r"S Clamp:(.*)", text),
        ambil(r"Isolasi:(.*)", text),
        ambil(r"Paku Beton:(.*)", text),

        # Koordinat
        ambil(r"Tikor Pelanggan:(.*)", text),
        ambil(r"Tikor ODP:(.*)", text),
    ]

    sheet.append_row(data)

    await update.message.reply_text("✅ Laporan lengkap berhasil masuk Google Sheets!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT, handle))
app.run_polling()
