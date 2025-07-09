import random
from app import create_app, db
from app.models import Pengguna, Produk, Penilaian, Pembobotan

def seed_data():
    """Populates the database with initial data."""
    app = create_app()
    with app.app_context():
        # Clean up existing data
        db.session.query(Penilaian).delete()
        db.session.query(Pembobotan).delete()
        db.session.query(Produk).delete()
        db.session.query(Pengguna).delete()
        db.session.commit()

        # --- Create a default user ---
        default_user = Pengguna(NAMA='Admin User', NO_KONTAK='123456789')
        db.session.add(default_user)
        db.session.commit()

        # --- Create Products and Evaluations ---
        products_data = [
            {'nama': 'COSRX Low pH Good Morning Cleanser', 'harga': 85000, 'stok': 150},
            {'nama': 'The Ordinary Niacinamide 10% + Zinc 1%', 'harga': 150000, 'stok': 75},
            {'nama': 'Wardah Acnederm Series', 'harga': 75000, 'stok': 200},
            {'nama': 'Some By Mi AHA BHA PHA Miracle Toner', 'harga': 180000, 'stok': 100},
            {'nama': 'Emina Ms. Pimple Series', 'harga': 50000, 'stok': 250},
            {'nama': 'Skintific Mugwort Anti Pores & Acne Clay Mask', 'harga': 120000, 'stok': 90}
        ]

        for p_data in products_data:
            produk = Produk(
                NAMA_PRODUK=p_data['nama'],
                HARGA=p_data['harga'],
                STOK=p_data['stok']
            )
            db.session.add(produk)
            db.session.commit() # Commit to get the ID for the foreign key

            penilaian = Penilaian(
                ID_PRODUK=produk.ID_PRODUK,
                BAHAN_AKTIF=random.randint(3, 5), # Score 1-5
                REVIEW=random.randint(3, 5),      # Score 1-5
                EFEK_SAMPING=random.randint(3, 5), # Score 1-5, higher is better
                ID_PENGGUNA=default_user.ID_PENGGUNA
            )
            db.session.add(penilaian)

        # --- Create a Preset Weight ---
        preset_weight = Pembobotan(
            W1=0.30,  # Bobot untuk Harga
            W2=0.25,  # Bobot untuk Bahan Aktif
            W3=0.20,  # Bobot untuk Review
            W4=0.15,  # Bobot untuk Stok
            W5=0.10,  # Bobot untuk Efek Samping
            IS_PRESET=True,
            ID_PENGGUNA=default_user.ID_PENGGUNA
        )
        db.session.add(preset_weight)

        db.session.commit()
        print("Database has been seeded with initial data.")

if __name__ == '__main__':
    seed_data() 