user_data = {
    "apoteker": {"password": "1234", "role": "apoteker", "member": False},
    "user": {"password": "2345", "role": "user", "member": False}
}

obat_data = {
    101: {"nama": "Paracetamol", "stok": 50, "harga": 5000},
    102: {"nama": "Amoxicillin", "stok": 30, "harga": 15000},
    103: {"nama": "Komix", "stok": 20, "harga": 10000},
    104: {"nama": "OBH", "stok": 15, "harga": 13000},
    105: {"nama": "Tremenza", "stok": 20, "harga": 20000},
    106: {"nama": "Omeprazol", "stok": 13, "harga": 15000},
    107: {"nama": "Promag", "stok": 25, "harga": 10000},
    108: {"nama": "Vitamin C Redoxon", "stok": 20, "harga": 40000},
    109: {"nama": "Betadine", "stok": 30, "harga": 10000},
    110: {"nama": "Combatrin", "stok": 25, "harga": 25000},
}

next_kode_obat = 111
pengguna = None
role_pengguna = None
run = True