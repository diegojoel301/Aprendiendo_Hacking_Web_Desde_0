from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "<h1>This is Admin Panel</h1>"

if __name__ == '__main__':
    app.run(port=7462)

