import unittest


class TestUtils(unittest.TestCase):

	def test_orm(self):
		import sqlalchemy
		from flask import Flask
		from flask_sqlalchemy import SQLAlchemy
		from sqlalchemy.orm import sessionmaker
		import models

		app = Flask(__name__)
		# MariaDB Config
		SERVER_IP = "167.71.142.2"  # ip 167.71.142.2
		SERVER_USER = "root"
		SERVER_PASSWORD = "bikeeper"
		app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{}:{}@{}/BIKEEPER'.format(SERVER_USER, SERVER_PASSWORD, SERVER_IP)

		db = SQLAlchemy(app)

		engine = sqlalchemy.create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)  # , isolation_level="READ

		Session = sessionmaker(bind=engine)
		session = Session()



		self.assertEqual(False, "")


if __name__ == '__main__':
	unittest.main()
