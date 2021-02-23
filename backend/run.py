from flaskr import *
from settings import DEBUG

if __name__ == '__main__':
	create_app().run(debug=DEBUG)