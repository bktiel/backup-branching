import json

from flask import Flask, render_template

app = Flask(__name__)

branches={}

with open('branches.json') as reader:
    branches=json.load(reader)


@app.route('/')
def hello_world():
    return render_template('base.html',branches=branches)


if __name__ == '__main__':
    app.run()
