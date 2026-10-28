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

def tambah_pasien(nama, usia, gula, bmi, riwayat, hasil):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pasien
        (nama_pasien, usia, gula_darah, bmi,
         riwayat_ortu, hasil_prediksi)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (nama, usia, gula, bmi, riwayat, hasil))

    conn.commit()
    conn.close()

def get_pasien():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nama_pasien, usia, gula_darah,
               bmi, riwayat_ortu, hasil_prediksi
        FROM pasien
        ORDER BY id DESC
    """)

    data = cursor.fetchall()
    conn.close()
    return data

def submit_data():
    nama = entry_nama.get().strip()
    riwayat = combo_riwayat.get()

    if not nama:
        messagebox.showerror(
            "Error Validasi",
            "Nama pasien tidak boleh kosong!"
        )
        return

    if not entry_usia.get().strip() or not entry_gula.get().strip() or not entry_bmi.get().strip():
        messagebox.showerror(
            "Error Validasi",
            "Semua data harus diisi!"
        )
        return

    try:
        usia = int(entry_usia.get())
        gula = float(entry_gula.get())
        bmi = float(entry_bmi.get())

    except ValueError:
        messagebox.showerror(
            "Error Validasi",
            "Usia, gula darah, dan BMI harus berupa angka valid!"
        )
        return

    if usia < 1 or usia > 120:
        messagebox.showerror(
            "Error Validasi",
            "Usia harus antara 1 sampai 120 tahun!"
        )
        return

    if gula <= 0:
        messagebox.showerror(
            "Error Validasi",
            "Gula darah harus lebih dari 0!"
        )
        return

    if bmi <= 0:
        messagebox.showerror(
            "Error Validasi",
            "BMI harus lebih dari 0!"
        )
        return

    if riwayat not in ("Ya", "Tidak"):
        messagebox.showerror(
            "Error Validasi",
            "Pilih riwayat diabetes orang tua!"
        )
        return

    hasil, warna = prediksi_diabetes(gula, bmi, riwayat)

    label_hasil.config(
        text=hasil,
        fg=warna
    )

    try:
        tambah_pasien(
            nama, usia, gula, bmi, riwayat, hasil
        )

        messagebox.showinfo(
            "Berhasil",
            "Data pasien berhasil disimpan!"
        )

    except sqlite3.Error as e:
        messagebox.showerror(
            "Database Error",
            f"Gagal menyimpan data: {e}"
        )

