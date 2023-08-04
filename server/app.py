from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import xmlrpc.client

app = Flask(__name__)
CORS(app)


load_dotenv()

url = os.getenv("URL")
db = os.getenv("DB")
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")


def is_odoo_connected():
    try:
        common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
        uid = common.authenticate(db, username, password, {})
        return True
    except xmlrpc.client.Fault as e:
        return False


@app.route("/")
def home():
    if is_odoo_connected():
        return "Hello World From Flask! Odoo is connected."
    else:
        return "Hello World From Flask! Odoo is not connected."


if __name__ == "__main__":
    app.run()
