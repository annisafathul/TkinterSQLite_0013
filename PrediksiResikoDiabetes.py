import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "prediksi_diabetes.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pasien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_pasien TEXT NOT NULL,
            usia INTEGER NOT NULL,
            gula_darah REAL NOT NULL,
            bmi REAL NOT NULL,
            riwayat_ortu TEXT NOT NULL,
            hasil_prediksi TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()

def prediksi_diabetes(gula_darah, bmi, riwayat_ortu):
    if gula_darah >= 200:
        if riwayat_ortu == "Ya":
            return (
                "Risiko Sangat Tinggi (Indikasi Diabetes + Genetik)",
                "#ff5555"
            )
        else:
            return (
                "Risiko Tinggi (Indikasi Diabetes)",
                "#ff5555"
            )

    elif 140 <= gula_darah < 200:
        if riwayat_ortu == "Ya" or bmi >= 30:
            return (
                "Risiko Tinggi (Prediabetes + Genetik/Obesitas)",
                "#e66220"
            )
        else:
            return (
                "Risiko Sedang (Prediabetes)",
                "#f2830b"
            )

    else:
        if bmi >= 30:
            if riwayat_ortu == "Ya":
                return (
                    "Risiko Sedang (Normal + Obesitas & Genetik)",
                    "#ffb86c"
                )
            else:
                return (
                    "Risiko Waspada (Normal + Obesitas)",
                    "#ffb86c"
                )
        else:
            if riwayat_ortu == "Ya":
                return (
                    "Risiko Waspada (Gula Normal + Riwayat Genetik)",
                    "#ffb86c"
                )
            else:
                return (
                    "Risiko Rendah (Normal)",
                    "#5094fa"
                )

