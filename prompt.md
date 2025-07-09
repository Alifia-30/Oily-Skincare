buatkan aplikasi dengan ketentuan di bawah ini menggunakan flask dengan ui yang simple.
saya mau buat aplikasi pemilihan skincare untuk kulit berminyak.

dengan kriteria:
Harga (diambil dari database)
bahan aktif
review pengguna
stok (diambil dari database)
efek samping

dan contoh alternatif prouduknya
A1 COSRX Low pH Good Morning Cleanser
A2 The Ordinary Niacinamide 10% + Zinc 1%
A3 Wardah Acnederm Series
A4 Some By Mi AHA BHA PHA Miracle Toner
A5 Emina Ms. Pimple Series
A6 Skintific Mugwort Anti Pores & Acne Clay Mask

dengan flow aplikasi seperti ini:
user masuk ke halaman web. setelah masuk web itu user bisa melihat
alternatif produk skincare yang sudah ada harga dan stoknya,
kemudian masukkan bobot untuk tiap kriteria (total = 1) atau gunakan preset yang ada (ambil dari database)
setelah itu hitung rangking produk skincare. Proses Perhitungan SAW di database.
user juga bisa menambahkan alternatif produk yang tersedia di list/dropdown yang dibuat admin

1.  pengguna (users):

    - ID_PENGGUNA (User ID, primary key)
    - NAMA (User Name)
    - NO_KONTAK (Contact Number)

2.  produk (products):

    - ID_PRODUK (Product ID, primary key)
    - NAMA_PRODUK (Product Name)
    - HARGA (Price)
    - STOK (Stock)

3.  penilaian (evaluation):

    - ID_PENILAIAN (Evaluation ID, primary key)
    - TANGGAL (Date)
    - BAHAN_AKTIF (Active Ingredients)
    - REVIEW (Review)
    - EFEK_SAMPING (Side Effects)
    - ID_PRODUK (Product ID, foreign key referencing produk)
    - ID_PENGGUNA (User ID, foreign key referencing pengguna)

4.  pembobotan (weighting):
    - ID_PEMBOBOTAN (Weighting ID, primary key)
    - TANGGAL (Date)
    - W1 (Weight 1)
    - W2 (Weight 2)
    - W3 (Weight 3)
    - W4 (Weight 4)
    - W5 (Weight 5)
    - ID_PENGGUNA (User ID, foreign key referencing pengguna)
