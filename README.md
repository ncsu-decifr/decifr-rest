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
