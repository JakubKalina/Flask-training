from flask import Flask, jsonify, request, make_response

app = Flask(__name__)

app.config["SECRET_KEY"] = "USERSECRETKEY"

from app import views
