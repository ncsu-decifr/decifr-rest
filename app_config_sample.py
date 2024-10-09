'''
copy this file to app_config.py and edit

TMP_FOLDER - folder where unzipped mep files can be found.
TOOL_FOLDER - folder where decifr tools has put a folder rest<runid> with unzipped file.
USE_TOOL_FOLDER - True of False to look for unzipped files in TMP_FOLDER
or TOOL_FOLDER.

'''


TMP_FOLDER = "/var/www/xml_archives"
USERNAME = 'admin'
PASSWORD = 'secret'

# set to full path of tool folder less <runid>
TOOL_FOLDER = "/var/www/html/tbas2_1/tmp/rest"
USE_TOOL_FOLDER = True

