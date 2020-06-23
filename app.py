from flask import Flask, request,  render_template
from all import *
from sent import *

app = Flask(__name__)


def alldraft():
    fetch()


def checklabel():
    makelabel()


@app.route('/')
def index():
    return render_template('app.html')


@app.route("/fetch")
def senddraft():
    alldraft()
    return 'OK'

@app.route("/label")
def label():
    checklabel()
    return 'OK'


if __name__ == '__main__':
    app.run(debug=False, threaded=False)
