# decifr-rest
DeCIFR REST server

The Representational State Transfer Application Program Interface (REST) server to can be used to retrieve tree information from Metadata  Enhanced Phyloxml (MEP) files.

## Installation

The REST server allows a user to share information about placements from T-BAS with other users via the web. The program is written to run in a Python 3 virtual environment. The default location of the virtual environment is set to /usr/local/pythonenvs. To change it edit the first line in the /usr/local/decifr-rest/decifr-rest.py script. Follow the commands below to create the virtual environment.

```
cd /usr/local
sudo su
mkdir pythonenvs
cd /usr/local/pythonenvs
python3 -m venv decifr-rest
source decifr-rest/bin/activate
pip install Flask
pip install lxml
```

Next install the server using git.

```
cd /usr/local
git clone https://github.com/ncsu-decifr/decifr-rest.git
```

To share the results of some placements, copy the MEP files created either on the public T-BAS site or with docker to a folder on your computer, and uncompress them by double-clicking if on Mac or Windows or using Linux command gunzip *. An example (6BLUBNSA.mep.gz) is included. Edit the app.config['TMP_FOLDER']  parameter in the main file to point to this directory.

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



