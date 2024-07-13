import csv
import os
from datetime import datetime, timedelta

# Nama file CSV untuk pengguna dan transaksi
FILE_PENGGUNA = 'pengguna.csv'
FILE_TRANSAKSI = 'transaksi.csv'

# Fungsi untuk memuat data pengguna dari file CSV
def muat_pengguna():
    if not os.path.exists(FILE_PENGGUNA):
        return []
    with open(FILE_PENGGUNA, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [dict(user) for user in reader]

# Fungsi untuk menyimpan data pengguna ke file CSV
def simpan_pengguna(pengguna):
    with open(FILE_PENGGUNA, mode='w', newline='') as file:
        namafile = ['id', 'nama', 'email', 'kata_sandi', 'saldo']
        writer = csv.DictWriter(file, fieldnames=namafile)
        writer.writeheader()
        writer.writerows(pengguna)

# Fungsi untuk memuat data transaksi dari file CSV
def muat_transaksi():
    if not os.path.exists(FILE_TRANSAKSI):
        return []
    with open(FILE_TRANSAKSI, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [dict(trx) for trx in reader]

# Fungsi untuk menyimpan data transaksi ke file CSV
def simpan_transaksi(transaksi):
    with open(FILE_TRANSAKSI, mode='w', newline='') as file:
        namafile = ['id', 'id_pengguna', 'tipe', 'jumlah', 'tanggal', 'kategori']
        writer = csv.DictWriter(file, fieldnames=namafile)
        writer.writeheader()
        writer.writerows(transaksi)

# Fungsi untuk mendaftarkan pengguna baru
def daftar_pengguna(pengguna, nama, email, kata_sandi):
    id_pengguna = len(pengguna) + 1
    pengguna.append({'id': id_pengguna, 'nama': nama, 'email': email, 'kata_sandi': kata_sandi, 'saldo': '0'})
    simpan_pengguna(pengguna)
    print(f"Pengguna {nama} berhasil terdaftar.")

# Fungsi untuk login pengguna
def login_pengguna(pengguna, email, kata_sandi):
    for user in pengguna:
        if user['email'] == email and user['kata_sandi'] == kata_sandi:
            print("\n============================================================")
            print(f"Login berhasil. Selamat datang, {user['nama']}!")
            print("============================================================")
            return user
    print("\n============================================================")
    print("Email atau kata sandi salah.")
    print("============================================================")
    return None

# Fungsi untuk logout pengguna (belum diimplementasikan)
def logout_pengguna():
    return None

# Fungsi untuk menghapus riwayat transaksi
def hapus_riwayat_transaksi(transaksi):
    print("===============================================================================================")
    print("Riwayat Transaksi:")
    for trx in transaksi:
        print(f"ID: {trx['id']}, Tipe: {trx['tipe']}, Jumlah: {format_rupiah(float(trx['jumlah']))}, Tanggal: {trx['tanggal']}")

    while True:
        print("===============================================================================================")
        pilihan = input("Masukkan ID transaksi yang ingin dihapus (atau ketik 'batal' untuk membatalkan): ").strip().lower()
        if pilihan == 'batal':
            print("Penghapusan riwayat transaksi dibatalkan.")
            print("===============================================================================================")
            return
        if pilihan.isdigit():
            pilihan_id = int(pilihan)
            for trx in transaksi:
                if trx['id'] == pilihan_id:
                    transaksi.remove(trx)
                    simpan_transaksi(transaksi)
                    print("\n==================================================")
                    print(f"Transaksi dengan ID {pilihan_id} berhasil dihapus dari file CSV.")
                    print("==================================================")
                    return
            print(f"Tidak ada transaksi dengan ID {pilihan_id}. Silakan coba lagi.")
        else:
            print("ID transaksi harus berupa angka. Silakan coba lagi.")

# Fungsi untuk format rupiah
def format_rupiah(amount):
    return f"Rp {int(amount):,}".replace(",", ".")

# Fungsi untuk mengecek saldo pengguna
def cek_saldo(user):
    print("\n==================================================")
    print(f"Saldo Anda saat ini adalah: {format_rupiah(float(user['saldo']))}")
    print("==================================================")

# Fungsi untuk top up saldo pengguna
def topup_saldo(pengguna, transaksi, user, jumlah):
    for usr in pengguna:
        if usr['id'] == user['id']:
            usr['saldo'] = str(float(usr['saldo']) + jumlah)
            transaksi.append({
                'id': len(transaksi) + 1,
                'id_pengguna': usr['id'],
                'tipe': 'topup',
                'jumlah': jumlah,
                'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'kategori': ''
            })
            simpan_pengguna(pengguna)
            simpan_transaksi(transaksi)
            print("\n==================================================")
            print(f"Top up sebesar {format_rupiah(jumlah)} berhasil.")
            print("==================================================")
            return

# Fungsi untuk transfer saldo ke pengguna lain
def transfer_saldo(pengguna, transaksi, user, email_penerima, jumlah, kategori):
    penerima = None
    for usr in pengguna:
        if usr['email'] == email_penerima:
            penerima = usr
            break

    if penerima is None:
        print("\n==================================================")
        print("Penerima tidak ditemukan.")
        print("==================================================")
        return

    if penerima['id'] == user['id']:
        print("\n==================================================")
        print("Tidak bisa mentransfer ke akun sendiri.")
        print("==================================================")
        return

    if float(user['saldo']) < jumlah:
        print("\n==================================================")
        print("Saldo tidak mencukupi.")
        print("==================================================")
        return

    for usr in pengguna:
        if usr['id'] == user['id']:
            usr['saldo'] = str(float(usr['saldo']) - jumlah)
        if usr['id'] == penerima['id']:
            usr['saldo'] = str(float(usr['saldo']) + jumlah)

    transaksi.append({
        'id': len(transaksi) + 1,
        'id_pengguna': user['id'],
        'tipe': 'transfer',
        'jumlah': jumlah,
        'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'kategori': kategori
    })
    simpan_pengguna(pengguna)
    simpan_transaksi(transaksi)
    print("\n==================================================")
    print(f"Transfer sebesar {format_rupiah(jumlah)} ke {penerima['nama']} berhasil.")
    print("==================================================")

# Fungsi untuk melakukan penarikan saldo
def tarik_saldo(pengguna, transaksi, user, jumlah, kategori):
    if float(user['saldo']) < jumlah:
        print("\n==================================================")
        print("Saldo tidak mencukupi untuk melakukan penarikan.")
        print("==================================================")
        return

    for usr in pengguna:
        if usr['id'] == user['id']:
            usr['saldo'] = str(float(usr['saldo']) - jumlah)

    transaksi.append({
        'id': len(transaksi) + 1,
        'id_pengguna': user['id'],
        'tipe': 'tarik',
        'jumlah': jumlah,
        'tanggal': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'kategori': kategori  # Menyimpan kategori dalam transaksi
    })

    simpan_pengguna(pengguna)
    simpan_transaksi(transaksi)
    print("\n==================================================")
    print(f"Penarikan saldo sebesar {format_rupiah(jumlah)} dengan kategori '{kategori}' berhasil.")
    print("==================================================")
    
# Fungsi untuk menampilkan laporan kategori pengeluaran berdasarkan tanggal mulai dan tanggal selesai
def laporan_kategori(transaksi, user, tanggal_mulai, tanggal_selesai):
    kategori_map = {}
    for i in transaksi:
        tanggal_transaksi = datetime.strptime(i['tanggal'], '%Y-%m-%d %H:%M:%S')
        if i['tipe'] == 'transfer' and tanggal_mulai <= tanggal_transaksi <= tanggal_selesai and i['id_pengguna'] == user['id']:
            kategori = i['kategori']
            jumlah = float(i['jumlah'])
            if kategori in kategori_map:
                kategori_map[kategori] += jumlah
            else:
                kategori_map[kategori] = jumlah
        elif i['tipe'] == 'tarik' and tanggal_mulai <= tanggal_transaksi <= tanggal_selesai and i['id_pengguna'] == user['id']:
            kategori = i['kategori']
            jumlah = float(i['jumlah'])
            if kategori in kategori_map:
                kategori_map[kategori] += jumlah
            else:
                kategori_map[kategori] = jumlah
    return kategori_map

# Fungsi untuk menampilkan laporan bulanan
def laporan_bulanan(transaksi, user):
    hari_ini = datetime.now()
    tanggal_mulai = hari_ini.replace(day=1)
    tanggal_selesai = (tanggal_mulai + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    uang_masuk = laporan_uang(transaksi, user, 'topup', tanggal_mulai, tanggal_selesai)
    uang_keluar = laporan_uang(transaksi, user, 'transfer', tanggal_mulai, tanggal_selesai)
    uang_tarik = laporan_uang(transaksi, user, 'tarik', tanggal_mulai, tanggal_selesai)
    kategori_map = laporan_kategori(transaksi, user, tanggal_mulai, tanggal_selesai)
    print("\n==================================================")
    print(f"Laporan Bulanan ({tanggal_mulai.date()} - {tanggal_selesai.date()}):")
    print(f"Total uang masuk: {format_rupiah(uang_masuk)}")
    print(f"Total uang keluar (transfer): {format_rupiah(uang_keluar)}")
    print(f"Total uang keluar (tarik saldo): {format_rupiah(uang_tarik)}")
    print("Pengeluaran per kategori:")
    for kategori, jumlah in kategori_map.items():
        print(f"{kategori}: {format_rupiah(jumlah)}")
    print("==================================================")

# Fungsi untuk menampilkan laporan tahunan
def laporan_tahunan(transaksi, user):
    hari_ini = datetime.now()
    tanggal_mulai = hari_ini.replace(month=1, day=1)
    tanggal_selesai = hari_ini.replace(month=12, day=31)
    uang_masuk = laporan_uang(transaksi, user, 'topup', tanggal_mulai, tanggal_selesai)
    uang_keluar = laporan_uang(transaksi, user, 'transfer', tanggal_mulai, tanggal_selesai)
    uang_tarik = laporan_uang(transaksi, user, 'tarik', tanggal_mulai, tanggal_selesai)
    kategori_map = laporan_kategori(transaksi, user, tanggal_mulai, tanggal_selesai)
    print("\n==================================================")
    print(f"Laporan Tahunan ({tanggal_mulai.date()} - {tanggal_selesai.date()}):")
    print(f"Total uang masuk: {format_rupiah(uang_masuk)}")
    print(f"Total uang keluar (transfer): {format_rupiah(uang_keluar)}")
    print(f"Total uang keluar (tarik saldo): {format_rupiah(uang_tarik)}")
    print("Pengeluaran per kategori:")
    for kategori, jumlah in kategori_map.items():
        print(f"{kategori}: {format_rupiah(jumlah)}")
    print("==================================================")

# Fungsi untuk menampilkan laporan keuangan berdasarkan tipe transaksi, tanggal mulai, dan tanggal selesai
def laporan_uang(transaksi, user, tipe, tanggal_mulai, tanggal_selesai):
    total = 0
    for i in transaksi:
        tanggal_transaksi = datetime.strptime(i['tanggal'], '%Y-%m-%d %H:%M:%S')
        if i['tipe'] == tipe and tanggal_mulai <= tanggal_transaksi <= tanggal_selesai and i['id_pengguna'] == user['id']:
            total += float(i['jumlah'])
    return total


# Fungsi utama untuk menjalankan program manajemen keuangan
def main():
    pengguna = muat_pengguna()
    transaksi = muat_transaksi()
    user = None

    while True:
        print("\nSistem Manajemen Keuangan Pribadi DompetQu")
        if user is None:
            print("1. Daftar")
            print("2. Login")
            print("3. Keluar")
            pilihan = input("Masukkan pilihan Anda: ").strip()
            if pilihan == '1':
                nama = input("Masukkan nama: ").strip()
                email = input("Masukkan email: ").strip()
                kata_sandi = input("Masukkan kata sandi: ").strip()
                daftar_pengguna(pengguna, nama, email, kata_sandi)
            elif pilihan == '2':
                email = input("Masukkan email: ").strip()
                kata_sandi = input("Masukkan kata sandi: ").strip()
                user = login_pengguna(pengguna, email, kata_sandi)
            elif pilihan == '3':
                print("Terima kasih telah menggunakan layanan kami.")
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")
        else:
            print(f"\nSelamat datang, {user['nama']}")
            print("1. Cek Saldo")
            print("2. Top Up Saldo")
            print("3. Transfer Saldo")
            print("4. Tarik Saldo")
            print("5. Laporan Bulanan")
            print("6. Laporan Tahunan")
            print("7. Hapus Riwayat Transaksi")
            print("8. Logout")
            pilihan = input("Masukkan pilihan Anda: ").strip()
            if pilihan == '1':
                cek_saldo(user)
            elif pilihan == '2':
                jumlah = float(input("Masukkan jumlah dana yang ingin disetor: ").strip())
                topup_saldo(pengguna, transaksi, user, jumlah)
            elif pilihan == '3':
                email_penerima = input("Masukkan email penerima: ").strip()
                jumlah = float(input("Masukkan jumlah saldo yang ingin ditransfer: ").strip())
                kategori = input("Masukkan kategori transfer: ").strip()
                transfer_saldo(pengguna, transaksi, user, email_penerima, jumlah, kategori)
            elif pilihan == '4':
                jumlah = float(input("Masukkan jumlah saldo yang ingin ditarik: ").strip())
                kategori = input("Masukkan kategori penarikan: ").strip()
                tarik_saldo(pengguna, transaksi, user, jumlah, kategori)
            elif pilihan == '5':
                laporan_bulanan(transaksi, user)
            elif pilihan == '6':
                laporan_tahunan(transaksi, user)
            elif pilihan == '7':
                hapus_riwayat_transaksi(transaksi)
            elif pilihan == '8':
                user = logout_pengguna()
                print("Logout berhasil.")
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == '__main__':
    main()
