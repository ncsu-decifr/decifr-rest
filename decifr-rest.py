#!/usr/local/pythonenvs/decifr-rest/bin/python

from flask import Flask, escape, request
from flask import render_template
from werkzeug.serving import run_simple
import glob

app = Flask(__name__)
app.config['TMP_FOLDER'] = "/var/www/html/tbas2_1/tmp"


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, %s!' % escape(name)


@app.route("/rest")
def rest():

    files = glob.glob("%s/phyloxml_cifr*.xml" % app.config['TMP_FOLDER'])
    runids = []
    for file in files:
        runid = file[-12:-4]
        runids.append(runid)

    return render_template(
        'rest.html',
        runids=runids
    )


if __name__ == '__main__':
    run_simple('localhost', 8080, app, use_reloader=True)



