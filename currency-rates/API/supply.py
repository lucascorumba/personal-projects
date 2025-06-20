from flask import Flask, request, response
import sys
sys.path.append("/path/to/jsonify.py")
from jsonify import export_query_json

app = Flask(__name__)

@app.route("/endpoint")
def data():
    if request.args.get("auth") != "_":
        return Response(status=401)
    else:
        lookup = request.args.get("lookup")
        if lookup:
            # Query .db for refined search
            return Response(export_query_json(lookup=lookup, status=200, mimetype="application/json"))
        
        # Gets json file as _io.TextIOWrapper -- all records
        with open("/path/to/brl_prices.json", "r") as f:
            return Response(f.read(), status=200, mimetype="application/json")