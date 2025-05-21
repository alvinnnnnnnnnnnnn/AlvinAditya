import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import os

# === Konstanta ===
FILE_EXCEL = "data_dummy.xlsx"
FITUR = ["Kecepatan", "Jarak", "GesekanBan", "KecepatanAngin"]
KODE_KOLOM_ASLI = {
    "Kecepatan (km/s)": "Kecepatan",
    "Jarak (m)": "Jarak",
    "Koef Gesekan Ban": "GesekanBan",
    "Kecepatan Angin (m/s)": "KecepatanAngin"
}

# === Fungsi Load & Training Model ===
def load_model():
    if not os.path.exists(FILE_EXCEL):
        messagebox.showerror("Error", f"File {FILE_EXCEL} tidak ditemukan!")
        exit()

    df = pd.read_excel(FILE_EXCEL)
    df = df.rename(columns=KODE_KOLOM_ASLI)

    missing = [col for col in FITUR + ["Label"] if col not in df.columns]
    if missing:
        messagebox.showerror("Error", f"Kolom berikut tidak ditemukan di Excel:\n{missing}")
        exit()

    X = df[FITUR]
    y = df["Label"]

    model = DecisionTreeClassifier()
    model.fit(X, y)
    return model

clf = load_model()

# === Fungsi Utama ===
def klasifikasi():
    try:
        kecepatan = float(entry_kecepatan.get())
        jarak = float(entry_jarak.get())
        gesekan = float(entry_gesekan.get())
        angin = float(entry_angin.get())

        hasil = clf.predict([[kecepatan, jarak, gesekan, angin]])[0]
        label_hasil.config(text=f"Hasil Klasifikasi: {hasil}")

        baris_baru = pd.DataFrame([{
            "Kecepatan (km/s)": kecepatan,
            "Jarak (m)": jarak,
            "Koef Gesekan Ban": gesekan,
            "Kecepatan Angin (m/s)": angin,
            "Label": hasil
        }])

        if os.path.exists(FILE_EXCEL):
            data_lama = pd.read_excel(FILE_EXCEL)
            data_baru = pd.concat([data_lama, baris_baru], ignore_index=True)
        else:
            data_baru = baris_baru

        data_baru.to_excel(FILE_EXCEL, index=False)
        messagebox.showinfo("Sukses", "Data berhasil disimpan!")
    except ValueError:
        messagebox.showerror("Input Error", "Masukkan angka yang valid!")

def reset_input():
    entry_kecepatan.delete(0, tk.END)
    entry_jarak.delete(0, tk.END)
    entry_gesekan.delete(0, tk.END)
    entry_angin.delete(0, tk.END)
    label_hasil.config(text="Hasil Klasifikasi:")

def tampilkan_tree():
    plt.figure(figsize=(10, 7))
    plot_tree(clf, feature_names=FITUR,
              class_names=clf.classes_, filled=True, rounded=True)
    plt.title("Pohon Keputusan - Deteksi Tabrakan")
    plt.show()

def tampilkan_data():
    data_window = tk.Toplevel(root)
    data_window.title("Data Klasifikasi")
    data_window.geometry("900x500")

    label_judul = tk.Label(data_window, text="Data Klasifikasi", font=("Helvetica", 14, "bold"))
    label_judul.pack(pady=10)

    global tabel
    kolom = ["Kecepatan (km/s)", "Jarak (m)", "Koef Gesekan Ban", "Kecepatan Angin (m/s)", "Label"]
    tabel = ttk.Treeview(data_window, columns=kolom, show="headings")
    for col in kolom:
        tabel.heading(col, text=col)
        tabel.column(col, anchor="center", width=140)
    tabel.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(data_window, orient="vertical", command=tabel.yview)
    tabel.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    refresh_data()

def refresh_data():
    for item in tabel.get_children():
        tabel.delete(item)

    if os.path.exists(FILE_EXCEL):
        try:
            data = pd.read_excel(FILE_EXCEL)
            # Rename kolom agar konsisten tampilannya
            data = data.rename(columns={
                "Kecepatan (m/s)": "Kecepatan (km/s)",
                "Jarak (cm)": "Jarak (m)"
            })
            data = data[["Kecepatan (km/s)", "Jarak (m)", "Koef Gesekan Ban", "Kecepatan Angin (m/s)", "Label"]]
            for _, row in data.iterrows():
                tabel.insert("", "end", values=list(row))
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memuat data: {e}")
    else:
        messagebox.showinfo("Info", "Belum ada data disimpan")

# === GUI ===
root = tk.Tk()
root.title("Sistem Deteksi Tabrakan Kendaraan")
root.geometry("500x430")
root.configure(bg="lightblue")  # Background root

frame_main = tk.Frame(root, bg="lightblue")
frame_main.pack(padx=20, pady=20)

judul = tk.Label(frame_main, text="Input Data Jarak Kendaraan", font=("ROG FONTS", 17, "bold"), bg="lightblue", fg="black")
judul.pack(pady=10)

frame_input = tk.Frame(frame_main, bg="lightblue")
frame_input.pack()

tk.Label(frame_input, text="Kecepatan (km):", bg="lightblue").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_kecepatan = tk.Entry(frame_input)
entry_kecepatan.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Jarak (m):", bg="lightblue").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_jarak = tk.Entry(frame_input)
entry_jarak.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Gesekan Ban:", bg="lightblue").grid(row=2, column=0, padx=5, pady=5, sticky="e")
entry_gesekan = tk.Entry(frame_input)
entry_gesekan.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Kecepatan Angin (m/s):", bg="lightblue").grid(row=3, column=0, padx=5, pady=5, sticky="e")
entry_angin = tk.Entry(frame_input)
entry_angin.grid(row=3, column=1, padx=5, pady=5)

label_hasil = tk.Label(frame_main, text="Hasil Klasifikasi:", font=("Algerian", 12), bg="lightblue", fg="black")
label_hasil.pack(pady=10)

frame_tombol = tk.Frame(frame_main, bg="lightblue")
frame_tombol.pack(pady=10)

btn_simpan = tk.Button(frame_tombol, text="Gas", command=klasifikasi, bg="green", fg="yellow", width=15)
btn_simpan.grid(row=0, column=0, padx=5)

btn_reset = tk.Button(frame_tombol, text="Reset", command=reset_input, bg="red", fg="yellow", width=15)
btn_reset.grid(row=0, column=1, padx=5)

btn_lihat_data = tk.Button(frame_main, text="Lihat Data Klasifikasi", command=tampilkan_data, bg="blue", fg="yellow", width=25)
btn_lihat_data.pack(pady=5)

btn_tree = tk.Button(frame_main, text="Lihat Pohon Keputusan", command=tampilkan_tree, bg="Yellow", fg="black")
btn_tree.pack(pady=5)

root.mainloop()

