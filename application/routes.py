from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Users, Stock, Product
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddProduct, AddStock



#This is the login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('add_product'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('add_product'))
    return render_template('login.html', title='Login', form=form)


#This is the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('add_product'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hash_pw = bcrypt.generate_password_hash(form.password.data)

        user = Users(
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            email=form.email.data,
            password=hash_pw
        )

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('add_product'))
    return render_template('register.html', title='Register', form=form)

#This is the logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


#Adding Product
@app.route("/addProduct", methods=['GET', 'POST'])
def add_product():
    form = AddProduct()
    if form.validate_on_submit():
        product_to_add = Product(
            product_name = form.product_name.data,
            product_category = form.product_category.data,
            price = form.price.data,
            size = form.size.data
        )
        db.session.add(product_to_add)
        db.session.commit()
    return render_template('add_product.html', title='Add Product', form=form)

#Adding Stock
@app.route("/addStock", methods=['GET', 'POST'])
def add_stock():
    form = AddStock()
    if form.validate_on_submit():
        stock_to_add = Stock(
            product_id = Product.query.filter.by(product_name=form.product_name.data).first(),
            quantity = form.quantity.data
        )
        db.session.add(stock_to_add)
        db.session.commit()
    return render_template('add_stock.html', title='Add Stock', form=form)

