from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Users, Stock, Product
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm, UpdateAccountForm, AddProduct, AddStock, UpdateProduct, UpdateStock



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


#Updating Product
@app.route("/update_product/<product_id>", methods = ["GET", "POST"])
@login_required
def update_product(product_id):
	product = Product.query.filter_by(product_id = product_id).first()
	form = UpdateProduct()
	if form.validate_on_submit():
		product.product_name = form.product_name.data
		product.product_category = form.product_category.data
		product.size = form.size.data
		product.price = form.price.data
		db.session.commit()
		return redirect(url_for("update_product", product_id = product_id))
	elif request.method == "GET":
		form.product_name.data = product.product_name
		form.product_category.data = product.product_category
		form.size.data = product.size
		form.price.data = product.price
	return render_template("stock/update_product.html", title = "Update Product", form = form)

@app.route("/update_stock/<product_name>", methods = ["GET", "POST"])
@login_required
def update_stock(product_name):
	stock = Stock.query.filter_by(product_name = product_name).first()
	form = UpdateStock()
	if form.validate_on_submit():
		stock.product_name = form.product_name.data
		stock.quantity = form.quantity.data
		db.session.commit()
		return redirect(url_for("update_stock", product_name = product_name))
	elif request.method == "GET":
		form.product_name.data = stock.product_name
		form.quantity.data = stock.quantity
	return render_template("stock/update_stock.html", title = "Update Stock", form = form)


@app.route("/product/delete/<product_id>")
@login_required
def delete_product(product_id):
	if current_user.is_authenticated:
		product = Product.query.filter_by(product_id = product_id).first()
		db.session.delete(product)
		db.session.commit
		return redirect(url_for("add_product"))



@app.route("/main_stock")
@login_required
def main_stock():
    StockData= Stock.query.all()
    return render_template('main_stock.html', "My Stock", Stock=StockData)