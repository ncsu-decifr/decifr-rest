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

To share the results of some placements, copy the MEP files created either on the public T-BAS site or with docker to a folder on your computer, and uncompress them by double-clicking if on Mac or Windows or using Linux command gunzip *. An example (6BLUBNSA.mep.gz) is included. Edit the line in decifr-rest .py that says app.config['TMP_FOLDER'] = "/tmp/rest" to the value of the directory with the MEP files.

```
cp /var/www/html/tbas2_1/tmp/*.mep.gz /tmp/rest
cd /tmp/rest
gunzip *
app.config['TMP_FOLDER'] = /tmp/rest
cd /usr/local/decifr-rest
./decifr-rest.py

```

To run just type ./decifr-rest.py. This will start the REST server. Open your browser to localhost:8090/list and there are links to a runid for each MEP file. Click on a link to see more information about the run.

If you want to restrict access to pages with basic authentication you can edit the decifr-rest.py file. Each function in the file has a line @requires_auth that is commented out. If you uncomment this line that page will be restricted. Edit the function check_auth to set the login credentials.



