from app import app, db
from models import Category, Product
import os

def seed_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Categories ---
        electronics = Category(name='Electronics')
        fashion = Category(name='Fashion')
        home = Category(name='Home & Kitchen')

        # Subcategories
        phones = Category(name='Phones', parent=electronics)
        laptops = Category(name='Laptops', parent=electronics)
        mens = Category(name='Men\'s Fashion', parent=fashion)
        womens = Category(name='Women\'s Fashion', parent=fashion)

        db.session.add_all([electronics, fashion, home, phones, laptops, mens, womens])
        db.session.commit()

        # Path helper for local images
        def img(filename):
            return f"{filename}"
        # relative to /static

        # --- Products ---
        products = [
            Product(
                title='iPhone 15 Pro',
                price=1299.99,
                description='Apple iPhone 15 Pro with A17 Bionic chip and 256GB storage.',
                image=img('cet.jpg'),
                category=phones
            ),
            Product(
                title='MacBook Air M3',
                price=1499.99,
                description='Apple MacBook Air with M3 chip, 13-inch Retina display, 512GB SSD.',
                image=img('cet.jpg'),
                category=laptops
            ),
            Product(
                title='Cotton T-Shirt',
                price=19.99,
                description='100% cotton t-shirt for men. Soft and comfortable.',
                image=img('cet.jpg'),
                category=mens
            ),
            Product(
                title='Women\'s Leather Handbag',
                price=89.99,
                description='Elegant leather handbag with gold accents.',
                image=img('cet.jpg'),
                category=womens
            ),
            Product(
                title='Electric Blender',
                price=59.99,
                description='High-speed electric blender perfect for smoothies and soups.',
                image=img('cet.jpg'),
                category=home
            ),
        ]

        db.session.add_all(products)
        db.session.commit()

        print('✅ Database seeded successfully!')

if __name__ == '__main__':
    seed_data()
