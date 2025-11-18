from prettytable import PrettyTable
import data as d
import inquirer
from colorama import Fore, Style, init

init(autoreset=True)

def get_int_input(pilihan_opsi, min_nilai, max_nilai):
    while True:
        input_str = input(Fore.YELLOW + pilihan_opsi + Style.RESET_ALL).strip()
        if not input_str:
            print(Fore.RED + "❌ Input tidak boleh kosong." + Style.RESET_ALL)
            continue
        try:
            pilihan = int(input_str)
            if min_nilai <= pilihan <= max_nilai:
                return pilihan
            else:
                print(Fore.RED + f"❌ Opsi tidak valid. Pilih antara {min_nilai} dan {max_nilai}." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Input harus berupa angka." + Style.RESET_ALL)

def cek_obat_kosong():
    return not d.obat_data

def tampilkan_daftar_obat_user():
    if cek_obat_kosong():
        print(Fore.RED + "❌ Data obat kosong." + Style.RESET_ALL)
        return False
    
    table = PrettyTable()
    table.title = Fore.CYAN + Style.BRIGHT + "📋 DAFTAR OBAT" + Style.RESET_ALL
    table.field_names = [
        Fore.YELLOW + "Kode" + Style.RESET_ALL,
        Fore.YELLOW + "Nama Obat" + Style.RESET_ALL,
        Fore.YELLOW + "Harga (Rp)" + Style.RESET_ALL,
        Fore.YELLOW + "Stok" + Style.RESET_ALL
    ]
    table.align = "l"

    for kodeObat, obat in d.obat_data.items():
        harga_formatted = f"{obat['harga']:,}"
        stok_display = Fore.GREEN + str(obat['stok']) + Style.RESET_ALL if obat['stok'] >= 20 else Fore.RED + str(obat['stok']) + Style.RESET_ALL
        table.add_row([kodeObat, obat['nama'], harga_formatted, stok_display])
        
    print(table)
    return True

def proses_pembelian(kode_obat, jumlah_beli):
    if kode_obat not in d.obat_data:
        print(Fore.RED + "❌ Kode obat tidak valid." + Style.RESET_ALL)
        return False
    
    data_obat = d.obat_data[kode_obat]
    nama_obat = data_obat['nama']
    harga_satuan = data_obat['harga']

    if jumlah_beli <= 0:
        print(Fore.RED + "❌ Jumlah beli harus positif." + Style.RESET_ALL)
        return False
        
    if data_obat['stok'] < jumlah_beli:
        print(Fore.RED + f"❌ Stok {nama_obat} tidak mencukupi (Tersedia: {data_obat['stok']})." + Style.RESET_ALL)
        
        def minta_jumlah_ulang(nama_obat, max_stok):
            print(Fore.YELLOW + f"ℹ️  Mohon masukkan ulang jumlah pembelian untuk {nama_obat}. Maksimal {max_stok}." + Style.RESET_ALL)
            try:
                jumlah_baru_str = input(Fore.CYAN + "Jumlah Beli Baru (0 untuk batal): " + Style.RESET_ALL).strip()
                if not jumlah_baru_str:
                    return minta_jumlah_ulang(nama_obat, max_stok)
                jumlah_baru = int(jumlah_baru_str)
                if jumlah_baru == 0:
                    print(Fore.YELLOW + "ℹ️  Pembelian dibatalkan." + Style.RESET_ALL)
                    return 0
                elif jumlah_baru < 0:
                    print(Fore.RED + "❌ Jumlah tidak boleh negatif." + Style.RESET_ALL)
                    return minta_jumlah_ulang(nama_obat, max_stok)
                elif jumlah_baru > max_stok:
                    print(Fore.RED + f"❌ Jumlah melebihi stok tersedia ({max_stok})." + Style.RESET_ALL)
                    return minta_jumlah_ulang(nama_obat, max_stok) 
                else:
                    return jumlah_baru
            except ValueError:
                print(Fore.RED + "❌ Input harus berupa angka." + Style.RESET_ALL)
                return minta_jumlah_ulang(nama_obat, max_stok)

        jumlah_beli_baru = minta_jumlah_ulang(nama_obat, data_obat['stok'])
        if jumlah_beli_baru == 0:
            return False
        jumlah_beli = jumlah_beli_baru

    data_obat['stok'] -= jumlah_beli
    total_harga = jumlah_beli * harga_satuan

    is_member = d.user_data[d.pengguna]["member"]
    if is_member:
        diskon = int(total_harga * 0.10)
        total_setelah_diskon = total_harga - diskon
    else:
        diskon = 0
        total_setelah_diskon = total_harga
    
    table_transaksi = PrettyTable()
    table_transaksi.field_names = [
        Fore.CYAN + "Keterangan" + Style.RESET_ALL, 
        Fore.CYAN + "Nilai" + Style.RESET_ALL
    ]
    table_transaksi.align = "l"
    table_transaksi.add_row(["Obat", Fore.GREEN + nama_obat + Style.RESET_ALL])
    table_transaksi.add_row(["Jumlah", jumlah_beli])
    table_transaksi.add_row(["Total Harga (Rp)", f"{total_harga:,}"])
    
    if is_member:
        table_transaksi.add_row(["Diskon Member (Rp)", Fore.GREEN + f"-{diskon:,}" + Style.RESET_ALL])
    else:
        table_transaksi.add_row(["Diskon Member (Rp)", f"{diskon:,}"])
    
    table_transaksi.add_row([
        Fore.YELLOW + Style.BRIGHT + "Total Bayar (Rp)" + Style.RESET_ALL, 
        Fore.GREEN + Style.BRIGHT + f"{total_setelah_diskon:,}" + Style.RESET_ALL
    ])

    print(Fore.GREEN + "\n✅ Pembelian berhasil:" + Style.RESET_ALL)
    print(table_transaksi)
    return True


def filter_obat_user():
    if cek_obat_kosong():
        print(Fore.RED + "\n❌ Tidak ada obat yang tersedia." + Style.RESET_ALL)
        return
    
    print(Fore.CYAN + "\n╔════════════════════════════════════════╗")
    print(Fore.CYAN + "║     🔍 FILTER & CARI OBAT             ║")
    print(Fore.CYAN + "╚════════════════════════════════════════╝" + Style.RESET_ALL)

    menu_filter = [
        inquirer.List(
            "pilihan",
            message=Fore.CYAN + "Pilih jenis filter:" + Style.RESET_ALL,
            choices=[
                "🔎 Cari berdasarkan Nama Obat",
                "💰 Harga Termurah",
                "💎 Harga Termahal",
                "📦 Stok Terbanyak",
                "⚠️  Stok Tersedikit",
                "⬅️  Kembali"
            ]
        )
    ]

    jawaban = inquirer.prompt(menu_filter)
    opsi = jawaban["pilihan"]

    if opsi == "🔎 Cari berdasarkan Nama Obat":
        keyword = input(Fore.CYAN + "🔍 Masukkan nama obat: " + Style.RESET_ALL).strip().lower()
        if not keyword:
            print(Fore.RED + "❌ Nama tidak boleh kosong." + Style.RESET_ALL)
            return
        
        hasil = {k: v for k, v in d.obat_data.items() if keyword in v["nama"].lower()}
        if not hasil:
            print(Fore.RED + f"❌ Tidak ditemukan obat dengan nama '{keyword}'." + Style.RESET_ALL)
            return

        tampilkan_hasil_filter(hasil.items(), f"Hasil Pencarian: '{keyword}'")

    elif opsi == "💰 Harga Termurah":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["harga"])
        tampilkan_hasil_filter(sorted_obat, "💰 Harga Termurah")

    elif opsi == "💎 Harga Termahal":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["harga"], reverse=True)
        tampilkan_hasil_filter(sorted_obat, "💎 Harga Termahal")

    elif opsi == "📦 Stok Terbanyak":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["stok"], reverse=True)
        tampilkan_hasil_filter(sorted_obat, "📦 Stok Terbanyak")

    elif opsi == "⚠️  Stok Tersedikit":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["stok"])
        tampilkan_hasil_filter(sorted_obat, "⚠️  Stok Tersedikit")

    elif opsi == "⬅️  Kembali":
        return


def filter_obat_admin():
    if cek_obat_kosong():
        print(Fore.RED + "\n❌ Tidak ada obat yang tersedia." + Style.RESET_ALL)
        return

    print(Fore.MAGENTA + "\n╔════════════════════════════════════════╗")
    print(Fore.MAGENTA + "║   🔍 FILTER & KELOLA OBAT (ADMIN)    ║")
    print(Fore.MAGENTA + "╚════════════════════════════════════════╝" + Style.RESET_ALL)

    menu_filter = [
        inquirer.List(
            "pilihan",
            message=Fore.MAGENTA + "Pilih jenis filter:" + Style.RESET_ALL,
            choices=[
                "🔎 Cari berdasarkan Nama Obat",
                "💰 Harga Termurah",
                "💎 Harga Termahal",
                "📦 Stok Terbanyak",
                "⚠️  Stok Tersedikit",
                "🔴 Stok Rendah (< 20)",
                "⬅️  Kembali"
            ]
        )
    ]

    jawaban = inquirer.prompt(menu_filter)
    opsi = jawaban["pilihan"]

    if opsi == "🔎 Cari berdasarkan Nama Obat":
        keyword = input(Fore.CYAN + "🔍 Masukkan nama obat: " + Style.RESET_ALL).strip().lower()
        if not keyword:
            print(Fore.RED + "❌ Nama tidak boleh kosong." + Style.RESET_ALL)
            return
        
        hasil = {k: v for k, v in d.obat_data.items() if keyword in v["nama"].lower()}
        if not hasil:
            print(Fore.RED + f"❌ Tidak ditemukan obat dengan nama '{keyword}'." + Style.RESET_ALL)
            return

        tampilkan_hasil_filter_admin(hasil.items(), f"Hasil Pencarian: '{keyword}'")

    elif opsi == "💰 Harga Termurah":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["harga"])
        tampilkan_hasil_filter_admin(sorted_obat, "💰 Harga Termurah")

    elif opsi == "💎 Harga Termahal":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["harga"], reverse=True)
        tampilkan_hasil_filter_admin(sorted_obat, "💎 Harga Termahal")

    elif opsi == "📦 Stok Terbanyak":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["stok"], reverse=True)
        tampilkan_hasil_filter_admin(sorted_obat, "📦 Stok Terbanyak")

    elif opsi == "⚠️  Stok Tersedikit":
        sorted_obat = sorted(d.obat_data.items(), key=lambda x: x[1]["stok"])
        tampilkan_hasil_filter_admin(sorted_obat, "⚠️  Stok Tersedikit")

    elif opsi == "🔴 Stok Rendah (< 20)":
        stok_rendah = {k: v for k, v in d.obat_data.items() if v["stok"] < 20}
        if not stok_rendah:
            print(Fore.GREEN + "Semua obat memiliki stok mencukupi." + Style.RESET_ALL)
            return

        tampilkan_hasil_filter_admin(stok_rendah.items(), "🔴 Stok Rendah (< 20)")

    elif opsi == "⬅️  Kembali":
        return


def tampilkan_hasil_filter(sorted_obat, judul):
    table = PrettyTable()
    table.title = Fore.CYAN + Style.BRIGHT + f"📋 {judul}" + Style.RESET_ALL
    table.field_names = [
        Fore.YELLOW + "Kode" + Style.RESET_ALL,
        Fore.YELLOW + "Nama Obat" + Style.RESET_ALL,
        Fore.YELLOW + "Harga (Rp)" + Style.RESET_ALL,
        Fore.YELLOW + "Stok" + Style.RESET_ALL
    ]
    table.align = "l"
    
    for kode, obat in sorted_obat:
        stok_display = Fore.GREEN + str(obat['stok']) + Style.RESET_ALL if obat['stok'] >= 20 else Fore.RED + str(obat['stok']) + Style.RESET_ALL
        table.add_row([kode, obat['nama'], f"{obat['harga']:,}", stok_display])
    
    print(table)

def tampilkan_hasil_filter_admin(sorted_obat, judul):
    table = PrettyTable()
    table.title = Fore.MAGENTA + Style.BRIGHT + f"📋 {judul}" + Style.RESET_ALL
    table.field_names = [
        Fore.YELLOW + "Kode" + Style.RESET_ALL,
        Fore.YELLOW + "Nama Obat" + Style.RESET_ALL,
        Fore.YELLOW + "Stok" + Style.RESET_ALL,
        Fore.YELLOW + "Harga (Rp)" + Style.RESET_ALL
    ]
    table.align = "l"
    
    for kode, obat in sorted_obat:
        stok_display = Fore.GREEN + str(obat['stok']) + Style.RESET_ALL if obat['stok'] >= 20 else Fore.RED + str(obat['stok']) + Style.RESET_ALL
        table.add_row([kode, obat['nama'], stok_display, f"{obat['harga']:,}"])
    
    print(table)

    
def prosedur_tampilkan_obat_admin():
    if cek_obat_kosong():
        print(Fore.RED + "❌ Data obat kosong." + Style.RESET_ALL)
        return
    
    table = PrettyTable()
    table.title = Fore.MAGENTA + Style.BRIGHT + "📋 DAFTAR OBAT (ADMIN)" + Style.RESET_ALL
    table.field_names = [
        Fore.YELLOW + "Kode" + Style.RESET_ALL,
        Fore.YELLOW + "Nama Obat" + Style.RESET_ALL,
        Fore.YELLOW + "Stok" + Style.RESET_ALL,
        Fore.YELLOW + "Harga (Rp)" + Style.RESET_ALL
    ]
    table.align = "l"

    for kodeObat, obat in d.obat_data.items():
        harga_formatted = f"{obat['harga']:,}"
        stok_display = Fore.GREEN + str(obat['stok']) + Style.RESET_ALL if obat['stok'] >= 20 else Fore.RED + str(obat['stok']) + Style.RESET_ALL
        table.add_row([kodeObat, obat['nama'], stok_display, harga_formatted])
        
    print(table)

def prosedur_tambah_obat_baru():
    nama = input(Fore.CYAN + "📝 Nama Obat: " + Style.RESET_ALL).strip()
    if not nama:
        print(Fore.RED + "❌ Nama obat tidak boleh kosong. Penambahan dibatalkan." + Style.RESET_ALL)
        return

    while True:
        try:
            stok = int(input(Fore.CYAN + "📦 Stok: " + Style.RESET_ALL).strip())
            if stok >= 0:
                break
            else:
                print(Fore.RED + "❌ Stok tidak boleh negatif." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Stok harus berupa angka." + Style.RESET_ALL)

    while True:
        try:
            harga = int(input(Fore.CYAN + "💰 Harga: " + Style.RESET_ALL).strip())
            if harga >= 0:
                break
            else:
                print(Fore.RED + "❌ Harga tidak boleh negatif." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Harga harus berupa angka." + Style.RESET_ALL)
            
    d.obat_data[d.next_kode_obat] = {"nama": nama, "stok": stok, "harga": harga}
    print(Fore.GREEN + f"✅ Obat '{nama}' berhasil ditambahkan dengan kode {d.next_kode_obat}." + Style.RESET_ALL)
    d.next_kode_obat += 1

def prosedur_perbarui_obat():
    prosedur_tampilkan_obat_admin()

    kodeObat = None
    while True:
        inputKode = input(Fore.YELLOW + "\n📝 Masukkan kode obat yang akan diubah: " + Style.RESET_ALL).strip()
        try:
            kodeObat = int(inputKode)
            break
        except ValueError:
            print(Fore.RED + "❌ Kode obat harus berupa angka." + Style.RESET_ALL)
            
    if kodeObat in d.obat_data:
        print(Fore.CYAN + f"📋 Obat yang dipilih: {d.obat_data[kodeObat]['nama']}" + Style.RESET_ALL)
        
        stok_baru_str = input(Fore.YELLOW + "📦 Stok Baru (kosongkan jika tidak diubah): " + Style.RESET_ALL).strip()
        harga_baru_str = input(Fore.YELLOW + "💰 Harga Baru (kosongkan jika tidak diubah): " + Style.RESET_ALL).strip()

        updated = False
        
        if stok_baru_str:
            try:
                stokBaru = int(stok_baru_str)
                if stokBaru >= 0:
                    d.obat_data[kodeObat]['stok'] = stokBaru
                    updated = True
                else:
                    print(Fore.RED + "❌ Stok tidak boleh negatif. Perubahan stok dibatalkan." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "❌ Stok harus berupa angka. Perubahan stok dibatalkan." + Style.RESET_ALL)

        if harga_baru_str:
            try:
                hargaBaru = int(harga_baru_str)
                if hargaBaru >= 0:
                    d.obat_data[kodeObat]['harga'] = hargaBaru
                    updated = True
                else:
                    print(Fore.RED + "❌ Harga tidak boleh negatif. Perubahan harga dibatalkan." + Style.RESET_ALL)
            except ValueError:
                print(Fore.RED + "❌ Harga harus berupa angka. Perubahan harga dibatalkan." + Style.RESET_ALL)
                
        if updated:
            print(Fore.GREEN + f"\n✅ Kode obat {kodeObat} berhasil diperbarui. Data terbaru:" + Style.RESET_ALL)
            table_update = PrettyTable()
            table_update.field_names = [
                Fore.YELLOW + "Kode" + Style.RESET_ALL,
                Fore.YELLOW + "Nama Obat" + Style.RESET_ALL,
                Fore.YELLOW + "Stok" + Style.RESET_ALL,
                Fore.YELLOW + "Harga (Rp)" + Style.RESET_ALL
            ]
            table_update.align = "l"
            obat_diperbarui = d.obat_data[kodeObat]
            harga_formatted = f"{obat_diperbarui['harga']:,}"
            stok_display = Fore.GREEN + str(obat_diperbarui['stok']) + Style.RESET_ALL if obat_diperbarui['stok'] >= 20 else Fore.RED + str(obat_diperbarui['stok']) + Style.RESET_ALL
            table_update.add_row([kodeObat, obat_diperbarui['nama'], stok_display, harga_formatted])
            print(table_update)
            
        elif not stok_baru_str and not harga_baru_str:
            print(Fore.YELLOW + "ℹ️  Tidak ada perubahan dilakukan." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Kode obat {kodeObat} tidak ditemukan." + Style.RESET_ALL)

def prosedur_hapus_obat():
    prosedur_tampilkan_obat_admin()
    kodeObat = None
    while True:
        inputKode = input(Fore.YELLOW + "\n🗑️  Masukkan kode obat yang akan dihapus: " + Style.RESET_ALL).strip()
        try:
            kodeObat = int(inputKode)
            break
        except ValueError:
            print(Fore.RED + "❌ Kode obat harus berupa angka." + Style.RESET_ALL)
    
    if kodeObat in d.obat_data:
        nama_obat_hapus = d.obat_data[kodeObat]['nama']
        del d.obat_data[kodeObat]
        print(Fore.GREEN + f"✅ Obat '{nama_obat_hapus}' (Kode {kodeObat}) berhasil dihapus." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Kesalahan: Kode obat {kodeObat} tidak ditemukan." + Style.RESET_ALL)