from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)
application = app  # IMPORTANT for Azure

# Home page (Upload page)
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


# Analyze route
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        # Get uploaded files
        inventory_file = request.files.get('inventory')
        incident_file = request.files.get('incident')

        if not inventory_file or not incident_file:
            return "Please upload both files"

        # Read Excel files
        inv = pd.read_excel(inventory_file)
        inc = pd.read_excel(incident_file)

        # -------------------------
        # METRICS CALCULATION
        # -------------------------

        inventory_count = len(inv)
        incident_count = len(inc)

        # Safe column handling
        top_os_sub = (
            inv['operating_system_subcategory'].value_counts().idxmax()
            if 'operating_system_subcategory' in inv else "N/A"
        )

        top_os_name = (
            inv['operating_system_name'].value_counts().idxmax()
            if 'operating_system_name' in inv else "N/A"
        )

        priority_counts = (
            inc['priority'].value_counts().to_dict()
            if 'priority' in inc else {}
        )

        top_hosts = (
            inc['hostname'].value_counts().head(10).to_dict()
            if 'hostname' in inc else {}
        )

        resolution_percent = (
            (inc['resolution_code'].value_counts(normalize=True) * 100).round(2).to_dict()
            if 'resolution_code' in inc else {}
        )

        os_percent = (
            (inc['os_type'].value_counts(normalize=True) * 100).round(2).to_dict()
            if 'os_type' in inc else {}
        )

        # Extract top words from summary
        if 'summary' in inc:
            top_categories = (
                inc['summary']
                .astype(str)
                .str.split()
                .explode()
                .value_counts()
                .head(10)
                .to_dict()
            )
        else:
            top_categories = {}

        # -------------------------
        # SEND TO UI
        # -------------------------

        return render_template(
            "result.html",
            inventory_count=inventory_count,
            incident_count=incident_count,
            top_os_sub=top_os_sub,
            top_os_name=top_os_name,
            priority_counts=priority_counts,
            top_hosts=top_hosts,
            resolution_percent=resolution_percent,
            os_percent=os_percent,
            top_categories=top_categories
        )

    except Exception as e:
        return f"Error occurred: {str(e)}"


# Run locally
if __name__ == "__main__":
    app.run(debug=True)