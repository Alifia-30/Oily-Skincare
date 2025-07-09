from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from app import db
from app.models import Produk, Penilaian, Pembobotan, Pengguna
from sqlalchemy import text
from datetime import datetime

bp = Blueprint('main', __name__)

def get_saw_calculation(weights):
    """Executes the SAW calculation using a raw SQL query."""
    sql = text("""
        WITH ProductEvaluations AS (
            SELECT
                p.ID_PRODUK,
                p.NAMA_PRODUK,
                p.HARGA AS C1,
                pe.BAHAN_AKTIF AS C2,
                pe.REVIEW AS C3,
                p.STOK AS C4,
                pe.EFEK_SAMPING AS C5
            FROM produk p
            JOIN penilaian pe ON p.ID_PRODUK = pe.ID_PRODUK
        ),
        MinMax AS (
            SELECT
                MIN(C1) as min_c1,
                MAX(C2) as max_c2,
                MAX(C3) as max_c3,
                MAX(C4) as max_c4,
                MAX(C5) as max_c5
            FROM ProductEvaluations
        ),
        NormalizedMatrix AS (
            SELECT
                pe.ID_PRODUK,
                pe.NAMA_PRODUK,
                (SELECT min_c1 FROM MinMax) * 1.0 / pe.C1 AS r1,
                pe.C2 * 1.0 / (SELECT max_c2 FROM MinMax) AS r2,
                pe.C3 * 1.0 / (SELECT max_c3 FROM MinMax) AS r3,
                pe.C4 * 1.0 / (SELECT max_c4 FROM MinMax) AS r4,
                pe.C5 * 1.0 / (SELECT max_c5 FROM MinMax) AS r5
            FROM ProductEvaluations pe
        )
        SELECT
            NAMA_PRODUK,
            (r1 * :w1 + r2 * :w2 + r3 * :w3 + r4 * :w4 + r5 * :w5) AS score
        FROM NormalizedMatrix
        ORDER BY score DESC;
    """)
    
    with db.engine.connect() as connection:
        result = connection.execute(sql, weights)
        return result.fetchall()

@bp.route('/', methods=['GET', 'POST'])
def index():
    # Get only active products for calculation
    products = db.session.query(
        Produk, Penilaian
    ).join(
        Penilaian
    ).filter(
        Produk.STATUS == 'active'
    ).all()

    if request.method == 'POST':
        weights = {
            'w1': float(request.form['w1']),
            'w2': float(request.form['w2']),
            'w3': float(request.form['w3']),
            'w4': float(request.form['w4']),
            'w5': float(request.form['w5'])
        }
        
        # Calculate rankings only for active products
        sql = text("""
            WITH normalized_matrix AS (
                SELECT 
                    p.ID_PRODUK,
                    p.NAMA_PRODUK,
                    -- Normalize cost criteria (price)
                    (SELECT MIN(HARGA) FROM produk WHERE STATUS = 'active') / p.HARGA as norm_c1,
                    -- Normalize benefit criteria
                    e.BAHAN_AKTIF / (SELECT MAX(BAHAN_AKTIF) FROM penilaian) as norm_c2,
                    e.REVIEW / (SELECT MAX(REVIEW) FROM penilaian) as norm_c3,
                    p.STOK / (SELECT MAX(STOK) FROM produk WHERE STATUS = 'active') as norm_c4,
                    e.EFEK_SAMPING / (SELECT MAX(EFEK_SAMPING) FROM penilaian) as norm_c5
                FROM produk p
                JOIN penilaian e ON p.ID_PRODUK = e.ID_PRODUK
                WHERE p.STATUS = 'active'
            )
            SELECT 
                NAMA_PRODUK,
                (norm_c1 * :w1 + 
                 norm_c2 * :w2 + 
                 norm_c3 * :w3 + 
                 norm_c4 * :w4 + 
                 norm_c5 * :w5) as score
            FROM normalized_matrix
            ORDER BY score DESC;
        """)
        
        results = db.session.execute(sql, weights)
        results = [{'nama_produk': row[0], 'score': row[1]} for row in results]
        
        return render_template('index.html', 
                             products=products,
                             results=results,
                             user_weights=weights)
    
    preset_weights = Pembobotan.query.filter_by(IS_PRESET=True).first()
    return render_template('index.html', products=products, preset_weights=preset_weights)

@bp.route('/products/list', methods=['GET'])
def list_products():
    products = db.session.query(Produk, Penilaian).outerjoin(Penilaian).all()
    return render_template('user_products.html', products=products)

@bp.route('/products/manage', methods=['GET'])
def manage_products():
    products = db.session.query(Produk, Penilaian).outerjoin(Penilaian).all()
    return render_template('manage_products.html', products=products)

@bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        try:
            # Add new product
            new_product = Produk(
                NAMA_PRODUK=request.form['nama_produk'],
                HARGA=int(request.form['harga']),
                STOK=int(request.form['stok']),
                STATUS=request.form['status']
            )
            db.session.add(new_product)
            db.session.flush()  # Get the ID of new product

            # Add product evaluation
            new_evaluation = Penilaian(
                BAHAN_AKTIF=int(request.form['bahan_aktif']),
                REVIEW=int(request.form['review']),
                EFEK_SAMPING=int(request.form['efek_samping']),
                ID_PRODUK=new_product.ID_PRODUK,
                ID_PENGGUNA=1  # Default admin user
            )
            db.session.add(new_evaluation)
            db.session.commit()
            flash('Produk berhasil ditambahkan!', 'success')
            return redirect(url_for('main.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
            return redirect(url_for('main.add_product'))

    return render_template('add_product.html')

@bp.route('/products/<int:id>/toggle', methods=['POST'])
def toggle_product_status(id):
    product = Produk.query.get_or_404(id)
    product.STATUS = 'inactive' if product.STATUS == 'active' else 'active'
    db.session.commit()
    return jsonify({'status': 'success', 'new_status': product.STATUS})

@bp.route('/products/<int:id>/edit', methods=['GET', 'POST'])
def edit_product(id):
    product = db.session.query(Produk, Penilaian).join(Penilaian).filter(Produk.ID_PRODUK == id).first_or_404()
    
    if request.method == 'POST':
        try:
            # Update product
            product.Produk.NAMA_PRODUK = request.form['nama_produk']
            product.Produk.HARGA = int(request.form['harga'])
            product.Produk.STOK = int(request.form['stok'])
            product.Produk.STATUS = request.form['status']

            # Update evaluation
            product.Penilaian.BAHAN_AKTIF = int(request.form['bahan_aktif'])
            product.Penilaian.REVIEW = int(request.form['review'])
            product.Penilaian.EFEK_SAMPING = int(request.form['efek_samping'])
            
            db.session.commit()
            flash('Produk berhasil diupdate!', 'success')
            return redirect(url_for('main.manage_products'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('edit_product.html', product=product)

@bp.route('/products/<int:id>/delete', methods=['DELETE'])
def delete_product(id):
    try:
        # First delete the evaluation
        evaluation = Penilaian.query.filter_by(ID_PRODUK=id).first()
        if evaluation:
            db.session.delete(evaluation)
            
        # Then delete the product
        product = Produk.query.get_or_404(id)
        db.session.delete(product)
        
        db.session.commit()
        return jsonify({'status': 'success'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': str(e)}), 500

@bp.route('/get_preset_weights')
def get_preset_weights_json():
    preset = Pembobotan.query.filter_by(IS_PRESET=True).first()
    if preset:
        return jsonify({
            'w1': preset.W1,
            'w2': preset.W2,
            'w3': preset.W3,
            'w4': preset.W4,
            'w5': preset.W5
        })
    return jsonify({}) 