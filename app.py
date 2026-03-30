from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
application = app  # Azure requirement


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

        # NORMALIZE COLUMN NAMES
        inv.columns = inv.columns.str.strip().str.lower()
        inc.columns = inc.columns.str.strip().str.lower()

        print("INVENTORY COLUMNS:", inv.columns)
        print("INCIDENT COLUMNS:", inc.columns)

        # COUNTS
        inventory_count = len(inv)
        incident_count = len(inc)

        # INVENTORY DATA
        top_os_sub = "N/A"
        top_os_name = "N/A"

        for col in inv.columns:
            if 'subcategory' in col:
                top_os_sub = inv[col].value_counts().idxmax()
            if 'operating_system' in col or 'os name' in col:
                top_os_name = inv[col].value_counts().idxmax()

        # =========================
        # INCIDENT AUTO DETECT
        # =========================
        def find_column(columns, keywords):
            for key in keywords:
                for col in columns:
                    if key in col:
                        return col
            return None

        priority_col = find_column(inc.columns, ['priority'])
        host_col = find_column(inc.columns, ['host'])
        resolution_col = find_column(inc.columns, ['resolution'])
        os_col = find_column(inc.columns, ['os'])

        print("Detected Columns:")
        print(priority_col, host_col, resolution_col, os_col)

        # =========================
        # CALCULATIONS
        # =========================

        priority_counts = (
            inc[priority_col].value_counts().to_dict()
            if priority_col else {}
        )

        top_hosts = (
            inc[host_col].value_counts().head(10).to_dict()
            if host_col else {}
        )

        resolution_percent = (
            (inc[resolution_col].value_counts(normalize=True) * 100)
            .round(2)
            .head(10)
            .to_dict()
            if resolution_col else {}
        )

        os_percent = (
            (inc[os_col].value_counts(normalize=True) * 100)
            .round(2)
            .head(10)
            .to_dict()
            if os_col else {}
        )

        return render_template(
            'result.html',
            inventory_count=inventory_count,
            incident_count=incident_count,
            top_os_sub=top_os_sub,
            top_os_name=top_os_name,
            priority_counts=priority_counts,
            top_hosts=top_hosts,
            resolution_percent=resolution_percent,
            os_percent=os_percent
        )

    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)