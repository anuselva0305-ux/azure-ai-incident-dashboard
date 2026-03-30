from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    inventory_file = request.files['inventory']
    incident_file = request.files['incident']

    inv = pd.read_excel(inventory_file)
    inc = pd.read_excel(incident_file)

    # Metrics
    inventory_count = len(inv)
    incident_count = len(inc)

    top_os_sub = inv['operating_system_subcategory'].value_counts().idxmax()
    top_os_name = inv['operating_system_name'].value_counts().idxmax()

    priority_counts = inc['priority'].value_counts().to_dict()
    top_hosts = inc['hostname'].value_counts().head(10).to_dict()

    resolution_percent = (inc['resolution_code'].value_counts(normalize=True) * 100).to_dict()
    os_percent = (inc['os_type'].value_counts(normalize=True) * 100).to_dict()

    # simple keyword extraction
    top_categories = inc['summary'].str.split().explode().value_counts().head(10).to_dict()

    return render_template("result.html",
                           inventory_count=inventory_count,
                           incident_count=incident_count,
                           top_os_sub=top_os_sub,
                           top_os_name=top_os_name,
                           priority_counts=priority_counts,
                           top_hosts=top_hosts,
                           resolution_percent=resolution_percent,
                           os_percent=os_percent,
                           top_categories=top_categories)


application = app

if __name__ == "__main__":
    app.run()