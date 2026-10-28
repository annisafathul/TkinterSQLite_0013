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

def lihat_data():
    jendela = tk.Toplevel(root)
    jendela.title("Riwayat Data Pasien")
    jendela.geometry("1100x400")

    kolom = (
        "id", "nama_pasien", "usia", "gula_darah",
        "bmi", "riwayat_ortu", "hasil_prediksi"
    )

    tabel = ttk.Treeview(
        jendela,
        columns=kolom,
        show="headings"
    )

    judul = [
        "ID", "Nama Pasien", "Usia",
        "Gula Darah", "BMI", "Riwayat Ortu",
        "Hasil Prediksi"
    ]

    lebar = [50, 140, 70, 100, 80, 110, 500]

    for col, text, width in zip(kolom, judul, lebar):
        tabel.heading(col, text=text)
        tabel.column(col, width=width, anchor="center")

    scrollbar = ttk.Scrollbar(
        jendela, orient="vertical",
        command=tabel.yview
    )
    tabel.configure(yscrollcommand=scrollbar.set)

    tabel.pack(
        side="left", fill="both",
        expand=True, padx=(10, 0), pady=10
    )
    scrollbar.pack(
        side="right", fill="y",
        padx=(0, 10), pady=10
    )

    data = get_pasien()

    for pasien in data:
        tabel.insert("", tk.END, values=pasien)

    if not data:
        messagebox.showinfo(
            "Informasi",
            "Belum ada data pasien yang tersimpan."
        )

init_db()

root = tk.Tk()
root.title("Aplikasi Prediksi Risiko Diabetes")
root.geometry("600x530")
root.resizable(False, False)


tk.Label(
    root,
    text="Aplikasi Prediksi Risiko Diabetes",
    font=("Arial", 16, "bold")
).pack(pady=15)



frame = tk.Frame(root)
frame.pack(pady=5)


tk.Label(
    frame, text="Nama Pasien"
).grid(row=0, column=0, sticky="w", padx=10, pady=7)

entry_nama = tk.Entry(frame, width=35)
entry_nama.grid(row=0, column=1, pady=7)


tk.Label(
    frame, text="Usia (tahun)"
).grid(row=1, column=0, sticky="w", padx=10, pady=7)

entry_usia = tk.Entry(frame, width=35)
entry_usia.grid(row=1, column=1, pady=7)


tk.Label(
    frame, text="Gula Darah (mg/dL)"
).grid(row=2, column=0, sticky="w", padx=10, pady=7)

entry_gula = tk.Entry(frame, width=35)
entry_gula.grid(row=2, column=1, pady=7)


tk.Label(
    frame, text="BMI"
).grid(row=3, column=0, sticky="w", padx=10, pady=7)

entry_bmi = tk.Entry(frame, width=35)
entry_bmi.grid(row=3, column=1, pady=7)

# Pilihan riwayat diabetes orang tua
tk.Label(
    frame, text="Riwayat Diabetes Ortu"
).grid(row=4, column=0, sticky="w", padx=10, pady=7)

combo_riwayat = ttk.Combobox(
    frame,
    values=["Ya", "Tidak"],
    state="readonly",
    width=32
)
combo_riwayat.grid(row=4, column=1, pady=7)
combo_riwayat.set("Tidak")


tk.Button(
    root,
    text="Prediksi dan Simpan Data",
    command=submit_data,
    width=25,
    bg="#3498db",
    fg="white"
).pack(pady=12)



label_hasil = tk.Label(
    root,
    text="Hasil Prediksi: -",
    font=("Arial", 11, "bold"),
    wraplength=550
)
label_hasil.pack(pady=10)

tk.Button(
    root,
    text="Lihat Data",
    command=lihat_data,
    width=20,
    bg="#3498db",
    fg="white"
).pack(pady=8)

root.mainloop()