from flask import Flask, render_template, jsonify, session, request
import requests
from bs4 import BeautifulSoup
from flask_cors import CORS
from dotenv import load_dotenv
import os
import xmlrpc.client
import jwt
import datetime
from urllib.parse import urlparse, parse_qs
import flask_session

app = Flask(__name__)
CORS(
    app,
    resources={
        r"/*": {"origins": "*", "methods": ["POST"], "allow_headers": ["Content-Type"]}
    },
)


load_dotenv()
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")


def get_odoo_server():
    odoo_url = os.environ.get("ODOO_URL")
    odoo_db = os.environ.get("ODOO_DB")
    odoo_username = os.environ.get("ODOO_USERNAME")
    odoo_password = os.environ.get("ODOO_PASSWORD")

    if not all([odoo_url, odoo_db, odoo_username, odoo_password]):
        return None, None

    common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
    uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

    if uid:
        return xmlrpc.client.ServerProxy(
            f"{odoo_url}/xmlrpc/2/object", allow_none=True
        ), int(uid)

    return None, None


@app.route("/")
def home():
    return "Hello World, from Flask! Odoo is connected."


@app.route("/get_secret_key", methods=["GET"])
def get_secret_key():
    return jsonify({"secret_key": app.config["SECRET_KEY"]})


@app.route("/list_partners")
def list_partners():
    server, uid = get_odoo_server()
    if server and uid:
        partner_ids = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "res.partner",
            "search",
            [[]],
        )

        if not partner_ids:
            return "No partners found."
        else:
            partner_data = server.execute_kw(
                os.environ.get("ODOO_DB"),
                uid,
                os.environ.get("ODOO_PASSWORD"),
                "res.partner",
                "read",
                [partner_ids],
                {"fields": ["name", "is_company"]},
            )
            if partner_data:
                partners_info = ""
                for partner in partner_data:
                    partners_info += f"ID: {partner['id']}<br>"
                    partners_info += f"Name: {partner['name']}<br>"
                    partners_info += f"Is Company: {partner['is_company']}<br>"
                    partners_info += "-------<br>"
                return partners_info
            else:
                return "Failed to retrieve partner data."
    else:
        return "Could not connect to Odoo server."


@app.route("/inventory_overview")
def inventory_overview():
    server, uid = get_odoo_server()
    if server and uid:
        picking_type_ids = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "stock.picking.type",
            "search",
            [[]],
        )

        if not picking_type_ids:
            return jsonify([])  # Return an empty JSON array
        else:
            picking_type_data = server.execute_kw(
                os.environ.get("ODOO_DB"),
                uid,
                os.environ.get("ODOO_PASSWORD"),
                "stock.picking.type",
                "read",
                [picking_type_ids],
                {"fields": ["name", "code", "sequence"]},
            )
            if picking_type_data:
                return jsonify(picking_type_data)  # Return the JSON data directly
            else:
                return jsonify([])  # Return an empty JSON array
    else:
        return jsonify({"error": "Could not connect to Odoo server."})


@app.route("/stock_picking_data")
def stock_picking_data():
    server, uid = get_odoo_server()
    if server and uid:
        picking_data = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "stock.picking",
            "search_read",
            [],
            {"fields": ["name"], "context": {}},
        )

        if picking_data:
            picking_info = ""
            for picking in picking_data:
                picking_info += f"Name: {picking['name']}<br>"
                picking_info += "-------<br>"
            return picking_info
        else:
            return "No stock pickings found."
    else:
        return "Could not connect to Odoo server."


@app.route("/receipts_data")
def receipts_data():
    server, uid = get_odoo_server()
    if server and uid:
        picking_data = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "stock.picking",
            "search_read",
            ["picking_type_id" == 1],
            {"fields": ["name", "picking_type_id"], "context": {}},
        )

        if picking_data:
            picking_info = ""
            for picking in picking_data:
                if "picking_type_id" in picking:
                    picking_type_id = picking["picking_type_id"][0]
                    if picking_type_id == 1:
                        picking_info += f"Name: {picking['name']}<br>"
                        picking_info += f"Picking Type ID: {picking_type_id}<br>"
            return picking_info
        else:
            return "No stock pickings found."
    else:
        return "Could not connect to Odoo server."


@app.route("/get-account")
def get_account():
    server, uid = get_odoo_server()
    if server and uid:
        user_data = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "res.users",
            "search_read",
            [],
            {"fields": ["name"], "context": {}},
        )
        if user_data:
            user_info = ""
            for user in user_data:
                user_info += f"Name: {user['name']}<br>"
                user_info += "-------<br>"
            return user_info
        else:
            return "No user data found."
    else:
        return "Could not connect to Odoo server."


def simulate_odoo_authentication(username, password):
    if username == "valid_user":
        return {"name": "Valid User"}
    else:
        return None


def authenticate_against_odoo(username):
    server, uid = get_odoo_server()

    if server and uid:
        authenticated_user = server.execute_kw(
            os.environ.get("ODOO_DB"),
            uid,
            os.environ.get("ODOO_PASSWORD"),
            "res.users",
            "search_read",
            [["name", "=", username]],
            {"fields": ["name"]},
        )

        if authenticated_user:
            return {"name": authenticated_user[0]["name"]}
    return None


@app.route("/login2", methods=["POST"])
def login2():
    odoo_url = os.environ.get("ODOO_URL")
    odoo_db = os.environ.get("ODOO_DB")
    odoo_username = os.environ.get("ODOO_USERNAME")
    odoo_password = os.environ.get("ODOO_PASSWORD")

    if not all([odoo_url, odoo_db, odoo_username, odoo_password]):
        return "<p>Environment variables not set</p>"

    common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
    uid = common.authenticate(odoo_db, odoo_username, odoo_password, {})

    if uid:
        session["uid"] = uid
        session["email"] = request.json.get("email")
        models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")

        user_data = models.execute_kw(
            odoo_db,
            uid,
            odoo_password,
            "res.users",
            "search_read",
            [[["id", "=", uid]]],
            {
                "fields": ["name"],
            },
        )

        if user_data:
            return f"Logged in as: {user_data[0]['name']}"
        else:
            return "User data not found"
    else:
        return "<p>Login failed</p>"


if __name__ == "__main__":
    app.run()
