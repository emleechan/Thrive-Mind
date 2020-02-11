from datetime import datetime, timedelta
from flask import Flask, render_template, jsonify, request, make_response
from . import app
from auth import token_required, create_token

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")

@app.route("/hello/")
@app.route("/hello/<name>")
def hello_there(name = None):
    return render_template(
        "hello_there.html",
        name=name,
        date=datetime.now()
    )

@app.route("/api/data")
def get_data():
    return app.send_static_file("data.json")

@app.route('/unprotected')
def unprotected():
    return ''

@app.route('/protected')
@token_required
def protected():
    return jsonify({'message': 'protected route!'})

@app.route('/protected/route')
@token_required
def get_token():
    return ''

@app.route('/login')
def login():
    return create_token()
