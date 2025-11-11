
from prettytable import PrettyTable
import data as d

def get_int_input(pilihan_opsi, min_nilai, max_nilai):
    while True:
        input_str = input(pilihan_opsi).strip()
        if not input_str:
            print("Input tidak boleh kosong.")
            continue
        try:
            pilihan = int(input_str)
            if min_nilai <= pilihan <= max_nilai:
                return pilihan
            else:
                print(f"Opsi tidak valid. Pilih antara {min_nilai} dan {max_nilai}.")
        except ValueError:
            print("Input harus berupa angka.")

# Cek ketersediaan data obat
def cek_obat_kosong():
    return not d.obat_data

# --- FUNGSI USER ---

def tampilkan_daftar_obat_user():
    print("\n--- Daftar Obat ---\n")
    if cek_obat_kosong():
        print("Data obat kosong.")
        return False
    
    table = PrettyTable()
    table.field_names = ["Kode", "Nama Obat", "Harga (Rp)", "Stok"]
    table.align = "l"

    for kodeObat, obat in d.obat_data.items():
        harga_formatted = f"{obat['harga']:,}"
        table.add_row([kodeObat, obat['nama'], harga_formatted, obat['stok']])
        
    print(table)
    return True

def proses_pembelian(kode_obat, jumlah_beli):
    if kode_obat not in d.obat_data:
        print("Kode obat tidak valid.")
        return False
    
    data_obat = d.obat_data[kode_obat]
    nama_obat = data_obat['nama']
    harga_satuan = data_obat['harga']

    if jumlah_beli <= 0:
        print("Jumlah beli harus positif.")
        return False
        
    if data_obat['stok'] < jumlah_beli:
        print(f"Stok {nama_obat} tidak mencukupi (Tersedia: {data_obat['stok']}).")
        
        def minta_jumlah_ulang(nama_obat, max_stok):
            print(f"Mohon masukkan ulang jumlah pembelian untuk {nama_obat}. Maksimal {max_stok}.")
            try:
                jumlah_baru_str = input("Jumlah Beli Baru (0 untuk batal): ").strip()
                if not jumlah_baru_str:
                    return minta_jumlah_ulang(nama_obat, max_stok)
                jumlah_baru = int(jumlah_baru_str)
                if jumlah_baru == 0:
                    print("Pembelian dibatalkan.")
                    return 0
                elif jumlah_baru < 0:
                    print("Jumlah tidak boleh negatif.")
                    return minta_jumlah_ulang(nama_obat, max_stok)
                elif jumlah_baru > max_stok:
                    print(f"Jumlah melebihi stok tersedia ({max_stok}).")
                    return minta_jumlah_ulang(nama_obat, max_stok) 
                else:
                    return jumlah_baru
            except ValueError:
                print("Input harus berupa angka.")
                return minta_jumlah_ulang(nama_obat, max_stok)

        jumlah_beli_baru = minta_jumlah_ulang(nama_obat, data_obat['stok'])
        if jumlah_beli_baru == 0:
            return False
        jumlah_beli = jumlah_beli_baru

    # Lakukan Transaksi
    data_obat['stok'] -= jumlah_beli
    total_harga = jumlah_beli * harga_satuan
    
    table_transaksi = PrettyTable()
    table_transaksi.field_names = ["Keterangan", "Nilai"]
    table_transaksi.align = "l"
    table_transaksi.add_row(["Obat", nama_obat])
    table_transaksi.add_row(["Jumlah", jumlah_beli])
    table_transaksi.add_row(["Total Harga (Rp)", f"{total_harga:,}"])
    
    print("\nPembelian berhasil:")
    print(table_transaksi)
    return True
    
# --- FUNGSI ADMIN ---

# Menampilkan Daftar Obat Lengkap (Admin View)
def prosedur_tampilkan_obat_admin():
    if cek_obat_kosong():
        print("Data obat kosong.")
        return
        
    print("\n--- Daftar Obat (Admin) ---")
    
    table = PrettyTable()
    table.field_names = ["Kode", "Nama Obat", "Stok", "Harga (Rp)"]
    table.align = "l"

    for kodeObat, obat in d.obat_data.items():
        harga_formatted = f"{obat['harga']:,}"
        table.add_row([kodeObat, obat['nama'], obat['stok'], harga_formatted])
        
    print(table)


# Proses Tambah Obat Baru
def prosedur_tambah_obat_baru():
    print("\n--- Tambah Obat Baru ---")
    
    nama = input("Nama Obat: ").strip()
    if not nama:
        print("Nama obat tidak boleh kosong. Penambahan dibatalkan.")
        return

    # Validasi Stok
    while True:
        try:
            stok = int(input("Stok: ").strip())
            if stok >= 0:
                break
            else:
                print("Stok tidak boleh negatif.")
        except ValueError:
            print("Stok harus berupa angka.")

    # Validasi Harga
    while True:
        try:
            harga = int(input("Harga: ").strip())
            if harga >= 0:
                break
            else:
                print("Harga tidak boleh negatif.")
        except ValueError:
            print("Harga harus berupa angka.")
            
    d.obat_data[d.next_kode_obat] = {"nama": nama, "stok": stok, "harga": harga}
    print(f"Obat '{nama}' berhasil ditambahkan dengan kode {d.next_kode_obat}.")
    d.next_kode_obat += 1

# Proses Perbarui Obat (Stok/Harga)
def prosedur_perbarui_obat():
    print("\n--- Perbarui Obat ---")
    prosedur_tampilkan_obat_admin()

    # Input Kode Obat
    kodeObat = None
    while True:
        inputKode = input("Masukkan kode obat yang akan diubah: ").strip()
        try:
            kodeObat = int(inputKode)
            break
        except ValueError:
            print("Kode obat harus berupa angka.")
            
    if kodeObat in d.obat_data:
        print(f"Obat yang dipilih: {d.obat_data[kodeObat]['nama']}")
        
        stok_baru_str = input("Masukkan Stok Baru (kosongkan jika tidak diubah): ").strip()
        harga_baru_str = input("Masukkan Harga Baru (kosongkan jika tidak diubah): ").strip()

        updated = False
        
        # Cek dan update stok
        if stok_baru_str:
            try:
                stokBaru = int(stok_baru_str)
                if stokBaru >= 0:
                    d.obat_data[kodeObat]['stok'] = stokBaru
                    updated = True
                else:
                    print("Stok tidak boleh negatif. Perubahan stok dibatalkan.")
            except ValueError:
                print("Stok harus berupa angka. Perubahan stok dibatalkan.")

        # Cek dan update harga 
        if harga_baru_str:
            try:
                hargaBaru = int(harga_baru_str)
                if hargaBaru >= 0:
                    d.obat_data[kodeObat]['harga'] = hargaBaru
                    updated = True
                else:
                    print("Harga tidak boleh negatif. Perubahan harga dibatalkan.")
            except ValueError:
                print("Harga harus berupa angka. Perubahan harga dibatalkan.")
                
        if updated:
            print(f"Kode obat {kodeObat} berhasil diperbarui. Data terbaru:")
            # Tampilkan data obat yang baru diperbarui
            table_update = PrettyTable()
            table_update.field_names = ["Kode", "Nama Obat", "Stok", "Harga (Rp)"]
            table_update.align = "l"
            obat_diperbarui = d.obat_data[kodeObat]
            harga_formatted = f"{obat_diperbarui['harga']:,}"
            table_update.add_row([kodeObat, obat_diperbarui['nama'], obat_diperbarui['stok'], harga_formatted])
            print(table_update)
            
        elif not stok_baru_str and not harga_baru_str:
            print("Tidak ada perubahan dilakukan.")
    else:
        print(f"Kode obat {kodeObat} tidak ditemukan.")

# Proses Hapus Obat
def prosedur_hapus_obat():
    print("\n--- Hapus Obat ---")
    prosedur_tampilkan_obat_admin()
    kodeObat = None
    while True:
        inputKode = input("Masukkan kode obat yang akan dihapus: ").strip()
        try:
            kodeObat = int(inputKode)
            break
        except ValueError:
            print("Kode obat harus berupa angka.")
    
    if kodeObat in d.obat_data:
        nama_obat_hapus = d.obat_data[kodeObat]['nama']
        del d.obat_data[kodeObat]
        print(f"Obat '{nama_obat_hapus}' (Kode {kodeObat}) berhasil dihapus.")
    else:
        print(f"Kesalahan: Kode obat {kodeObat} tidak ditemukan.")