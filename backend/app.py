import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from sql.MySQLDatabaseHandler import MySQLDatabaseHandler
from routes.DocSearchUN import doc_search_un_handler
from routes.DocSearchX import doc_search_x_handler
from routes.Summarize import summarize_handler
from lib.Utils import formatServerResponse, parseBool, parseInt

# BEGIN INITIAL SETUP ----------------------------------------------------------

# ROOT_PATH for linking with all files
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# Define DB connection parameters
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = "admin"
LOCAL_MYSQL_PORT = 3306
LOCAL_MYSQL_DATABASE = "kardashiandb"
mysql_engine = MySQLDatabaseHandler(LOCAL_MYSQL_USER,LOCAL_MYSQL_USER_PASSWORD,LOCAL_MYSQL_PORT,LOCAL_MYSQL_DATABASE)
mysql_engine.load_file_into_db()

# Create the Flask app
app = Flask(__name__)
CORS(app)

# BEGIN ROUTES -----------------------------------------------------------------

# Serve main frontend page
@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')

# Serve backend endpoint to search UN documents
@app.route("/api/searchun")
def doc_search_un():
    text = request.args.get("text") # string
    limit = parseInt(request.args.get("limit")) # int, optional
    return formatServerResponse(doc_search_un_handler(mysql_engine,text,limit))

# Serve backend endpoint to search X documents
@app.route("/api/searchx")
def doc_search_x():
    text = request.args.get("text") # string
    limit = parseInt(request.args.get("limit")) # int, optional
    return formatServerResponse(doc_search_x_handler(mysql_engine,text,limit))

# Serve backend endpoint to summarize text
@app.route("/api/summarize")
def summarize():
    text = request.args.get("text")
    return formatServerResponse(summarize_handler(mysql_engine,text))

# Serve all remaining files from the frontend
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)

# RUN APP ----------------------------------------------------------------------

if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)