#!/usr/local/pythonenvs/decifr-rest/bin/python

from flask import Flask, escape, request
from werkzeug.serving import run_simple

app = Flask(__name__)


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


if __name__ == '__main__':
    run_simple('localhost', 8080, app, use_reloader=True)



