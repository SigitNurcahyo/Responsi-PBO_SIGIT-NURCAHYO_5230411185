-- Membuat database
CREATE DATABASE IF NOT EXISTS retail_db;

-- Gunakan database yang baru dibuat
USE retail_db;

-- Membuat tabel produk
CREATE TABLE IF NOT EXISTS produk (
    id_produk INT AUTO_INCREMENT PRIMARY KEY,
    nama_produk VARCHAR(100) NOT NULL,
    harga_produk DECIMAL(65, 10) NOT NULL
);

-- Membuat tabel transaksi
CREATE TABLE IF NOT EXISTS transaksi (
    id_transaksi INT AUTO_INCREMENT PRIMARY KEY,
    id_produk INT NOT NULL,
    jumlah_produk INT NOT NULL,
    total_harga DECIMAL(65, 10) NOT NULL,
    tanggal_transaksi DATE NOT NULL,
    FOREIGN KEY (id_produk) REFERENCES produk(id_produk)
);
