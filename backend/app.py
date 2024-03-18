import json
import os
from flask import Flask, request, send_from_directory
from flask_cors import CORS
from sql.MySQLDatabaseHandler import MySQLDatabaseHandler
from routes.DocSearchUN import doc_search_un_handler
from routes.DocSearchX import doc_search_x_handler
from routes.Summarize import summarize_handler
from lib.Utils import parseBool, parseInt

# BEGIN INITIAL SETUP ----------------------------------------------------------

# ROOT_PATH for linking with all files
os.environ['ROOT_PATH'] = os.path.abspath(os.path.join("..",os.curdir))

# Define DB connection parameters
LOCAL_MYSQL_USER = "root"
LOCAL_MYSQL_USER_PASSWORD = "admin"
LOCAL_MYSQL_PORT = 3306
LOCAL_MYSQL_DATABASE = "ourdb"
mysql_engine = MySQLDatabaseHandler(LOCAL_MYSQL_USER,LOCAL_MYSQL_USER_PASSWORD,LOCAL_MYSQL_PORT,LOCAL_MYSQL_DATABASE)
mysql_engine.load_file_into_db()

# Create the Flask app
app = Flask(__name__)
CORS(app)

# BEGIN FRONTEND ROUTES --------------------------------------------------------

# Path for our main Svelte page
@app.route("/")
def base():
    return send_from_directory('client/dist', 'index.html')

# Path for all the static files (compiled JS/CSS, etc.)
@app.route("/<path:path>")
def home(path):
    return send_from_directory('client/dist', path)


# BEGIN BACKEND ROUTES ---------------------------------------------------------

@app.route("/api/doc-search-un")
def doc_search_un():
    text = request.args.get("text") # string
    limit = parseInt(request.args.get("limit")) # int, optional
    agree = parseBool(request.args.get("agree")) # boolean, optional
    return json.dumps(doc_search_un_handler(mysql_engine,text,limit,agree))

@app.route("/api/doc-search-x")
def doc_search_x():
    text = request.args.get("text") # string
    limit = parseInt(request.args.get("limit")) # int, optional
    agree = parseBool(request.args.get("agree")) # boolean, optional
    return json.dumps(doc_search_x_handler(mysql_engine,text,limit,agree))

@app.route("/api/summarize")
def summarize():
    text = request.args.get("text")
    return json.dumps(summarize_handler(mysql_engine,text))

# RUN APP ----------------------------------------------------------------------

if 'DB_NAME' not in os.environ:
    app.run(debug=True,host="0.0.0.0",port=5000)