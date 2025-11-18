from prettytable import PrettyTable
import data as d 
import handler as h
import os
import inquirer
from colorama import Fore, Back, Style, init
import pyfiglet

init(autoreset=True)

tabel1 = PrettyTable()
tabel2 = PrettyTable()
tabel3 = PrettyTable()

def clear():
    os.system("cls || clear")

def tampilkan_banner():
    banner = pyfiglet.figlet_format("APOTEK NAYLA", font="slant")
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.GREEN + "=" * 60)
    print(Fore.YELLOW + "        🏥 Sistem Manajemen Apotek Sehat 🏥")
    print(Fore.GREEN + "=" * 60 + Style.RESET_ALL)

def header_box(text, warna=Fore.CYAN):
    panjang = len(text) + 4
    print()
    print(warna + "╔" + "═" * panjang + "╗")
    print(warna + "║  " + Style.BRIGHT + text + Style.NORMAL + "  ║")
    print(warna + "╚" + "═" * panjang + "╝" + Style.RESET_ALL)
    print()

def pesan_sukses(text):
    print(Fore.GREEN + "✅ " + text + Style.RESET_ALL)

def pesan_error(text):
    print(Fore.RED + "❌ " + text + Style.RESET_ALL)

def pesan_info(text):
    print(Fore.YELLOW + "ℹ️  " + text + Style.RESET_ALL)

while d.run:
    if d.pengguna is None:
        clear()
        tampilkan_banner()
        
        menu_utama = [
            inquirer.List(
                "pilihan",
                message=Fore.CYAN + Style.BRIGHT + "🏠 MENU UTAMA" + Style.RESET_ALL,
                choices=["Login", "Registrasi", "Keluar"]
            )
        ]
        jawaban = inquirer.prompt(menu_utama)
        pilihan = jawaban["pilihan"]
        clear()

        if pilihan == "Login":
            header_box("LOGIN PENGGUNA", Fore.BLUE)
            username = input(Fore.CYAN + "👤 Username: " + Style.RESET_ALL).strip()
            password = input(Fore.CYAN + "🔒 Password: " + Style.RESET_ALL).strip()

            if username in d.user_data:
                if d.user_data[username]["password"] == password:
                    d.pengguna = username
                    d.role_pengguna = d.user_data[username]["role"]
                    pesan_sukses(f"Login berhasil! Selamat datang, {username} ({d.role_pengguna}).")
                    input(Fore.YELLOW + "\nTekan Enter untuk melanjutkan..." + Style.RESET_ALL)
                    continue
                else:
                    pesan_error("Password salah.")
            else:
                pesan_error("Username tidak ditemukan.")
            
            input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

        elif pilihan == "Registrasi":
            header_box("REGISTRASI PENGGUNA BARU", Fore.GREEN)
            new_username = input(Fore.CYAN + "👤 Username Baru: " + Style.RESET_ALL).strip()
            new_password = input(Fore.CYAN + "🔒 Password: " + Style.RESET_ALL).strip()

            if not new_username or not new_password:
                pesan_error("Username dan Password tidak boleh kosong.")
            elif new_username in d.user_data:
                pesan_error("Username sudah terdaftar.")
            else:
                if len(new_password) < 4:
                    pesan_error("Password minimal 4 karakter.")
                else:
                    d.user_data[new_username] = {"password": new_password, "role": "user", "member": False}
                    pesan_sukses(f"Registrasi {new_username} berhasil. Silakan Login.")
            
            input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

        elif pilihan == "Keluar":
            clear()
            print(Fore.CYAN + Style.BRIGHT)
            print("╔════════════════════════════════════════╗")
            print("║   Terima kasih telah menggunakan      ║")
            print("║      🏥 TOKO OBAT SEHAT 🏥           ║")
            print("║         Semoga sehat selalu!          ║")
            print("╚════════════════════════════════════════╝")
            print(Style.RESET_ALL)
            d.run = False

    elif d.pengguna is not None:
        if d.role_pengguna == "apoteker":
            clear()
            header_box(f"👨‍⚕️  ADMIN: {d.pengguna.upper()}", Fore.MAGENTA)
            
            menu_admin = [
                inquirer.List(
                    "opsi",
                    message=Fore.MAGENTA + Style.BRIGHT + "🔧 MENU ADMIN" + Style.RESET_ALL,
                    choices=[
                        "📋 Lihat Daftar Obat",
                        "➕ Tambah Obat Baru",
                        "✏️  Perbarui Stok/Harga Obat",
                        "🗑️  Hapus Obat",
                        "🔍 Filter & Cari Obat",
                        "🚪 Logout"
                    ]
                )
            ]
            jawaban = inquirer.prompt(menu_admin)
            opsi = jawaban["opsi"]

            if opsi == "📋 Lihat Daftar Obat":
                clear()
                header_box("DAFTAR OBAT", Fore.CYAN)
                h.prosedur_tampilkan_obat_admin()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                
            elif opsi == "➕ Tambah Obat Baru":
                clear()
                header_box("TAMBAH OBAT BARU", Fore.GREEN)
                h.prosedur_tambah_obat_baru()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                
            elif opsi == "✏️  Perbarui Stok/Harga Obat":
                clear()
                header_box("PERBARUI OBAT", Fore.YELLOW)
                h.prosedur_perbarui_obat()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                
            elif opsi == "🗑️  Hapus Obat":
                clear()
                header_box("HAPUS OBAT", Fore.RED)
                h.prosedur_hapus_obat()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                
            elif opsi == "🔍 Filter & Cari Obat":
                clear()
                header_box("FILTER & CARI OBAT", Fore.BLUE)
                h.filter_obat_admin()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                
            elif opsi == "🚪 Logout":
                pesan_sukses(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

        elif d.role_pengguna == "user":
            clear()
            header_box(f"👤 USER: {d.pengguna.upper()}", Fore.CYAN)
            
            if d.user_data[d.pengguna]["member"]:
                print(Fore.YELLOW + "⭐ Status: MEMBER (Diskon 10%)" + Style.RESET_ALL)
            else:
                print(Fore.WHITE + "💡 Status: Non-Member" + Style.RESET_ALL)
            print()
            
            menu_user = [
                inquirer.List(
                    "opsi",
                    message=Fore.CYAN + Style.BRIGHT + "🛒 MENU PENGGUNA" + Style.RESET_ALL,
                    choices=[
                        "📋 Lihat Daftar Obat", 
                        "🛍️  Beli Obat", 
                        "🔍 Filter & Cari Obat", 
                        "⭐ Daftar Member", 
                        "🚪 Logout"
                    ]
                )
            ]
            jawaban = inquirer.prompt(menu_user)
            opsi = jawaban["opsi"]

            if opsi == "📋 Lihat Daftar Obat":
                clear()
                header_box("DAFTAR OBAT", Fore.CYAN)
                h.tampilkan_daftar_obat_user()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

            elif opsi == "🔍 Filter & Cari Obat":
                clear()
                header_box("FILTER & CARI OBAT", Fore.BLUE)
                h.filter_obat_user()
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

            elif opsi == "⭐ Daftar Member":
                clear()
                header_box("PENDAFTARAN MEMBER", Fore.YELLOW)
                if d.user_data[d.pengguna]["member"]:
                    pesan_info("Kamu sudah menjadi member!")
                else:
                    print(Fore.CYAN + "💰 Keuntungan Member:")
                    print(Fore.GREEN + "   ✓ Diskon 10% setiap pembelian")
                    print(Fore.GREEN + "   ✓ Gratis bergabung\n")
                    konfirmasi = input(Fore.YELLOW + "Daftar jadi member? (y/n): " + Style.RESET_ALL).strip().lower()
                    if konfirmasi == "y":
                        d.user_data[d.pengguna]["member"] = True
                        pesan_sukses("Selamat! Kamu sekarang member (diskon 10%).")
                    else:
                        pesan_info("Pendaftaran member dibatalkan.")
                
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

            elif opsi == "🛍️  Beli Obat":
                clear()
                header_box("PEMBELIAN OBAT", Fore.GREEN)
                
                if h.cek_obat_kosong():
                    pesan_error("Tidak ada obat yang tersedia untuk dibeli.")
                    input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
                    continue

                h.tampilkan_daftar_obat_user()
                print(Fore.CYAN + "\n" + "─" * 60)
                print(Fore.CYAN + Style.BRIGHT + "  💊 PROSES PEMBELIAN OBAT" + Style.RESET_ALL)
                print(Fore.CYAN + "─" * 60 + "\n")

                kodeObat = None
                while True:
                    inputKode = input(Fore.YELLOW + "📝 Masukkan kode obat: " + Style.RESET_ALL).strip()
                    try:
                        kodeObat = int(inputKode)
                        if kodeObat in d.obat_data:
                            break
                        else:
                            pesan_error("Kode obat tidak ditemukan.")
                    except ValueError:
                        pesan_error("Kode obat harus berupa angka.")

                jumlahBeli = None
                while True:
                    inputJumlah = input(Fore.YELLOW + f"📦 Jumlah beli {d.obat_data.get(kodeObat, {}).get('nama', 'Obat')}: " + Style.RESET_ALL).strip()
                    try:
                        jumlahBeli = int(inputJumlah)
                        break
                    except ValueError:
                        pesan_error("Jumlah beli harus berupa angka.")

                h.proses_pembelian(kodeObat, jumlahBeli)
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

            elif opsi == "🚪 Logout":
                pesan_sukses(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)