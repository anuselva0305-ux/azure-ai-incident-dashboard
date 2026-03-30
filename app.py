from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
application = app  # REQUIRED for Azure

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    try:
        inventory_file = request.files['inventory']
        incident_file = request.files['incident']

        inv = pd.read_excel(inventory_file)
        inc = pd.read_excel(incident_file)

        # ---------------- METRICS ----------------
        inventory_count = len(inv)
        incident_count = len(inc)

        # Inventory insights
        top_os_sub = (
            inv['operating_system_subcategory'].value_counts().idxmax()
            if 'operating_system_subcategory' in inv else "N/A"
        )

        top_os_name = (
            inv['operating_system_name'].value_counts().idxmax()
            if 'operating_system_name' in inv else "N/A"
        )

        # Incident charts
        priority_counts = (
            inc['priority'].value_counts().to_dict()
            if 'priority' in inc else {}
        )

        top_hosts = (
            inc['hostname'].value_counts().head(10).to_dict()
            if 'hostname' in inc else {}
        )

        resolution_percent = (
            (inc['resolution_code'].value_counts(normalize=True) * 100)
            .round(2).to_dict()
            if 'resolution_code' in inc else {}
        )

        os_percent = (
            (inc['os_type'].value_counts(normalize=True) * 100)
            .round(2).to_dict()
            if 'os_type' in inc else {}
        )

        # Top categories from summary
        if 'summary' in inc:
            text = " ".join(inc['summary'].dropna().astype(str))
            words = pd.Series(text.lower().split())
            top_categories = words.value_counts().head(10).to_dict()
        else:
            top_categories = {}

        return render_template(
            'result.html',
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
        return f"Error: {str(e)}"


if __name__ == '__main__':
    app.run(debug=True)