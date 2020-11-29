from flask import Flask
from flask_restful import Resource,Api

token = '1483448860:AAHAdj7RRYpOsbe0S3pMr4nguA3t7k-AfIc'

app = Flask(__name__)
api = Api(app)

products = {}

class telegram_bot(Resource):
    pass

api.add_resource(telegram_bot,'/')

if __name__ == '__main__':
    app.run(debug=True)