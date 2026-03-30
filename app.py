from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route("/")
def home():
    data = pd.read_csv("data/incidents.csv")

    total = len(data)
    top_category = data['category'].value_counts().idxmax()

    # Simple AI Insight
    if total > 3:
        insight = "High incident volume detected"
    else:
        insight = "Incident levels normal"

    return render_template("index.html",
                           total=total,
                           top=top_category,
                           insight=insight)

if __name__ == "__main__":
    app.run(debug=True)