# decifr-rest

The Representational State Transfer Application Program Interface (REST) server can be used to retrieve tree information from Metadata Enhanced PhyloXML (MEP) files.

## Installation

The decifr-rest server allows a user to share information about placements from T-BAS with other users via the web. The program is written to run in a Python 3 virtual environment. The default location of the virtual environment is set to /usr/local/pythonenvs. To change it edit the first line in the /usr/local/decifr-rest/decifr-rest.py script. Follow the commands below to create the virtual environment.

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
To share the results of some placements, copy the MEP files created either on the public T-BAS site or with docker to a folder on your computer, and uncompress them by double-clicking if on Mac or Windows or using Linux command gunzip *. An example (6BLUBNSA.mep.gz) is included. Edit the line in /usr/local/decifr-rest/decifr-rest.py with app.config['TMP_FOLDER'] = "/tmp/rest" to the value of the directory with the MEP files.
```
cd /tmp
mkdir rest
cd /usr/local/decifr-rest
cp 6BLUBNSA.mep.gz /tmp/rest
cd /tmp/rest
gunzip *
cd /usr/local/decifr-rest
./decifr-rest.py

```
To run just type ./decifr-rest.py. This will start the REST server. Open your browser to localhost:8090/list and there are links to a runid for each MEP file. Click on a link to see more information about the run.

If you want to restrict access to pages with basic authentication you can edit the /usr/local/decifr-rest/decifr-rest.py file. Each function in the file has a line @requires_auth that is commented out. If you uncomment this line that page will be restricted. Edit the function check_auth to set the login credentials.

### BSD 3-Clause License

Copyright (c) 2019, North Carolina State University
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. The names “North Carolina State University”, “NCSU” and any trade-name, personal name, trademark, trade device, service mark, symbol, image, icon, or any abbreviation, contraction or simulation thereof owned by North Carolina State University must not be used to endorse or promote products derived from this software without prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


