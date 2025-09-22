# AdventureWorks Sales Dashboard

Interactive dashboard built with **Streamlit** to visualize sales performance using the **AdventureWorks** database.  
It allows filtering by **date**, **product**, and **region**, and provides:

- 📊 Total sales value (KPI)  
- 📦 Sales by product (bar chart)  
- 🌍 Sales by region (aggregated)  
- ⏳ Sales trend over time (line chart)

---

## Live Demo

👉 [Click here to access the live dashboard](https://YOUR-LINK-HERE.streamlit.app)

---

## How to Run Locally

Clone the repository and install dependencies:

```bash
git clone https://github.com/yaracyta/adventureworks-sales-dashboard.git
cd adventureworks-sales-dashboard

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows

# Install requirements
pip install -r requirements.txt

# Run the app
streamlit run dashboard.py

Open in your browser :

http://localhost:8501



