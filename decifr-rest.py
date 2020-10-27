#!/usr/local/pythonenvs/decifr-rest/bin/python

from flask import Flask, escape, request, Response
from flask import render_template
from werkzeug.serving import run_simple
import glob
from functools import wraps
import logging
import json
import traceback
import os
import app_config

logger = logging.getLogger("decifr-rest")
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('logs/logs.log')
formatter = logging.Formatter(
    '%(asctime)s - %(name)s, %(lineno)s - %(levelname)s - %(message)s',
    datefmt='%m/%d %H:%M:%S'
)
fh.setFormatter(formatter)
logger.addHandler(fh)
logger.debug("start app")

app = Flask(__name__)
app.config['TMP_FOLDER'] = app_config.TMP_FOLDER
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
    if username == app_config.USERNAME and password == app_config.PASSWORD:
        return True
    else:
        return False


@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return 'Hello, %s!' % escape(name)


@app.route("/list")
@requires_auth
def list():
    logger.debug("/list")

    mep_files = glob.glob(
        "%s/*.mep" % app.config['TMP_FOLDER']
    )

    runids = []
    for file in mep_files:
        basename = os.path.basename(file)
        runids.append(basename.replace(".mep", ""))

    return render_template(
        'list.xml',
        runids=runids
    )


@app.route("/run/<runid>")
@requires_auth
def run(runid):
    return render_template(
        'run.xml',
        runid=runid
    )


@app.route("/leaves/<runid>")
@requires_auth
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
@requires_auth
def leaf(runid):
    import scripts.get_metadata
    query = request.args.get("query")
    try:
        retval = scripts.get_metadata.main(
            runid, query, app.config['TMP_FOLDER']
        )
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return "<pre>%s</pre>" % retval


@app.route("/queries/<runid>")
@requires_auth
def queries(runid):
    import scripts.get_leaves

    try:
        queries_json = scripts.get_leaves.get_queries(
            runid, app.config['TMP_FOLDER']
        )
        queries = json.loads(queries_json)
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return render_template(
        'queries.xml',
        runid=runid,
        queries=queries
    )


@app.route("/query/<runid>/metadata")
@requires_auth
def query(runid):
    import scripts.get_metadata
    query = request.args.get("query")
    try:
        retval = scripts.get_metadata.get_query(
            runid, query, app.config['TMP_FOLDER']
        )
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return "<pre>%s</pre>" % retval


@app.route("/otus/<runid>")
@requires_auth
def otus(runid):
    import scripts.get_leaves

    try:
        otus_json = scripts.get_leaves.get_otus(
            runid, app.config['TMP_FOLDER']
        )
        otus = json.loads(otus_json)
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    # return otus_json

    return render_template(
        'otus.xml',
        runid=runid,
        otus=otus
    )


@app.route("/otu/<runid>/metadata")
@requires_auth
def otu(runid):
    import scripts.get_metadata
    query = request.args.get("query")
    try:
        retval = scripts.get_metadata.otu_query(
            runid, query, app.config['TMP_FOLDER']
        )
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return "<pre>%s</pre>" % retval


if __name__ == '__main__':
    run_simple("0.0.0.0", 8090, app, use_reloader=True)



