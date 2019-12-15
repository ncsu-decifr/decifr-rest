# decifr-rest
DeCIFR REST server

The REST server to can be used to retrieve tree information from metadata enhanced Phyloxml (.mep) files.

## Installation

```
cd /usr/local/pythonenvs
python3 -m venv decifr-rest
source decifr-rest/bin/activate
pip install Flask
pip install lxml
cd /usr/local
git clone https://github.com/ncsu-decifr/decifr-rest.git

```

The REST  server allows a user to share information about placemnts from TBAS with other users via the web. To share the results of some placements copy the metadata enhanced Phyloxml (.mep) files created either on the publice TBAS site or with docker to a folder on your computer. If they are compressed then uncompress them (gunzip *). Edit the app.config['TMP_FOLDER']  parameter in the main file to point to this directory.

```
cp /var/www/html/tbas2_1/tmp/*.mep.gz /tmp/rest
cd /tmp/rest
gunzip *
app.config['TMP_FOLDER'] = /tmp/rest
cd /usr/local/decifr-rest
./decifr-rest.py

```

To run just type ./decifr-rest.py. This will start a development server. To run in production it would be best to run with a production server. The server should be available in your browser at localhost:8090/list

To restrict access to pages with basic auth add the @requires_auth decorator to the function and edit the function check_auth.



