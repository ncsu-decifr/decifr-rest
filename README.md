# decifr-rest
DeCIFR REST API

## Installation

```
cd /usr/local/pythonenvs
python3 -m venv decifr-rest
source decifr-rest/bin/activate
pip install Flask
pip install lxml
```

To restrict access to pages with basic auth add the @requires_auth decorator to the function and edit the function check_auth.