#!/usr/local/pythonenvs/decifr-rest/bin/python

from flask import Flask, escape, request, Response
from flask import render_template
from werkzeug.serving import run_simple
import glob
from functools import wraps
import logging
import json
import traceback

logger = logging.getLogger("decifr-rest")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('/var/www/wsgi/decifr-rest/logs/logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s, %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug("start app")

app = Flask(__name__)
app.config['TMP_FOLDER'] = "/var/www/html/tbas2_1/tmp"
app.config['TMP_FOLDER'] = "/home/jim/.local/share/Trash/files"
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
def list():
    logger.debug("/list")

    files = glob.glob(
        "%s/phyloxml_cifr*.xml" % app.config['TMP_FOLDER']
    )
    files_updated = glob.glob(
        "%s/phyloxml_cifr_edit_metadata*.xml" % app.config['TMP_FOLDER']
    )
    files = set(files) - set(files_updated)
    runids = []
    runids_updated = []
    for file in files:
        runid = file[-12:-4]
        runids.append(runid)

    for file in files_updated:
        runid = file[-12:-4]
        runids_updated.append(runid)

    return render_template(
        'list.xml',
        runids=runids,
        runids_updated=runids_updated
    )


@app.route("/run/<runid>")
# @requires_auth
def run(runid):
    return render_template(
        'run.xml',
        runid=runid
    )


@app.route("/leaves/<runid>")
# @requires_auth
def leaves(runid):
    import scripts.get_leaves

    try:
        leaves_json = scripts.get_leaves.main(runid, app.config['TMP_FOLDER'])
        leaves = json.loads(leaves_json)
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return render_template(
        'leaves.xml',
        runid=runid,
        leaves=leaves
    )


@app.route("/leaf/<runid>/metadata")
# @requires_auth
def leaf(runid):
    query = request.args.get("query")
    return query



if __name__ == '__main__':
    run_simple('localhost', 8090, app, use_reloader=True)



