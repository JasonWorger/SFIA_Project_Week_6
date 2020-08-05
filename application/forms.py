from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField, DecimalField, IntegerField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from application.models import Users, Product, Stock
from flask_login import current_user


#This is the registration form
class RegistrationForm(FlaskForm):
    
    first_name = StringField('First Name',
    validators=[
        DataRequired(),
        Length(min=2, max=30)
    ])
    
    last_name = StringField('Last Name',
    validators=[
        DataRequired(),
        Length(min=3, max=30)
    ])
       
    
    email = StringField('Email',
        validators = [
            DataRequired(),
            Email()
        ]
    )
    password = PasswordField('Password',
        validators = [
            DataRequired(),
        ]
    )
    confirm_password = PasswordField('Confirm Password',
        validators = [
            DataRequired(),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = Users.query.filter_by(email=email.data).first()

        if user:
            raise ValidationError('Email already in use')

#This is the login form
class LoginForm(FlaskForm):
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField('Password',
        validators=[
            DataRequired()
        ]
    )

    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


#This is the update account form
class UpdateAccountForm(FlaskForm):
    first_name = StringField('First Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    last_name = StringField('Last Name',
        validators=[
            DataRequired(),
            Length(min=4, max=30)
        ])
    email = StringField('Email',
        validators=[
            DataRequired(),
            Email()
        ])
    submit = SubmitField('Update Account')

    def validate_email(self,email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already in use')



#Add Product Form
class AddProduct(FlaskForm):
    product_name = StringField("Product Name", validators = [DataRequired()])
    product_category = StringField("Type Of Drink", validators = [Length(min=0, max=100)])
    size = StringField("Product Size", validators = [DataRequired()])
    price = DecimalField("Price, places=2)
    submit = SubmitField("Add Product")"

    def validate_product_exists(self, product_name):
        product_name = Product.query.filter_by(product_name=product_name.data).first()
        if product_name is not None:
            raise ValidationError("This product has already been added. Please enter a new product.")



#Add Bar Stock Form
class AddStock(FlaskForm):
    product_name = StringField("Product Name", validators = [DataRequired()])
    quantity = IntegerField("Stock Quantity")
    submit = SubmitField("Add Stock")

    def validate_product_exists(self, product_name):
        product_name = Product.query.filter_by(product_name=product_name.data).first()
        if product_name is not None:
            raise ValidationError("Unable to add stock as product does not exist. Please add the product")


#Edit Product Form

#Edit Stock Form