import unittest
from flask import url_for
from flask_testing import TestCase
from application import app, db, bcrypt
from application.models import Users, Product, Stock
from os import getenv

class TestBase(TestCase):
	def create_app(self):
		# pass in configurations for test database
		config_name = 'testing'
		app.config.update(SQLALCHEMY_DATABASE_URI=getenv('TEST_DB_URI'),
				SECRET_KEY=getenv('TEST_SECRET_KEY'),
				WTF_CSRF_ENABLED=False,
				DEBUG=True
				)
		return app

	def setUp(self):
		"""
		Will be called before every test
		"""
		# ensure there is no data in the test database when the test starts
		db.session.commit()
		db.drop_all()
		db.create_all()

		# create test admin user
		hashed_pw = bcrypt.generate_password_hash('admin2016')
		admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password=hashed_pw)

		# create test non-admin user
		hashed_pw_2 = bcrypt.generate_password_hash('test2016')
		employee = Users(first_name="test", last_name="user", email="test@user.com", password=hashed_pw_2)

		# Creating a test product
		testproduct = Product(
			product_id = 1,
			product_name = "Water",
			product_category = "Soft",
			price = 2.00,
			size = 500
		)

		#Creating a test stock
		teststock = Stock(
			id = 1,
			product_id = 1,
			quantity = 5
		)

		# save users to database
		db.session.add(admin)
		db.session.add(employee)
		db.session.add(testproduct)
		db.session.add(teststock)
		db.session.commit()
		

	def tearDown(self):
		"""
		Will be called after every test
		"""

		db.session.remove()
		db.drop_all()


class TestViews(TestBase):
	# Test that register and login are accessible without being logged in
	def test_register_view(self):
		response = self.client.get(url_for('register'))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"register", response.data)
	
	def test_login_view(self):	
		response = self.client.get(url_for('login'))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"login", response.data)


class TestProductPages(TestBase):
	# Tests ensuring the correct pages load when user is logged in
	def test_login_main_stock(self):
		with self.client:
			self.client.post(
				url_for("login"),
				data = dict(
					email = "admin@admin.com",
					password = "admin2016"
				),
				follow_redirects = True
			)
		response = self.client.get(url_for('main_stock'))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Stock List", response.data)
		
	
	def test_login_updateProduct(self):
		with self.client:
			self.client.post(
				url_for("login"),
				data = dict(
					email = "admin@admin.com",
					password = "admin2016"
				),
				follow_redirects = True
			)
		response = self.client.get(url_for('updateProduct', product_id = 1))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Update Product", response.data)
	
	def test_login_addProduct(self):
		with self.client:
			self.client.post(
				url_for("login"),
				data = dict(
					email = "admin@admin.com",
					password = "admin2016"
				),
				follow_redirects = True
			)
		response = self.client.get(url_for('addProduct'))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Add Product", response.data)
	
	def test_login_addStock(self):
		with self.client:
			self.client.post(
				url_for("login"),
				data = dict(
					email = "admin@admin.com",
					password = "admin2016"
				),
				follow_redirects = True
			)
		response = self.client.get(url_for('addStock'))
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Add Stock", response.data)
	


class TestLoginPages(TestBase):
	# testing to make sure that the correct pages load when a user is not logged in
	def test_notloggedin_addProduct(self):
		response1 = self.client.get(url_for("addProduct"), follow_redirects = True)
		self.assertEqual(response1.status_code, 200)
		self.assertIn(b"login", response1.data)
	
	def test_notloggedin_addStock(self):
		response2 = self.client.get(url_for("addStock"), follow_redirects = True)
		self.assertEqual(response2.status_code, 200)
		self.assertIn(b"login", response2.data)
	
	def test_notloggedin_updateProduct(self):
		response3 = self.client.get(url_for("updateProduct", product_id=1), follow_redirects = True)
		self.assertEqual(response3.status_code, 200)
		self.assertIn(b"login", response3.data)

	def test_notloggedin_main_stock(self):
		response5 = self.client.get(url_for("main_stock"), follow_redirects = True)
		self.assertEqual(response5.status_code, 200)
		self.assertIn(b"login", response5.data)


#Testing the register,login and logout of user views
class TestUserViews(TestBase):
	def test_register(self):
		response = self.client.post(
			url_for('register'),
			data = dict(
				first_name = 'Joe',
				last_name = 'Bloggs',
				email = 'Joebloggs@mail.com',
				password = 'password',
				confrim_password = 'password',
			),
			follow_redirects = True
		)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"login", response.data)

	def test_users_login(self):
		response = 	self.client.post(
			url_for("login"),
			data = dict(
				email = "admin@admin.com",
				password = "admin2016"
			),
			follow_redirects = True
		)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"Add Product", response.data)


	def test_logout(self):
		with self.client:
			self.client.post(
				url_for("login"),
				data = dict(
					email = "admin@admin.com",
					password = "admin2016"
				),
				follow_redirects = True
			)
		response = self.client.get('logout', follow_redirects = True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"login", response.data)

# #Testing the stock pages as a user logged in
# class TestStockViews(TestBase):
# 	def test_add_stock(self):
# 		with self.client:
# 			self.client.post(
# 				url_for("login"),
# 				data = dict(
# 					username = "user1",
# 					password = "password1"
# 				),
# 				follow_redirects = True
# 			)
# 			response = self.client.get(url_for("updateProduct"))
# 			self.assertEqual(response.status_code, 200)
# 			self.assertIn(b"Update Product", response.data)

# 	def test_update_stock(self):
# 		with self.client:
# 			self.client.post(
# 				url_for("login"),
# 				data = dict(
# 					username = "user1",
# 					password = "password1"
# 				),
# 				follow_redirects = True
# 			)
# 			response = self.client.get(url_for("updateStock", product_id = 1))
# 			self.assertEqual(response.status_code, 200)
# 			self.assertIn(b"Update Stock", response.data)


class TestAdd(TestBase):
	def test_addProduct(self):
	# Test that when a product is added, the user is redirected to the add stock page
		with self.client:
			self.client.post(url_for('login'), data=dict(email='admin@admin.com',password='admin2016'),follow_redirects=True)
		response = self.client.post(
			'/addProduct',
			data=dict(
				product_name = "Test name",
				product_category = "Test category",
				price = "3.50",
				size = "330",
			),
			follow_redirects=True
		)
		self.assertIn(b'addStock', response.data)
		self.assertEqual(response.status_code, 200)


	def test_addStock(self):
	# Test that when stock is added, the user is redirected to the main stock page
		with self.client:
			self.client.post(url_for('login'), data=dict(email='admin@admin.com',password='admin2016'),follow_redirects=True)
		response = self.client.post(
			'/addStock',
			data=dict(
				product_name = "Water",
				quantity = "5",
			),
			follow_redirects=True
		)
		self.assertIn(b'Stock List', response.data)
		self.assertEqual(response.status_code, 200)

class TestUpdate(TestBase):
	# Test that when product or stock is updated, the user is redirected to the correct page visible.
	def test_UpdateProduct(self):
		with self.client:
			self.client.post(url_for('login'), data=dict(email='admin@admin.com',password='admin2016'),follow_redirects=True)
			self.client.get(url_for('updateProduct', product_id = 1), follow_redirects=True)

		response = self.client.post(url_for('updateProduct', product_id = 1), follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Stock List', response.data)



	# Test that when a use deletes a product from the stock list they are redirected to the correct page
	def test_DeleteProduct(self):
		with self.client:
			self.client.post(url_for("login"),data = dict(email='admin@admin.com',password='admin2016'),follow_redirects = True)
		response = self.client.post(
			url_for("deleteProduct", product_id = 1),
		follow_redirects=True)
		self.assertIn(b'Add Product',response.data)
		self.assertEqual(response.status_code, 200)



