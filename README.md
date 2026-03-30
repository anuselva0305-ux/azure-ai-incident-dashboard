# 🚀 Azure AI Incident Dashboard

An executive-level dashboard built using **Flask + Pandas + Chart.js**, deployed on **Microsoft Azure App Service**.

---

## 📊 Features

- Upload Inventory & Incident Excel files
- Auto-detect columns dynamically
- Executive dashboard with:
  - Total Inventory Count
  - Total Incident Count
  - Top OS Subcategory
  - Top OS Name
- Visual insights:
  - Priority distribution (Bar Chart)
  - Top 10 Hosts (Bar Chart)
  - Resolution Code % (Pie Chart)
  - OS Type % (Doughnut Chart)

---

## 🧠 Tech Stack

- Python (Flask)
- Pandas
- Chart.js
- HTML/CSS
- Azure App Service (Deployment)
- GitHub (CI/CD)

---

## 📂 Project Structure
azure-ai-incident-dashboard/
│
├── app.py
├── requirements.txt
├── templates/
│ ├── index.html
│ └── result.html
├── static/
└── README.md


---

## ⚙️ Setup (Local)

```bash
git clone https://github.com/anuselva0305-ux/azure-ai-incident-dashboard.git
cd azure-ai-incident-dashboard

pip install -r requirements.txt
python app.py

http://127.0.0.1:5000

☁️ Azure Deployment
Create an Azure App Service
Go to Deployment Center
Connect your GitHub repository
Select branch: main
Azure will auto-deploy your app

🌐 Live Application
👉 https://anitha-ai-dashboard-h0fjcudsc6g3akgw.centralindia-01.azurewebsites.net/

