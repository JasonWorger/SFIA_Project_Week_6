from flask import render_template, redirect, url_for, request
from application import app, db, bcrypt
from application.models import Users
from flask_login import login_user, current_user, logout_user, login_required
from application.forms import RegistrationForm, LoginForm


@app.route('/')
@app.route('/main_stock')
@login_required
def main_stock():
    stockData= main_stock.query.all()
    return render_template('main_stock.html', title='Stock List')




#This is the login route
@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main_stock'))
    form = LoginForm()
    if form.validate_on_submit():
        user=Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            else:
                return redirect(url_for('main_stock'))
    return render_template('login.html', title='Login', form=form)


#This is the register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main_stock'))
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

        return redirect(url_for('insert_stock'))
    return render_template('register.html', title='Register', form=form)



#This is the logout route
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))