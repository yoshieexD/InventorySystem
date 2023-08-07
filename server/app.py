from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
import xmlrpc.client

app = Flask(__name__)
CORS(app)


url = "http://localhost:8069"
db = "admin"
username = "admin@admin.com"
password = "admin"


def get_odoo_server():
    common = xmlrpc.client.ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, password, {})

    if uid:
        return xmlrpc.client.ServerProxy(
            f"{url}/xmlrpc/2/object", allow_none=True
        ), int(uid)

    return None, None


@app.route("/")
def home():
    return "Hello World, from Flask! Odoo is connected."


@app.route("/list_partners")
def list_partners():
    server, uid = get_odoo_server()
    if server and uid:
        partner_ids = server.execute_kw(
            db,
            uid,
            password,
            "res.partner",
            "search",
            [[]],
        )

        if not partner_ids:
            return "No partners found."
        else:
            partner_data = server.execute_kw(
                db,
                uid,
                password,
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


if __name__ == "__main__":
    app.run()
