from flask import Flask, jsonify, render_template, request


app = Flask(__name__)


@app.route('/data/', methods = ['GET'])
def data():



@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
