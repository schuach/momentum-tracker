import os
import sqlite3

from flask import Flask, g, render_template, jsonify, request

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY") or "SUPERSECRETKEY!"

DATABASE = "app.db"


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def get_state():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM state;")
    rv = cur.fetchall()
    cur.close()
    state = {"momentum": rv[0][1], "threat": rv[0][2]}
    return state


def update_state(resource, val):
    if resource == "momentum":
        query = """UPDATE state SET momentum = momentum + ? WHERE state_id = 1;"""
    elif resource == "threat":
        query = """UPDATE state SET threat = threat + ? WHERE state_id = 1;"""
    else:
        return

    connection = get_db()
    cur = connection.cursor()
    cur.execute(query, (val,))
    connection.commit()
    cur.close()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route("/")
@app.route("/index")
def index():
    state = get_state()
    return render_template("index.html", state=state)


@app.route("/update", methods=["GET", "POST"])
def update():
    current = get_state()
    json_data = request.json
    resource, val = json_data["resource"], json_data["val"]
    print(resource)

    if resource == "read":
        return jsonify(get_state())
    if val < 0 and current[resource] <= 0:
        return jsonify(get_state())
    if resource == "momentum" and current["momentum"] + val > 6:
        return jsonify(get_state())

    update_state(resource, val)
    return jsonify(get_state())
