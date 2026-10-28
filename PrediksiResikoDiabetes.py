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
