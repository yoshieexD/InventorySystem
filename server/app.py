from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import xmlrpc.client
import jwt
import datetime
from urllib.parse import urlparse, parse_qs

app = Flask(__name__)
CORS(app)
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
            return "No picking types found."
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
                picking_type_info = ""
                for picking_type in picking_type_data:
                    picking_type_info += f"ID: {picking_type['id']}<br>"
                    picking_type_info += f"Name: {picking_type['name']}<br>"
                    picking_type_info += f"Code: {picking_type['code']}<br>"
                    picking_type_info += f"Sequence: {picking_type['sequence']}<br>"
                    picking_type_info += "-------<br>"
                return picking_type_info
            else:
                return "Failed to retrieve picking type data."
    else:
        return "Could not connect to Odoo server."


if __name__ == "__main__":
    app.run()
