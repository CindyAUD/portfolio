from flask import Flask
application = Flask(__name__)

@application.route('/')
def myPortfolio():
    return 'Add Things Here'