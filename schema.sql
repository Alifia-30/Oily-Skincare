-- Drop database if exists and create new one
DROP DATABASE IF EXISTS oily_skincare;
CREATE DATABASE oily_skincare;
USE oily_skincare;

-- Create pengguna table
CREATE TABLE IF NOT EXISTS pengguna (
    ID_PENGGUNA INT AUTO_INCREMENT PRIMARY KEY,
    NAMA VARCHAR(100) NOT NULL,
    NO_KONTAK VARCHAR(20)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create produk table
CREATE TABLE IF NOT EXISTS produk (
    ID_PRODUK INT AUTO_INCREMENT PRIMARY KEY,
    NAMA_PRODUK VARCHAR(150) NOT NULL UNIQUE,
    HARGA INT NOT NULL,
    STOK INT NOT NULL,
    STATUS ENUM('active', 'inactive') NOT NULL DEFAULT 'active',
    CREATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UPDATED_AT TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create penilaian table
CREATE TABLE IF NOT EXISTS penilaian (
    ID_PENILAIAN INT AUTO_INCREMENT PRIMARY KEY,
    TANGGAL DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    BAHAN_AKTIF INT NOT NULL,
    REVIEW INT NOT NULL,
    EFEK_SAMPING INT NOT NULL,
    ID_PRODUK INT NOT NULL UNIQUE,
    ID_PENGGUNA INT,
    FOREIGN KEY (ID_PRODUK) REFERENCES produk(ID_PRODUK) ON DELETE CASCADE,
    FOREIGN KEY (ID_PENGGUNA) REFERENCES pengguna(ID_PENGGUNA) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Create pembobotan table
CREATE TABLE IF NOT EXISTS pembobotan (
    ID_PEMBOBOTAN INT AUTO_INCREMENT PRIMARY KEY,
    TANGGAL DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    W1 FLOAT NOT NULL,
    W2 FLOAT NOT NULL,
    W3 FLOAT NOT NULL,
    W4 FLOAT NOT NULL,
    W5 FLOAT NOT NULL,
    ID_PENGGUNA INT,
    IS_PRESET BOOLEAN NOT NULL DEFAULT FALSE,
    FOREIGN KEY (ID_PENGGUNA) REFERENCES pengguna(ID_PENGGUNA) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Insert sample data for testing
INSERT INTO pengguna (NAMA, NO_KONTAK) VALUES ('Admin User', '123456789');

-- Insert products
INSERT INTO produk (NAMA_PRODUK, HARGA, STOK, STATUS) VALUES
('COSRX Low pH Good Morning Cleanser', 85000, 150, 'active'),
('The Ordinary Niacinamide 10% + Zinc 1%', 150000, 75, 'active'),
('Wardah Acnederm Series', 75000, 200, 'active'),
('Some By Mi AHA BHA PHA Miracle Toner', 180000, 100, 'active'),
('Emina Ms. Pimple Series', 50000, 250, 'active'),
('Skintific Mugwort Anti Pores & Acne Clay Mask', 120000, 90, 'active'),
("Paula's Choice 2% BHA Liquid Exfoliant", 429000, 30, 'active'),
('COSRX Low pH Good Morning Gel Cleanser', 120000, 45, 'active'),
('Cetaphil Gentle Skin Cleanser', 159000, 60, 'active'),
('SK-II Facial Treatment Essence', 1850000, 15, 'active');

-- Insert evaluations (using random scores between 3-5 for demonstration)
INSERT INTO penilaian (BAHAN_AKTIF, REVIEW, EFEK_SAMPING, ID_PRODUK, ID_PENGGUNA)
SELECT 
    FLOOR(3 + (RAND() * 3)), -- Random score between 3-5
    FLOOR(3 + (RAND() * 3)),
    FLOOR(3 + (RAND() * 3)),
    ID_PRODUK,
    1 -- Admin user ID
FROM produk;

-- Insert preset weights
INSERT INTO pembobotan (W1, W2, W3, W4, W5, ID_PENGGUNA, IS_PRESET)
VALUES (0.30, 0.25, 0.20, 0.15, 0.10, 1, TRUE); 