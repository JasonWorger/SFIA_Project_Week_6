import unittest
import time
from flask import url_for
from urllib.request import urlopen
from os import getenv
from flask_testing import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from application import app, db, bcrypt
from application.models import Users, Product, Stock

# Set test variables for test admin user
test_admin_first_name = "admin"
test_admin_last_name = "admin"
test_admin_email = "admin@email.com"
test_admin_password = "admin2020"


class TestBase(LiveServerTestCase):

	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = str(getenv('TEST_DB_URI'))
		app.config['SECRET_KEY'] = getenv('TEST_SECRET_KEY')
		return app

	def setUp(self):
		"""Setup the test driver and create test users"""
		print("------------------NEXT-TEST------------------")
		chrome_options = Options()
		chrome_options.binary_location = "/usr/bin/chromium-browser"
		chrome_options.add_argument("--headless")
		self.driver = webdriver.Chrome(executable_path="/home/jasonworger/SFIA_Project_Week_6/chromedriver", chrome_options=chrome_options)
		self.driver.get("http://localhost:5000")
		db.session.commit()
		db.drop_all()
		db.create_all()

		
		# create test admin user
		hashed_pw = bcrypt.generate_password_hash('admin2016')
		admin = Users(first_name="admin", last_name="admin", email="admin@admin.com", password=hashed_pw)

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
			prooduct_id = 1,
			quantity = 5
		)

		#Adding the test product and stock to the test database
		db.session.add(admin)
		db.session.add(testproduct)
		db.session.add(teststock)
		db.session.commit()

	def tearDown(self):
		self.driver.quit()
		print("--------------------------END-OF-TEST----------------------------------------------\n\n\n-------------------------UNIT-AND-SELENIUM-TESTS----------------------------------------------")

	def test_server_is_up_and_running(self):
		response = urlopen("http://localhost:5000")
		self.assertEqual(response.code, 200)


#These are tests to ensure the nav bar is woring accordingly
class TestNavBar(TestBase):

	#Register
	def test_register(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()
		assert url_for("register") in self.driver.current_url

	#Login
	def test_login(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()
		assert url_for("login") in self.driver.current_url

	#Main Stock
	def test_main_stock(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()
		assert url_for("main_stock") in self.driver.current_url

	#Adding Product	
	def test_add_product(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/a[3]").click()
		assert url_for("addProduct") in self.driver.current_url

	#Adding Stock
	def test_add_stock(self):
		self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()
		assert url_for("addStock") in self.driver.current_url




class TestRegistration(TestBase):

	def test_registration(self):
		"""
		Test that a user can create an account using the registration form
		if all fields are filled out correctly, and that they will be 
		redirected to the login page
		"""

		# Clicking on register in nav bar
		self.driver.find_element_by_xpath("/html/body/div[1]/a[2]").click()
		time.sleep(1)

		# Filling in registration form
		self.driver.find_element_by_xpath('//*[@id="email"]').send_keys(test_admin_email)
		self.driver.find_element_by_xpath('//*[@id="first_name"]').send_keys(
			test_admin_first_name)
		self.driver.find_element_by_xpath('//*[@id="last_name"]').send_keys(
			test_admin_last_name)
		self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(
			test_admin_password)
		self.driver.find_element_by_xpath('//*[@id="confirm_password"]').send_keys(
			test_admin_password)
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()
		time.sleep(1)

		# Assert that browser redirects to login page
		assert url_for("login") in self.driver.current_url


class TestLogin(TestBase):

	def test_login(self):

		#Click on the login nav bar link
		self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()
		time.sleep(1)
		assert url_for("login") in self.driver.current_url
		
		# inputs the test user email
		self.driver.find_element_by_xpath('//*[@id="email"]"').send_keys(test_admin_email)
		
		# inputs the test user password
		self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
		
		# click the login button
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()
		
		# checks that you've logged in correctly
		assert url_for("addProduct") in self.driver.current_url



#For the following tests the user must be logged in. Therefore the test will start with the user logging in.
class TestAddProduct(TestBase):

	def test_add_product(self):

		self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()
		time.sleep(1)
		assert url_for("login") in self.driver.current_url
		self.driver.find_element_by_xpath('//*[@id="email"]"').send_keys(test_admin_email)
		self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()
		assert url_for("addProduct") in self.driver.current_url

		#Navigating to add product page
		self.driver.find_element_by_xpath('/html/body/div[1]/a[3]').click()
		assert url_for("addProduct") in self.driver.current_url
		
		#Input product name
		self.driver.find_element_by_xpath('//*[@id="product_name"]').send_keys("Water")
		
		#Input Type of drink
		self.driver.find_element_by_xpath('//*[@id="product_category"]').send_keys("Soft")
		
		#Input product size
		self.driver.find_element_by_xpath('//*[@id="size"]').send_keys("500")
		
		#Input Price
		self.driver.find_element_by_xpath('//*[@id="price"]').send_keys("2.00")
		
		#Click on add product button
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()
		
		#Check that the item has been added
		assert url_for("addStock") in self.driver.current_url


class TestAddStock(TestBase):

	def test_add_stock(self):

		self.driver.find_element_by_xpath("/html/body/div[1]/a[1]").click()
		time.sleep(1)
		assert url_for("login") in self.driver.current_url
		self.driver.find_element_by_xpath('//*[@id="email"]"').send_keys(test_admin_email)
		self.driver.find_element_by_xpath('//*[@id="password"]').send_keys(test_admin_password)
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()
		assert url_for("addProduct") in self.driver.current_url

		#Navigating to add stock page
		self.driver.find_element_by_xpath('/html/body/div/a[2]').click()  
		assert url_for("addStock") in self.driver.current_url

		#Input product name
		self.driver.find_element_by_xpath('//*[@id="product_name"]').send_keys("Water")

		#Input stock quantity 
		self.driver.find_element_by_xpath('//*[@id="quantity"]').send_keys("5")

		#Click on add stock button
		self.driver.find_element_by_xpath('//*[@id="submit"]').click()

		#Check that the item has been added
		assert url_for("main_stock") in self.driver.current_url