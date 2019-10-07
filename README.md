# decifr-rest
DeCIFR REST server

The REST server to can be used to retrieve tree information from cifr PhyloXML files.

## Installation

```
cd /usr/local/pythonenvs
python3 -m venv decifr-rest
source decifr-rest/bin/activate
pip install Flask
pip install lxml
```

To restrict access to pages with basic auth add the @requires_auth decorator to the function and edit the function check_auth.

Copy cifr phyloXML files to a directory and then set that with the app.config['TMP_FOLDER'] variable.

To run just type ./decifr-rest.py. This will start a development server. To run in production it would be best to run with a production server. The server should be available in your browser at localhost:8090/list
