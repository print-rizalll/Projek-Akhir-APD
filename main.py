from prettytable import PrettyTable
import data as d 
import handler as h
import os
tabel1 = PrettyTable()
tabel2 = PrettyTable()
tabel3 = PrettyTable()

def clear():
    os.system("cls || clear")
    
while d.run:
    if d.pengguna is None:
        # --- MENU PRE-LOGIN ---
        tabel1 = PrettyTable()
        tabel1.field_names = ["=== Selamat Datang di Toko Obat Sehat ==="]
        tabel1.add_row(["1. Login"])
        tabel1.add_row(["2. Registrasi"])
        tabel1.add_row(["3. Keluar"])
        print (tabel1)
        pilihan = h.get_int_input("Pilih Opsi (1-3): ", 1, 3) 
        clear()
        
        if pilihan == 1:
            # --- Login ---
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
                
        elif pilihan == 2:
            # --- Registrasi ---
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
                    d.user_data[new_username] = {"password": new_password, "role": "user"}
                    print(f"Registrasi {new_username} berhasil. Silakan Login.")
                    
        elif pilihan == 3:
            # --- Keluar Program ---
            d.run = False
            print("Terima kasih, program diakhiri.")
            
    elif d.pengguna is not None:
        if d.role_pengguna == "apoteker":
            # --- MENU ADMIN  ---
            tabel2 = PrettyTable()
            tabel2.field_names = ["=== Menu Admin ==="]
            tabel2.add_row(["1. Lihat Daftar Obat"])
            tabel2.add_row(["2. Tambah Obat Baru"])
            tabel2.add_row(["3. Perbarui Stok/Harga Obat"])
            tabel2.add_row(["4. Hapus Obat"])
            tabel2.add_row(["5. Logout"])
            print (tabel2)
            opsi_menu = h.get_int_input("Pilih Opsi (1-5): ", 1, 5)
            
            
            # pilihan Menu Admin
            if opsi_menu == 1:
                h.prosedur_tampilkan_obat_admin()

            elif opsi_menu == 2:
                h.prosedur_tambah_obat_baru()

            elif opsi_menu == 3:
                h.prosedur_perbarui_obat() 

            elif opsi_menu == 4:
                h.prosedur_hapus_obat() 

            # 5. Logout
            elif opsi_menu == 5:
                print(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None
            
        elif d.role_pengguna == "user":
            # --- MENU USER BIASA ---
            tabel3 = PrettyTable()
            tabel3.field_names = ["=== Menu ==="]
            tabel3.add_row(["1. Lihat Daftar Obat"])
            tabel3.add_row(["2. Beli Obat"])
            tabel3.add_row(["3. Logout"])
            print(tabel3)
            opsi_menu = h.get_int_input("Pilih Opsi (1-3): ", 1, 3)
            
            # Pilihan Menu User
            if opsi_menu == 1:
                h.tampilkan_daftar_obat_user()
                
            elif opsi_menu == 2:
                # --- BELI OBAT ---
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
                
            # 3. Logout
            elif opsi_menu == 3:
                print(f"Pengguna {d.pengguna} berhasil logout.")
                d.pengguna = None
                d.role_pengguna = None