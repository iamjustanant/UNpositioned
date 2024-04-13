import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from routes.DocGetHandler import doc_get_handler
from routes.DocPreviewHandler import doc_preview_handler
from routes.DocSearchHandler import doc_search_handler
from routes.TermSearchHandler import term_search_handler
from sql.MySQLDatabaseHandler import MySQLDatabaseHandler
from lib.Utils import formatServerResponse, parseArg, parseBool, parseInt

# BEGIN INITIAL SETUP ----------------------------------------------------------

# ROOT_PATH for linking with all files
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# Define DB connection parameters
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = "admin"
LOCAL_MYSQL_PORT = 3306
LOCAL_MYSQL_DATABASE = "kardashiandb"
mysql_engine = MySQLDatabaseHandler(LOCAL_MYSQL_USER,LOCAL_MYSQL_USER_PASSWORD,LOCAL_MYSQL_PORT,LOCAL_MYSQL_DATABASE)

# load data
# mysql_engine.load_file_into_db()

# Create the Flask app
app = Flask(__name__)
CORS(app)

# BEGIN ROUTES -----------------------------------------------------------------

# Serve main frontend page
@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')

# Serve endpoints
@app.route("/api/termsearch")
def termsearch():
    queryStr = parseArg(request.args.get("text").replace("+"," "))
    desiredType = parseArg(request.args.get("type"))
    limit = parseInt(request.args.get("limit"))
    return formatServerResponse(term_search_handler(mysql_engine,queryStr,desiredType,limit))

@app.route("/api/docsearch")
def docsearch():
    queryDocID = parseArg(request.args.get("doc_id"))
    queryDocType = parseArg(request.args.get("doc_type"))
    desiredType = parseArg(request.args.get("type"))
    limit = parseInt(request.args.get("limit"))
    return formatServerResponse(doc_search_handler(mysql_engine,queryDocID,queryDocType,desiredType,limit))

@app.route("/api/getdocpreview")
def docpreview():
    queryDocID = parseArg(request.args.get("doc_id"))
    queryDocType = parseArg(request.args.get("doc_type"))
    return formatServerResponse(doc_preview_handler(mysql_engine,queryDocID,queryDocType))

@app.route("/api/getdoc")
def doc_search_rep():
    queryDocID = parseArg(request.args.get("doc_id"))
    queryDocType = parseArg(request.args.get("doc_type"))
    return formatServerResponse(doc_get_handler(mysql_engine,queryDocID,queryDocType))

# Serve all remaining files from the frontend
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)

# RUN APP ----------------------------------------------------------------------

if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)