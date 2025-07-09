from app import db
from datetime import datetime

class Pengguna(db.Model):
    __tablename__ = 'pengguna'
    ID_PENGGUNA = db.Column(db.Integer, primary_key=True)
    NAMA = db.Column(db.String(100), nullable=False)
    NO_KONTAK = db.Column(db.String(20))
    pembobotan = db.relationship('Pembobotan', backref='pengguna', lazy=True)
    penilaian = db.relationship('Penilaian', backref='pengguna', lazy=True)

class Produk(db.Model):
    __tablename__ = 'produk'
    ID_PRODUK = db.Column(db.Integer, primary_key=True)
    NAMA_PRODUK = db.Column(db.String(150), nullable=False, unique=True)
    HARGA = db.Column(db.Integer, nullable=False)
    STOK = db.Column(db.Integer, nullable=False)
    STATUS = db.Column(db.Enum('active', 'inactive'), nullable=False, default='active')
    CREATED_AT = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    UPDATED_AT = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    penilaian = db.relationship('Penilaian', backref='produk', lazy=True, uselist=False)

    def to_dict(self):
        return {
            'ID_PRODUK': self.ID_PRODUK,
            'NAMA_PRODUK': self.NAMA_PRODUK,
            'HARGA': self.HARGA,
            'STOK': self.STOK,
            'STATUS': self.STATUS,
            'CREATED_AT': self.CREATED_AT.strftime('%Y-%m-%d %H:%M:%S'),
            'UPDATED_AT': self.UPDATED_AT.strftime('%Y-%m-%d %H:%M:%S')
        }

class Penilaian(db.Model):
    __tablename__ = 'penilaian'
    ID_PENILAIAN = db.Column(db.Integer, primary_key=True)
    TANGGAL = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Storing criteria as numeric values (e.g., 1-5 scale)
    BAHAN_AKTIF = db.Column(db.Integer, nullable=False)
    REVIEW = db.Column(db.Integer, nullable=False)
    EFEK_SAMPING = db.Column(db.Integer, nullable=False)
    ID_PRODUK = db.Column(db.Integer, db.ForeignKey('produk.ID_PRODUK', ondelete='CASCADE'), nullable=False, unique=True)
    ID_PENGGUNA = db.Column(db.Integer, db.ForeignKey('pengguna.ID_PENGGUNA', ondelete='SET NULL'))

    def to_dict(self):
        return {
            'ID_PENILAIAN': self.ID_PENILAIAN,
            'BAHAN_AKTIF': self.BAHAN_AKTIF,
            'REVIEW': self.REVIEW,
            'EFEK_SAMPING': self.EFEK_SAMPING,
            'ID_PRODUK': self.ID_PRODUK,
            'TANGGAL': self.TANGGAL.strftime('%Y-%m-%d %H:%M:%S')
        }

class Pembobotan(db.Model):
    __tablename__ = 'pembobotan'
    ID_PEMBOBOTAN = db.Column(db.Integer, primary_key=True)
    TANGGAL = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    # Weights for criteria: Harga, Bahan Aktif, Review, Stok, Efek Samping
    W1 = db.Column(db.Float, nullable=False) # Harga
    W2 = db.Column(db.Float, nullable=False) # Bahan Aktif
    W3 = db.Column(db.Float, nullable=False) # Review
    W4 = db.Column(db.Float, nullable=False) # Stok
    W5 = db.Column(db.Float, nullable=False) # Efek Samping
    ID_PENGGUNA = db.Column(db.Integer, db.ForeignKey('pengguna.ID_PENGGUNA', ondelete='SET NULL'))
    IS_PRESET = db.Column(db.Boolean, default=False, nullable=False) 