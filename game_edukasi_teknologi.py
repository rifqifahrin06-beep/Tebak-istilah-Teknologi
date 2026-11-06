"""
Tebak Istilah Teknologi - Game Edukasi Kuis Pilihan Ganda
Fitur: sistem nyawa, skor, bonus beruntun (streak), skor tertinggi tersimpan.
Jalankan : python tebak_istilah_teknologi.py
Jadi .exe: pip install pyinstaller
           pyinstaller --onefile --windowed tebak_istilah_teknologi.py
"""

import json
import os
import random
import tkinter as tk
from tkinter import messagebox

NYAWA_AWAL = 3
POIN_BENAR = 10
BONUS_STREAK = 5          # bonus tiap jawaban benar beruntun (mulai streak ke-2)
FILE_SKOR = "skor_tertinggi.json"

# (pertanyaan/definisi, jawaban benar, [pengecoh], penjelasan)
SOAL = [
    ("Jaringan komputer global yang menghubungkan miliaran perangkat di seluruh dunia.",
     "Internet", ["Intranet", "Bluetooth", "Firewall"],
     "Internet adalah jaringan global yang saling terhubung memakai protokol TCP/IP."),
    ("Perangkat lunak yang mengatur perangkat keras dan menjalankan aplikasi pada komputer.",
     "Sistem Operasi", ["Kompiler", "Basis Data", "Browser"],
     "Contoh sistem operasi: Windows, Linux, macOS, Android."),
    ("Kumpulan langkah logis dan terurut untuk menyelesaikan suatu masalah.",
     "Algoritma", ["Variabel", "Konstanta", "Protokol"],
     "Algoritma dapat dituliskan sebagai pseudocode atau flowchart sebelum dikodekan."),
    ("Sistem keamanan jaringan yang memfilter lalu lintas data masuk dan keluar.",
     "Firewall", ["Router", "Modem", "Hub"],
     "Firewall bekerja berdasarkan aturan untuk mengizinkan atau memblokir koneksi."),
    ("Teknologi yang memungkinkan penyimpanan dan akses data/layanan lewat internet, bukan perangkat lokal.",
     "Cloud Computing", ["Overclocking", "Defragmentasi", "Multitasking"],
     "Contohnya Google Drive, AWS, dan Microsoft Azure."),
    ("Kecerdasan yang ditanamkan pada mesin agar mampu meniru cara berpikir manusia.",
     "Artificial Intelligence", ["Virtual Reality", "Blockchain", "Internet of Things"],
     "AI mencakup machine learning, pengenalan gambar, dan pemrosesan bahasa alami."),
    ("Perangkat lunak berbahaya yang dirancang untuk merusak atau mencuri data.",
     "Malware", ["Freeware", "Middleware", "Shareware"],
     "Malware meliputi virus, worm, trojan, dan ransomware."),
    ("Alamat unik yang diberikan kepada setiap perangkat dalam jaringan.",
     "IP Address", ["MAC Filter", "Domain Name", "Hostname Server"],
     "Contoh IPv4: 192.168.1.1. IPv6 dibuat karena alamat IPv4 hampir habis."),
    ("Bahasa markup untuk membuat struktur halaman web.",
     "HTML", ["Python", "SQL", "CSS"],
     "HTML = HyperText Markup Language. CSS dipakai untuk tampilan, bukan struktur."),
    ("Bahasa yang digunakan untuk mengelola dan mengakses data pada basis data relasional.",
     "SQL", ["HTML", "PHP", "JSON"],
     "SQL = Structured Query Language, dengan perintah seperti SELECT, INSERT, UPDATE."),
    ("Perangkat yang menghubungkan beberapa jaringan dan meneruskan paket data antar jaringan.",
     "Router", ["Keyboard", "Scanner", "Plotter"],
     "Router menentukan jalur terbaik bagi paket data untuk sampai ke tujuan."),
    ("Teknologi buku besar digital terdesentralisasi yang menjadi dasar mata uang kripto.",
     "Blockchain", ["Cloud Storage", "Big Data", "Cache"],
     "Data disimpan dalam blok-blok yang saling terhubung dan sulit diubah."),
    ("Jaringan benda fisik (sensor, perangkat rumah, dll.) yang saling terhubung dan bertukar data lewat internet.",
     "Internet of Things", ["Augmented Reality", "Cyber Security", "Machine Code"],
     "Contohnya lampu pintar, jam tangan pintar, dan sensor pertanian."),
    ("Memori sementara berkecepatan tinggi yang menyimpan data yang sering diakses agar proses lebih cepat.",
     "Cache", ["Hard Disk", "BIOS", "Flash Drive"],
     "Cache ada di prosesor, browser, hingga server web."),
    ("Teknik penipuan yang memancing korban memberikan data sensitif lewat pesan atau situs palsu.",
     "Phishing", ["Debugging", "Streaming", "Booting"],
     "Waspadai tautan mencurigakan dan jangan bagikan OTP atau kata sandi."),
    ("Proses menemukan dan memperbaiki kesalahan (error) pada program.",
     "Debugging", ["Compiling", "Deploying", "Formatting"],
     "Istilah 'bug' populer sejak sebuah ngengat ditemukan di komputer Harvard Mark II."),
    ("Teknologi yang menggabungkan objek digital ke dalam tampilan dunia nyata secara langsung.",
     "Augmented Reality", ["Virtual Reality", "Mixed Storage", "Digital Twin Cache"],
     "Contoh: filter kamera dan game Pokemon GO."),
    ("Kumpulan data berukuran sangat besar dan kompleks yang butuh teknologi khusus untuk diolah.",
     "Big Data", ["Data Entry", "Data Type", "Database Key"],
     "Ciri utamanya: volume, kecepatan (velocity), dan variasi (variety)."),
    ("Proses mengubah data menjadi kode rahasia agar tidak bisa dibaca pihak yang tidak berwenang.",
     "Enkripsi", ["Kompresi", "Defragmentasi", "Indeksasi"],
     "Hanya pemilik kunci yang bisa mendekripsi data kembali ke bentuk asli."),
    ("Penerjemah yang mengubah seluruh kode sumber menjadi kode mesin sebelum dijalankan.",
     "Kompiler", ["Interpreter Baris", "Editor Teks", "Emulator"],
     "Contoh bahasa terkompilasi: C dan C++. Python umumnya diinterpretasi."),
]


def muat_skor_tertinggi():
    try:
        with open(FILE_SKOR, "r", encoding="utf-8") as f:
            return int(json.load(f).get("skor_tertinggi", 0))
    except (OSError, ValueError, json.JSONDecodeError):
        return 0


def simpan_skor_tertinggi(skor):
    try:
        with open(FILE_SKOR, "w", encoding="utf-8") as f:
            json.dump({"skor_tertinggi": skor}, f)
    except OSError:
        pass


class GameKuis(tk.Tk):
    WARNA_BG = "#0f172a"
    WARNA_KARTU = "#1e293b"
    WARNA_TEKS = "#e2e8f0"
    WARNA_AKSEN = "#38bdf8"
    WARNA_BENAR = "#22c55e"
    WARNA_SALAH = "#ef4444"

    def __init__(self):
        super().__init__()
        self.title("Tebak Istilah Teknologi")
        self.geometry("720x600")
        self.minsize(640, 560)
        self.configure(bg=self.WARNA_BG)

        self.skor_tertinggi = muat_skor_tertinggi()
        self.tombol_opsi = []
        self.sudah_menjawab = False
        self._buat_tampilan()
        self.mulai_game()

    # ---------- Tampilan ----------
    def _buat_tampilan(self):
        atas = tk.Frame(self, bg=self.WARNA_BG)
        atas.pack(fill="x", padx=24, pady=(18, 6))

        self.lbl_nyawa = tk.Label(atas, font=("Segoe UI", 18), bg=self.WARNA_BG, fg=self.WARNA_SALAH)
        self.lbl_nyawa.pack(side="left")

        kanan = tk.Frame(atas, bg=self.WARNA_BG)
        kanan.pack(side="right")
        self.lbl_skor = tk.Label(kanan, font=("Segoe UI", 14, "bold"), bg=self.WARNA_BG, fg=self.WARNA_AKSEN)
        self.lbl_skor.pack(anchor="e")
        self.lbl_rekor = tk.Label(kanan, font=("Segoe UI", 10), bg=self.WARNA_BG, fg="#94a3b8")
        self.lbl_rekor.pack(anchor="e")

        self.lbl_progres = tk.Label(self, font=("Segoe UI", 10), bg=self.WARNA_BG, fg="#94a3b8")
        self.lbl_progres.pack(anchor="w", padx=24)

        kartu = tk.Frame(self, bg=self.WARNA_KARTU)
        kartu.pack(fill="x", padx=24, pady=10)
        tk.Label(kartu, text="Istilah apakah ini?", font=("Segoe UI", 11, "bold"),
                 bg=self.WARNA_KARTU, fg=self.WARNA_AKSEN).pack(anchor="w", padx=16, pady=(14, 2))
        self.lbl_soal = tk.Label(kartu, font=("Segoe UI", 14), bg=self.WARNA_KARTU, fg=self.WARNA_TEKS,
                                 wraplength=620, justify="left")
        self.lbl_soal.pack(anchor="w", padx=16, pady=(0, 16))

        bingkai_opsi = tk.Frame(self, bg=self.WARNA_BG)
        bingkai_opsi.pack(fill="x", padx=24)
        for i in range(4):
            tombol = tk.Button(bingkai_opsi, font=("Segoe UI", 13), bg=self.WARNA_KARTU,
                               fg=self.WARNA_TEKS, activebackground="#334155",
                               activeforeground=self.WARNA_TEKS, relief="flat", anchor="w",
                               padx=16, pady=8, cursor="hand2",
                               command=lambda idx=i: self.cek_jawaban(idx))
            tombol.pack(fill="x", pady=4)
            self.tombol_opsi.append(tombol)

        self.lbl_umpan = tk.Label(self, font=("Segoe UI", 11), bg=self.WARNA_BG, fg=self.WARNA_TEKS,
                                  wraplength=650, justify="left")
        self.lbl_umpan.pack(anchor="w", padx=24, pady=(10, 4))

        self.btn_lanjut = tk.Button(self, text="Lanjut ➜", font=("Segoe UI", 12, "bold"),
                                    bg=self.WARNA_AKSEN, fg="#0f172a", relief="flat",
                                    padx=18, pady=6, cursor="hand2", command=self.soal_berikutnya)

    # ---------- Alur game ----------
    def mulai_game(self):
        self.nyawa = NYAWA_AWAL
        self.skor = 0
        self.streak = 0
        self.antrean = random.sample(SOAL, len(SOAL))
        self.nomor = 0
        self.tampilkan_soal()

    def perbarui_status(self):
        self.lbl_nyawa.config(text="❤" * self.nyawa + "🖤" * (NYAWA_AWAL - self.nyawa))
        self.lbl_skor.config(text=f"Skor: {self.skor}")
        self.lbl_rekor.config(text=f"Skor tertinggi: {self.skor_tertinggi}")
        self.lbl_progres.config(text=f"Soal {self.nomor + 1} dari {len(self.antrean)}"
                                     + (f"   •   🔥 Beruntun x{self.streak}" if self.streak >= 2 else ""))

    def tampilkan_soal(self):
        self.sudah_menjawab = False
        definisi, benar, pengecoh, penjelasan = self.antrean[self.nomor]
        pilihan = [benar] + pengecoh
        random.shuffle(pilihan)
        self.jawaban_benar = benar
        self.penjelasan = penjelasan
        self.pilihan_saat_ini = pilihan

        self.lbl_soal.config(text=definisi)
        for tombol, teks in zip(self.tombol_opsi, pilihan):
            label = f"{'ABCD'[self.tombol_opsi.index(tombol)]}.  {teks}"
            tombol.config(text=label, bg=self.WARNA_KARTU, state="normal")
        self.lbl_umpan.config(text="")
        self.btn_lanjut.pack_forget()
        self.perbarui_status()

    def cek_jawaban(self, idx):
        if self.sudah_menjawab:
            return
        self.sudah_menjawab = True
        dipilih = self.pilihan_saat_ini[idx]

        for tombol, teks in zip(self.tombol_opsi, self.pilihan_saat_ini):
            tombol.config(state="disabled")
            if teks == self.jawaban_benar:
                tombol.config(bg=self.WARNA_BENAR, disabledforeground="white")

        if dipilih == self.jawaban_benar:
            self.streak += 1
            tambahan = POIN_BENAR + (BONUS_STREAK * (self.streak - 1) if self.streak >= 2 else 0)
            self.skor += tambahan
            self.lbl_umpan.config(fg=self.WARNA_BENAR,
                                  text=f"✅ Benar! +{tambahan} poin\n{self.penjelasan}")
        else:
            self.streak = 0
            self.nyawa -= 1
            self.tombol_opsi[idx].config(bg=self.WARNA_SALAH, disabledforeground="white")
            self.lbl_umpan.config(fg=self.WARNA_SALAH,
                                  text=f"❌ Salah! Jawaban benar: {self.jawaban_benar}\n{self.penjelasan}")

        self.perbarui_status()
        if self.nyawa == 0:
            self.btn_lanjut.config(text="Lihat Hasil ➜")
        elif self.nomor + 1 >= len(self.antrean):
            self.btn_lanjut.config(text="Lihat Hasil ➜")
        else:
            self.btn_lanjut.config(text="Lanjut ➜")
        self.btn_lanjut.pack(anchor="e", padx=24, pady=8)

    def soal_berikutnya(self):
        if self.nyawa == 0 or self.nomor + 1 >= len(self.antrean):
            self.akhir_game()
        else:
            self.nomor += 1
            self.tampilkan_soal()

    def akhir_game(self):
        menang = self.nyawa > 0
        rekor_baru = self.skor > self.skor_tertinggi
        if rekor_baru:
            self.skor_tertinggi = self.skor
            simpan_skor_tertinggi(self.skor)

        judul = "🎉 Selamat, kamu menamatkan semua soal!" if menang else "💀 Game Over - nyawa habis!"
        pesan = f"{judul}\n\nSkor akhir: {self.skor}"
        if rekor_baru:
            pesan += "\n🏆 Skor tertinggi baru!"
        pesan += "\n\nMain lagi?"

        if messagebox.askyesno("Hasil", pesan):
            self.mulai_game()
        else:
            self.destroy()


if __name__ == "__main__":
    GameKuis().mainloop()