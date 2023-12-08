from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
db = SQLAlchemy(app)

# Model dla produktu
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String, nullable=True)  # Nowa kolumna dla obrazu


# Strona główna z listą produktów
@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

# Strona ze szczegółami produktu
@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get_or_404(product_id)
    # Przykładowy numer konta bankowego
    account_details = {
        'account_number': '23-14-70 55337078',
        'bank_name': 'WISE',
        'recipient_name': 'Bristol Deliveries'
    }
    return render_template('product_details.html', product=product, account_details=account_details)

# Kontekst aplikacji dla utworzenia tabel
with app.app_context():
    db.create_all()

# Uruchomienie aplikacji
if __name__ == '__main__':
    app.run(debug=True)




