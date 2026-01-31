from flask import Flask, render_template, session, redirect, url_for, request, jsonify
from models import db, Product, Category
from app import app
from werkzeug.utils import secure_filename
import os

app.config['UPLOAD_FOLDER'] = 'static/products'

@app.context_processor
def inject_categories():
    categories = Category.query.all()
    return dict(nav_categories=categories)


# ADMIN SIDE
@app.route('/admin')
def admin_dashboard():
    return render_template('admin/dashboard.html')

# --- Categories CRUD ---
@app.route('/admin/categories')
def list_categories():
    # Fetch all categories that have no parent (parent_id is NULL)
    top_level_categories = Category.query.filter_by(parent_id=None).all()
    
    # Pass them to the template
    return render_template('admin/categories.html', top_level_categories=top_level_categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
def add_category():
    categories = Category.query.all()  # get all categories for parent dropdown

    if request.method == 'POST':
        name = request.form.get('name')
        parent_id = request.form.get('parent_id')  # can be None or empty string

        if name:
            new_cat = Category(name=name)

            # Only set parent_id if provided and valid
            if parent_id:
                new_cat.parent_id = int(parent_id)

            db.session.add(new_cat)
            db.session.commit()
            return redirect(url_for('list_categories'))

    return render_template('admin/add_category.html', categories=categories)


@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
def edit_category(id):
    category = Category.query.get_or_404(id)
    categories = Category.query.filter(Category.id != id).all()  # exclude self from parent list

    if request.method == 'POST':
        name = request.form.get('name')
        parent_id = request.form.get('parent_id')

        if name:
            category.name = name
            if parent_id:
                category.parent_id = int(parent_id)
            else:
                category.parent_id = None  # allow clearing parent
            db.session.commit()
            return redirect(url_for('list_categories'))

    return render_template('admin/edit_category.html', category=category, categories=categories)


@app.route('/admin/categories/delete/<int:id>', methods=['POST'])
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for('list_categories'))

# --- Products CRUD ---
@app.route('/admin/products')
def list_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        category_id = request.form.get('category_id')

        # Handle image upload
        image_file = request.files.get('image')
        image_filename = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            image_filename = filename

        if title and description and price and category_id:
            new_product = Product(
                title=title,
                description=description,
                price=float(price),
                image=image_filename,
                category_id=int(category_id)
            )
            db.session.add(new_product)
            db.session.commit()
            return redirect(url_for('list_products'))
    return render_template('admin/add_product.html', categories=categories)

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    categories = Category.query.all()
    if request.method == 'POST':
        product.title = request.form.get('title')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.category_id = int(request.form.get('category_id'))

        # Handle optional image update
        image_file = request.files.get('image')
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image_file.save(image_path)
            product.image = filename

        db.session.commit()
        return redirect(url_for('list_products'))
    return render_template('admin/edit_product.html', product=product, categories=categories)

@app.route('/admin/products/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for('list_products'))

if __name__ == '__main__':
    app.run(debug=True)
