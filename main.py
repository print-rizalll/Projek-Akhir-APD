from prettytable import PrettyTable
import data as d 
import handler as h
import os
import inquirer

tabel1 = PrettyTable()
tabel2 = PrettyTable()
tabel3 = PrettyTable()

def clear():
    os.system("cls || clear")

while d.run:
    if d.pengguna is None:
        menu_utama = [
            inquirer.List(
                "pilihan",
                message="=== Selamat Datang di Toko Obat Sehat ===",
                choices=["Login", "Registrasi", "Keluar"]
            )
        ]
        jawaban = inquirer.prompt(menu_utama)
        pilihan = jawaban["pilihan"]
        clear()

        if pilihan == "Login":
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            if username in d.user_data:
                if d.user_data[username]["password"] == password:
                    d.pengguna = username
                    d.role_pengguna = d.user_data[username]["role"]
                    print(f"Login berhasil! Selamat datang, {username} ({d.role_pengguna}).")
                    continue
                else:
                    print("Password salah.")
            else:
                print("Username tidak ditemukan.")

        elif pilihan == "Registrasi":
            print("\n--- Registrasi Pengguna Baru ---")
            new_username = input("Masukkan Username Baru: ").strip()
            new_password = input("Masukkan Password: ").strip()

            if not new_username or not new_password:
                print("Username dan Password tidak boleh kosong.")
            elif new_username in d.user_data:
                print("Username sudah terdaftar.")
            else:
                if len(new_password) < 4:
                    print("Password minimal 4 karakter.")
                else:
                    d.user_data[new_username] = {"password": new_password, "role": "user", "member": False}
                    print(f"Registrasi {new_username} berhasil. Silakan Login.")

        elif pilihan == "Keluar":
            d.run = False
            print("Terima kasih, program diakhiri.")

    elif d.pengguna is not None:
        if d.role_pengguna == "apoteker":
            menu_admin = [
                inquirer.List(
                    "opsi",
                    message="=== Menu Admin ===",
                    choices=[
                        "Lihat Daftar Obat",
                        "Tambah Obat Baru",
                        "Perbarui Stok/Harga Obat",
                        "Hapus Obat",
                        "Logout"
                    ]
                )
            ]
            jawaban = inquirer.prompt(menu_admin)
            opsi = jawaban["opsi"]

            if opsi == "Lihat Daftar Obat":
                h.prosedur_tampilkan_obat_admin()
            elif opsi == "Tambah Obat Baru":
                h.prosedur_tambah_obat_baru()
            elif opsi == "Perbarui Stok/Harga Obat":
                h.prosedur_perbarui_obat()
            elif opsi == "Hapus Obat":
                h.prosedur_hapus_obat()
            elif opsi == "Logout":
                print(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None

        elif d.role_pengguna == "user":
            menu_user = [
                inquirer.List(
                    "opsi",
                    message="=== Menu Pengguna ===",
                    choices=["Lihat Daftar Obat", "Beli Obat", "Daftar Member", "Logout"]
                )
            ]
            jawaban = inquirer.prompt(menu_user)
            opsi = jawaban["opsi"]

            if opsi == "Lihat Daftar Obat":
                h.tampilkan_daftar_obat_user()

            elif opsi == "Daftar Member":
                if d.user_data[d.pengguna]["member"]:
                    print("Kamu sudah menjadi member!")
                else:
                    konfirmasi = input("Daftar jadi member? (y/n): ").strip().lower()
                    if konfirmasi == "y":
                        d.user_data[d.pengguna]["member"] = True
                        print("Selamat! Kamu sekarang member (diskon 10%).")
                    else:
                        print("Pendaftaran member dibatalkan.")

            elif opsi == "Beli Obat":
                if h.cek_obat_kosong():
                    print("\nTidak ada obat yang tersedia untuk dibeli.")
                    continue

                h.tampilkan_daftar_obat_user()
                print("\n--- Proses Pembelian Obat ---")

                kodeObat = None
                while True:
                    inputKode = input("Masukkan kode obat yang akan dibeli: ").strip()
                    try:
                        kodeObat = int(inputKode)
                        if kodeObat in d.obat_data:
                            break
                        else:
                            print("Kode obat tidak ditemukan.")
                    except ValueError:
                        print("Kode obat harus berupa angka.")

                jumlahBeli = None
                while True:
                    inputJumlah = input(f"Masukkan jumlah beli {d.obat_data.get(kodeObat, {}).get('nama', 'Obat')}: ").strip()
                    try:
                        jumlahBeli = int(inputJumlah)
                        break
                    except ValueError:
                        print("Jumlah beli harus berupa angka.")

                h.proses_pembelian(kodeObat, jumlahBeli)

            elif opsi == "Logout":
                print(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None
