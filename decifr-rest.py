#!/usr/local/pythonenvs/decifr-rest/bin/python

from flask import Flask, escape, request, Response
from flask import render_template
from werkzeug.serving import run_simple
import glob
from functools import wraps

app = Flask(__name__)
app.config['TMP_FOLDER'] = "/var/www/html/tbas2_1/tmp"
app.config['TEMPLATES_AUTO_RELOAD'] = True


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


def authenticate():
    """Sends a 401 response that enables basic auth"""
    return Response(
        'Could not verify your access level for that URL.\n'
        'You have to login with proper credentials', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )


def check_auth(username, password):
    if username == 'admin' and password == 'secret':
        return True
    else:
        return False


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, %s!' % escape(name)


@app.route("/list")
def rest():

    files = glob.glob("%s/phyloxml_cifr*.xml" % app.config['TMP_FOLDER'])
    runids = []
    for file in files:
        runid = file[-12:-4]
        runids.append(runid)

    return render_template(
        'list.xml',
        runids=runids
    )


@app.route("/runs/<runid>")
@requires_auth
def runs(runid):
    return render_template(
        'run.xml',
        runid=runid
    )


if __name__ == '__main__':
    run_simple('localhost', 8090, app, use_reloader=True, )



