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


def validasi_input_alphanumeric(prompt, min_length=1, max_length=None):
    while True:
        input_str = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            print(Fore.RED + "❌ Input tidak boleh kosong." + Style.RESET_ALL)
            continue
        
        if len(input_str) < min_length:
            print(Fore.RED + f"❌ Input minimal {min_length} karakter." + Style.RESET_ALL)
            continue
        
        if max_length and len(input_str) > max_length:
            print(Fore.RED + f"❌ Input maksimal {max_length} karakter." + Style.RESET_ALL)
            continue
        
        if not input_str.isalnum():
            print(Fore.RED + "❌ Input hanya boleh berupa huruf dan angka, tidak boleh ada spasi atau simbol." + Style.RESET_ALL)
            continue
        
        return input_str


def validasi_input_password(prompt, min_length=4):
    while True:
        input_str = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            print(Fore.RED + "❌ Password tidak boleh kosong." + Style.RESET_ALL)
            continue
        
        if len(input_str) < min_length:
            print(Fore.RED + f"❌ Password minimal {min_length} karakter." + Style.RESET_ALL)
            continue
        
        return input_str


def validasi_input_angka_positif(prompt, allow_zero=False):
    while True:
        input_str = input(Fore.YELLOW + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            print(Fore.RED + "❌ Input tidak boleh kosong." + Style.RESET_ALL)
            continue
        
        if not input_str.isdigit() and not (input_str[0] == '-' and input_str[1:].isdigit()):
            print(Fore.RED + "❌ Input harus berupa angka saja, tidak boleh ada huruf atau simbol." + Style.RESET_ALL)
            continue
        
        try:
            nilai = int(input_str)
            
            if nilai < 0:
                print(Fore.RED + "❌ Input tidak boleh berupa angka negatif." + Style.RESET_ALL)
                continue
            
            if nilai == 0 and not allow_zero:
                print(Fore.RED + "❌ Input tidak boleh nol (0)." + Style.RESET_ALL)
                continue
            
            return nilai
            
        except ValueError:
            print(Fore.RED + "❌ Input harus berupa angka yang valid." + Style.RESET_ALL)


def validasi_konfirmasi_yn(prompt):
    while True:
        input_str = input(Fore.YELLOW + prompt + Style.RESET_ALL).strip().lower()
        
        if not input_str:
            print(Fore.RED + "❌ Input tidak boleh kosong. Ketik 'y' untuk Ya atau 'n' untuk Tidak." + Style.RESET_ALL)
            continue
        
        if len(input_str) > 1:
            print(Fore.RED + "❌ Input harus 'y' atau 'n' saja." + Style.RESET_ALL)
            continue
        
        if not input_str.isalpha():
            print(Fore.RED + "❌ Input harus berupa huruf 'y' atau 'n', tidak boleh angka atau simbol." + Style.RESET_ALL)
            continue
        
        if input_str == 'y':
            return True
        elif input_str == 'n':
            return False
        else:
            print(Fore.RED + "❌ Input tidak valid. Ketik 'y' untuk Ya atau 'n' untuk Tidak." + Style.RESET_ALL)


def clear():
    os.system("cls || clear")

def tampilkan_banner():
    banner = pyfiglet.figlet_format("APOTEK NAYLA", font="slant")
    print(Fore.CYAN + Style.BRIGHT + banner)
    print(Fore.GREEN + "=" * 60)
    print(Fore.YELLOW + "        🏥 Sistem Manajemen Apotek Sehat 🏥")
    print(Fore.GREEN + "=" * 60 + Style.RESET_ALL)

def header_box(text, warna=Fore.CYAN):
    # Hitung panjang teks tanpa karakter emoji/unicode
    import unicodedata
    
    # Fungsi untuk menghitung lebar visual teks
    def hitung_lebar_visual(s):
        lebar = 0
        for char in s:
            # Karakter emoji dan wide characters dihitung sebagai 2
            if unicodedata.east_asian_width(char) in ('F', 'W'):
                lebar += 2
            # Karakter biasa dihitung sebagai 1
            else:
                lebar += 1
        return lebar
    
    lebar_visual = hitung_lebar_visual(text)
    panjang_box = lebar_visual + 4
    
    print()
    print(warna + "╔" + "═" * panjang_box + "╗")
    
    # Hitung padding untuk centering
    sisa_ruang = panjang_box - lebar_visual
    padding_kiri = sisa_ruang // 2
    padding_kanan = sisa_ruang - padding_kiri
    
    print(warna + "║" + " " * padding_kiri + Style.BRIGHT + text + Style.NORMAL + " " * padding_kanan + "║")
    print(warna + "╚" + "═" * panjang_box + "╝" + Style.RESET_ALL)
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
                message=Fore.CYAN + Style.BRIGHT + "MENU UTAMA" + Style.RESET_ALL,
                choices=["Login", "Registrasi", "Keluar"]
            )
        ]
        jawaban = inquirer.prompt(menu_utama)
        pilihan = jawaban["pilihan"]
        clear()

        if pilihan == "Login":
            header_box("LOGIN PENGGUNA", Fore.BLUE)
            
            username = validasi_input_alphanumeric("Username: ", min_length=1)
            password = validasi_input_password("Password: ", min_length=1)

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
            
            new_username = validasi_input_alphanumeric("Username Baru: ", min_length=3, max_length=20)
            
            if new_username in d.user_data:
                pesan_error("Username sudah terdaftar.")
            else:
                new_password = validasi_input_password("Password: ", min_length=4)
                
                d.user_data[new_username] = {"password": new_password, "role": "user", "member": False}
                pesan_sukses(f"Registrasi {new_username} berhasil. Silakan Login.")
            
            input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

        elif pilihan == "Keluar":
            clear()
            print(Fore.CYAN + Style.BRIGHT)
<<<<<<< HEAD
            print("╔════════════════════════════════════════╗")
            print("║    Terima kasih telah menggunakan      ║")
            print("║             TOKO OBAT SEHAT            ║")
            print("║          Semoga sehat selalu!          ║")
            print("╚════════════════════════════════════════╝")
=======
            print("╔═══════════════════════════════════════╗")
            print("║   Terima kasih telah menggunakan      ║")
            print("║      🏥 TOKO OBAT SEHAT 🏥            ║")
            print("║         Semoga sehat selalu!          ║")
            print("╚═══════════════════════════════════════╝")
>>>>>>> d498a503e0340641e641e6e85ea3370ccc8a53c1
            print(Style.RESET_ALL)
            d.run = False

    elif d.pengguna is not None:
        if d.role_pengguna == "apoteker":
            clear()
            header_box(f"ADMIN: {d.pengguna.upper()}", Fore.MAGENTA)
            
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
            header_box(f"USER: {d.pengguna.upper()}", Fore.CYAN)
            
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
                    
                    konfirmasi = validasi_konfirmasi_yn("Daftar jadi member? (y/n): ")
                    
                    if konfirmasi:
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
                    kodeObat = validasi_input_angka_positif("🔍 Masukkan kode obat: ", allow_zero=False)
                    if kodeObat in d.obat_data:
                        break
                    else:
                        pesan_error("Kode obat tidak ditemukan.")

                jumlahBeli = validasi_input_angka_positif(
                    f"📦 Jumlah beli {d.obat_data.get(kodeObat, {}).get('nama', 'Obat')}: ",
                    allow_zero=False
                )

                h.proses_pembelian(kodeObat, jumlahBeli)
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)

            elif opsi == "🚪 Logout":
                pesan_sukses(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None
                input(Fore.YELLOW + "\nTekan Enter untuk kembali..." + Style.RESET_ALL)
            