from prettytable import PrettyTable
import data as d
import inquirer
from colorama import Fore, Style, init

init(autoreset=True)
BATAS_STOK = 10000
BATAS_HARGA = 10000000

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

def validasi_input_angka_positif(prompt, allow_zero=False, allow_empty=False, max_value=None):
    while True:
        input_str = input(Fore.YELLOW + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            if allow_empty:
                return None
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
            
            if max_value is not None and nilai > max_value:
                print(Fore.RED + f"❌ Input melebihi batas maksimal ({max_value:,})." + Style.RESET_ALL)
                continue
            
            return nilai
            
        except ValueError:
            print(Fore.RED + "❌ Input harus berupa angka yang valid." + Style.RESET_ALL)


def validasi_nama_obat(prompt):
    while True:
        input_str = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            print(Fore.RED + "❌ Nama obat tidak boleh kosong." + Style.RESET_ALL)
            continue
        
        if len(input_str) < 2:
            print(Fore.RED + "❌ Nama obat minimal 2 karakter." + Style.RESET_ALL)
            continue
        
        cleaned = input_str.replace(" ", "")
        if not cleaned.isalnum():
            print(Fore.RED + "❌ Nama obat hanya boleh berupa huruf, angka, dan spasi. Tidak boleh ada simbol." + Style.RESET_ALL)
            continue
        
        if not any(c.isalpha() for c in input_str):
            print(Fore.RED + "❌ Nama obat harus mengandung minimal satu huruf." + Style.RESET_ALL)
            continue
        
        return input_str


def validasi_input_pencarian(prompt):
    while True:
        input_str = input(Fore.CYAN + prompt + Style.RESET_ALL).strip()
        
        if not input_str:
            print(Fore.RED + "❌ Kata kunci pencarian tidak boleh kosong." + Style.RESET_ALL)
            continue
        
        if len(input_str) < 2:
            print(Fore.RED + "❌ Kata kunci minimal 2 karakter." + Style.RESET_ALL)
            continue
        
        cleaned = input_str.replace(" ", "")
        if not cleaned.isalnum():
            print(Fore.RED + "❌ Kata kunci hanya boleh berupa huruf, angka, dan spasi." + Style.RESET_ALL)
            continue
        
        return input_str


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
            
            jumlah_baru = validasi_input_angka_positif(
                "Jumlah Beli Baru (0 untuk batal): ", 
                allow_zero=True, 
                allow_empty=False
            )
            
            if jumlah_baru == 0:
                print(Fore.YELLOW + "ℹ️  Pembelian dibatalkan." + Style.RESET_ALL)
                return 0
            elif jumlah_baru > max_stok:
                print(Fore.RED + f"❌ Jumlah melebihi stok tersedia ({max_stok})." + Style.RESET_ALL)
                return minta_jumlah_ulang(nama_obat, max_stok) 
            else:
                return jumlah_baru

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
    
    print(Fore.CYAN + "\n╔═══════════════════════════════════════╗")
    print(Fore.CYAN + "║     🔍 FILTER & CARI OBAT             ║")
    print(Fore.CYAN + "╚═══════════════════════════════════════╝" + Style.RESET_ALL)

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
        keyword = validasi_input_pencarian("🔍 Masukkan nama obat: ")
        keyword_lower = keyword.lower().strip()  # CASE-INSENSITIVE
        
        # Pencarian case-insensitive
        hasil = {k: v for k, v in d.obat_data.items() 
                if keyword_lower in v["nama"].lower()}
        
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

    print(Fore.MAGENTA + "\n╔═══════════════════════════════════════╗")
    print(Fore.MAGENTA + "║   🔍 FILTER & KELOLA OBAT (ADMIN)    ║")
    print(Fore.MAGENTA + "╚═══════════════════════════════════════╝" + Style.RESET_ALL)

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
        keyword = validasi_input_pencarian("🔍 Masukkan nama obat: ")
        keyword_lower = keyword.lower().strip()  # CASE-INSENSITIVE
        
        # Pencarian case-insensitive
        hasil = {k: v for k, v in d.obat_data.items() 
                if keyword_lower in v["nama"].lower()}
        
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
            print(Fore.GREEN + "✅ Semua obat memiliki stok mencukupi." + Style.RESET_ALL)
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
    nama = validasi_nama_obat("📖 Nama Obat: ")

    nama_lower = nama.lower().strip()
    obat_existing = None
    kode_existing = None
    
    for kode, data_obat in d.obat_data.items():
        if data_obat['nama'].lower().strip() == nama_lower:
            obat_existing = data_obat
            kode_existing = kode
            break
    
    if obat_existing:
        print(Fore.YELLOW + "⚠️  Obat sudah ada dalam database!" + Style.RESET_ALL)
        print(Fore.CYAN + f"ℹ️  Nama: {obat_existing['nama']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"ℹ️  Kode: {kode_existing}" + Style.RESET_ALL)
        print(Fore.CYAN + f"ℹ️  Stok saat ini: {obat_existing['stok']}" + Style.RESET_ALL)
        print(Fore.CYAN + f"ℹ️  Harga saat ini: Rp {obat_existing['harga']:,}" + Style.RESET_ALL)
        print()
        
        konfirmasi = validasi_konfirmasi_yn("Apakah ingin menambah stok obat ini? (y/n): ")
        
        if konfirmasi:
            stok_tambahan = validasi_input_angka_positif(
                f"📦 Jumlah stok yang ditambahkan (Maks {BATAS_STOK:,}): ", 
                allow_zero=False,
                max_value=BATAS_STOK
            )
            
            stok_lama = obat_existing['stok']
            obat_existing['stok'] += stok_tambahan
            
            print(Fore.GREEN + f"\n✅ Stok berhasil ditambahkan!" + Style.RESET_ALL)
            print(Fore.CYAN + f"   • Stok lama: {stok_lama}" + Style.RESET_ALL)
            print(Fore.CYAN + f"   • Ditambah: +{stok_tambahan}" + Style.RESET_ALL)
            print(Fore.GREEN + f"   • Stok baru: {obat_existing['stok']}" + Style.RESET_ALL)
            
            update_harga = validasi_konfirmasi_yn("\nApakah ingin mengubah harga juga? (y/n): ")
            if update_harga:
                harga_baru = validasi_input_angka_positif(
                    f"💰 Harga baru (Maks Rp {BATAS_HARGA:,}): ", 
                    allow_zero=False,
                    max_value=BATAS_HARGA
                )
                harga_lama = obat_existing['harga']
                obat_existing['harga'] = harga_baru
                print(Fore.GREEN + f"✅ Harga diubah dari Rp {harga_lama:,} → Rp {harga_baru:,}" + Style.RESET_ALL)
        else:
            print(Fore.YELLOW + "ℹ️  Penambahan stok dibatalkan." + Style.RESET_ALL)
        
        return
    
    stok = validasi_input_angka_positif(
        f"📦 Stok (Maks {BATAS_STOK:,}): ", 
        allow_zero=True,
        max_value=BATAS_STOK
    )
    harga = validasi_input_angka_positif(
        f"💰 Harga (Maks Rp {BATAS_HARGA:,}): ", 
        allow_zero=False,
        max_value=BATAS_HARGA
    )
    
    d.obat_data[d.next_kode_obat] = {"nama": nama, "stok": stok, "harga": harga}
    print(Fore.GREEN + f"✅ Obat '{nama}' berhasil ditambahkan dengan kode {d.next_kode_obat}." + Style.RESET_ALL)
    d.next_kode_obat += 1

def prosedur_perbarui_obat():
    prosedur_tampilkan_obat_admin()

    kodeObat = validasi_input_angka_positif("\n🔍 Masukkan kode obat yang akan diubah: ", allow_zero=False)
            
    if kodeObat in d.obat_data:
        print(Fore.CYAN + f"📋 Obat yang dipilih: {d.obat_data[kodeObat]['nama']}" + Style.RESET_ALL)
        print(Fore.YELLOW + f"\nℹ️  Batas Maksimal:" + Style.RESET_ALL)
        print(Fore.CYAN + f"   • Stok maksimal: {BATAS_STOK:,}" + Style.RESET_ALL)
        print(Fore.CYAN + f"   • Harga maksimal: Rp {BATAS_HARGA:,}" + Style.RESET_ALL)
        print()

        stok_baru = validasi_input_angka_positif(
            f"📦 Stok Baru (Maks {BATAS_STOK:,}, kosongkan jika tidak diubah): ", 
            allow_zero=True, 
            allow_empty=True,
            max_value=BATAS_STOK
        )
        
        harga_baru = validasi_input_angka_positif(
            f"💰 Harga Baru (Maks Rp {BATAS_HARGA:,}, kosongkan jika tidak diubah): ", 
            allow_zero=False, 
            allow_empty=True,
            max_value=BATAS_HARGA
        )

        updated = False
        
        if stok_baru is not None:
            d.obat_data[kodeObat]['stok'] = stok_baru
            updated = True

        if harga_baru is not None:
            d.obat_data[kodeObat]['harga'] = harga_baru
            updated = True
                
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
            
        else:
            print(Fore.YELLOW + "ℹ️  Tidak ada perubahan dilakukan." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Kode obat {kodeObat} tidak ditemukan." + Style.RESET_ALL)

def prosedur_hapus_obat():
    prosedur_tampilkan_obat_admin()
    kodeObat = validasi_input_angka_positif("\n🗑️  Masukkan kode obat yang akan dihapus: ", allow_zero=False)
    
    if kodeObat in d.obat_data:
        nama_obat_hapus = d.obat_data[kodeObat]['nama']
        del d.obat_data[kodeObat]
        print(Fore.GREEN + f"✅ Obat '{nama_obat_hapus}' (Kode {kodeObat}) berhasil dihapus." + Style.RESET_ALL)
    else:
        print(Fore.RED + f"❌ Kesalahan: Kode obat {kodeObat} tidak ditemukan." + Style.RESET_ALL)