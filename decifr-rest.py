#!/usr/local/pythonenvs/decifr-rest/bin/python

'''
pip install gunicorn==20.1.0
pip install eventlet==0.30.2

'''

from flask import Flask, request, Response
from markupsafe import escape
from flask import render_template
from flask import send_from_directory
import flask
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

# DeprecationWarning: The '__version__' attribute is deprecated
# logger.debug("flask version: %s" % flask.__version__)

app = Flask(__name__)
app.config['TMP_FOLDER'] = app_config.TMP_FOLDER
app.config['TOOL_FOLDER'] = app_config.TOOL_FOLDER
app.config['USE_TOOL_FOLDER'] = app_config.USE_TOOL_FOLDER

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
    return_type = request.args.get("return_type", "html")

    try:
        if app.config['USE_TOOL_FOLDER']:
            leaves_json = scripts.get_leaves.main(
                runid, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )
        else:
            leaves_json = scripts.get_leaves.main(
                runid, app.config['TMP_FOLDER']
            )
        leaves = json.loads(leaves_json)
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    if return_type == 'html':
        return render_template(
            'leaves.xml',
            runid=runid,
            leaves=leaves
        )
    else:
        return leaves_json


@app.route("/leaf/<runid>/metadata")
@requires_auth
def leaf(runid):
    import scripts.get_metadata
    query = request.args.get("query")
    try:
        if app.config['USE_TOOL_FOLDER']:
            retval = scripts.get_metadata.main(
                runid, query, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )

        else:
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
        if app.config['USE_TOOL_FOLDER']:
            queries_json = scripts.get_leaves.get_queries(
                runid, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )
        else:
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
    attr = request.args.get("attr", "na")
    try:
        if app.config['USE_TOOL_FOLDER']:
            retval = scripts.get_metadata.get_query(
                runid, query, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )
        else:
            retval = scripts.get_metadata.get_query(
                runid, query, app.config['TMP_FOLDER']
            )
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error
    if attr == 'na':
        return "<pre>%s</pre>" % retval
    else:
        result = json.loads(retval)

        return result['placement'][attr]


@app.route("/otus/<runid>")
@requires_auth
def otus(runid):
    import scripts.get_leaves

    try:
        if app.config['USE_TOOL_FOLDER']:
            otus_json = scripts.get_leaves.get_otus(
                runid, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )
        else:
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
        if app.config['USE_TOOL_FOLDER']:
            retval = scripts.get_metadata.otu_query(
                runid, query, "%s%s" % (app.config['TOOL_FOLDER'], runid)
            )
        else:
            retval = scripts.get_metadata.otu_query(
                runid, query, app.config['TMP_FOLDER']
            )
    except Exception:
        error = traceback.format_exc()
        return "<pre>%s</pre>" % error

    return "<pre>%s</pre>" % retval


@app.route("/mep/<runid>")
# @requires_auth
def mep(runid):
    '''

    wget --content-disposition --user admin --password secret localhost:8090/mep/<runid>

    Set  gzip off; in nginx may fix auto unzip in Chromium.

    '''
    # change path from uncompressed to zipped perm folder

    TMP_FOLDER = "%s/../" % app.config['TMP_FOLDER']

    logger.debug(TMP_FOLDER)

    if os.path.isfile("%s/%s_edit.mep.gz" % (TMP_FOLDER, runid)):
        return send_from_directory(
            TMP_FOLDER,
            "%s_edit.mep.gz" % runid,
            download_name="%s.mep.gz" % runid,
            as_attachment=True,
            mimetype='application/gzip'
        )
    else:
        return send_from_directory(
            TMP_FOLDER,
            "%s.mep.gz" % runid,
            download_name="%s.mep.gz" % runid,
            as_attachment=True,
            mimetype='application/gzip'
        )


if __name__ == '__main__':
    run_simple("0.0.0.0", 8090, app, use_reloader=True)



