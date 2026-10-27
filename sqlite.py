import sqlite3
import tkinter as tk
from tkinter import messagebox


# --- 1. FUNGSI DATABASE ---
def create_db():
  conn = sqlite3.connect("nilai_siswa.db")
  cursor = conn.cursor()
  cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nama_siswa TEXT NOT NULL,
            biologi INTEGER NOT NULL,
            fisika INTEGER NOT NULL,
            inggris INTEGER NOT NULL,
            prediksi_fakultas TEXT NOT NULL
        )
    """)
  conn.commit()
  conn.close()


create_db()


# --- 2. FUNGSI PREDIKSI FAKULTAS ---
def prediksi_fakultas(biologi, fisika, inggris):
  if biologi > fisika and biologi > inggris:
    return "Kedokteran"
  elif fisika > biologi and fisika > inggris:
    return "Teknik"
  elif inggris > biologi and inggris > fisika:
    return "Bahasa"
  else:
    return "Tidak dapat ditentukan"


# --- 3. FUNGSI SUBMIT DATA ---
def submit_nilai():
  nama = entry_nama.get().strip()
  try:
    bio = int(entry_bio.get())
    fis = int(entry_fis.get())
    ing = int(entry_ing.get())
  except ValueError:
    messagebox.showerror("Error", "Nilai harus berupa angka!")
    return

  if not nama:
    messagebox.showerror("Error", "Nama siswa tidak boleh kosong!")
    return

  hasil_prediksi = prediksi_fakultas(bio, fis, ing)

  conn = sqlite3.connect("nilai_siswa.db")
  cursor = conn.cursor()
  cursor.execute(
      """
        INSERT INTO nilai_siswa(nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """,
      (nama, bio, fis, ing, hasil_prediksi),
  )
  conn.commit()
  conn.close()

  messagebox.showinfo("Hasil Prediksi", f"Prediksi Fakultas: {hasil_prediksi}")

  # Reset input
  entry_nama.delete(0, tk.END)
  entry_bio.delete(0, tk.END)
  entry_fis.delete(0, tk.END)
  entry_ing.delete(0, tk.END)


# --- 4. FUNGSI HOVER TOMBOL ---
def on_enter(e):
  btn_submit["bg"] = "#50fa7b"
  btn_submit["fg"] = "black"


def on_leave(e):
  btn_submit["bg"] = "#44475a"
  btn_submit["fg"] = "white"


# --- 5. TAMPILAN GUI (TKINTER) ---
root = tk.Tk()
root.title("Aplikasi Prediksi Fakultas Siswa")
root.geometry("400x420")
root.config(bg="#282a36")
root.resizable(False, False)

# Judul Utama
label_title = tk.Label(
    root,
    text="Prediksi Fakultas Siswa",
    font=("Arial", 16, "bold"),
    bg="#282a36",
    fg="#f8f8f2",
)
label_title.pack(pady=20)

# Frame Kontainer Form Input
frame_form = tk.Frame(root, bg="#282a36")
frame_form.pack(pady=10)

# Input Nama Siswa
tk.Label(
    frame_form,
    text="Nama Siswa:",
    font=("Arial", 11),
    bg="#282a36",
    fg="#f8f8f2",
).grid(row=0, column=0, sticky="w", pady=8)
entry_nama = tk.Entry(frame_form, font=("Arial", 11), width=22)
entry_nama.grid(row=0, column=1, pady=8, padx=10)

# Input Nilai Biologi
tk.Label(
    frame_form,
    text="Nilai Biologi:",
    font=("Arial", 11),
    bg="#282a36",
    fg="#f8f8f2",
).grid(row=1, column=0, sticky="w", pady=8)
entry_bio = tk.Entry(frame_form, font=("Arial", 11), width=22)
entry_bio.grid(row=1, column=1, pady=8, padx=10)

# Input Nilai Fisika
tk.Label(
    frame_form,
    text="Nilai Fisika:",
    font=("Arial", 11),
    bg="#282a36",
    fg="#f8f8f2",
).grid(row=2, column=0, sticky="w", pady=8)
entry_fis = tk.Entry(frame_form, font=("Arial", 11), width=22)
entry_fis.grid(row=2, column=1, pady=8, padx=10)

# Input Nilai Bahasa Inggris
tk.Label(
    frame_form,
    text="Nilai Bahasa Inggris:",
    font=("Arial", 11),
    bg="#282a36",
    fg="#f8f8f2",
).grid(row=3, column=0, sticky="w", pady=8)
entry_ing = tk.Entry(frame_form, font=("Arial", 11), width=22)
entry_ing.grid(row=3, column=1, pady=8, padx=10)

# Tombol Submit & Prediksi
btn_submit = tk.Button(
    root,
    text="Submit & Prediksi",
    font=("Arial", 11, "bold"),
    bg="#44475a",
    fg="white",
    relief="flat",
    width=22,
    command=submit_nilai,
)
btn_submit.pack(pady=15)

# Event Binding Hover Efek
btn_submit.bind("<Enter>", on_enter)
btn_submit.bind("<Leave>", on_leave)

# Event Loop Aplikasi
root.mainloop()