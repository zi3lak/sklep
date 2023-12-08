from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=True)
    is_sold = db.Column(db.Boolean, default=False)

# Strona do dodawania produktów
@app.route('/admin/add-product', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        image = request.form.get('image')
        new_product = Product(name=name, price=price, image=image)
        db.session.add(new_product)
        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template('add_product.html')

# Strona z listą produktów w back office
@app.route('/admin/products')
def list_products():
    products = Product.query.all()
    return render_template('list_products.html', products=products)

# Strona do edycji produktu
@app.route('/admin/edit-product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.price = request.form.get('price')
        product.image = request.form.get('image')
        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template('edit_product.html', product=product)

# Strona do usuwania produktu
@app.route('/admin/delete-product/<int:product_id>', methods=['POST'])
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('list_products'))

@app.route('/')
def home():
    return render_template('home.html')


# Kontekst aplikacji dla utworzenia tabel
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Uruchom na porcie 8080
