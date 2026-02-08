# 🛡️ FinSage: AI-Powered Financial Intelligence

**FinSage** is a context-aware financial analytics platform that transforms static data into actionable intelligence. By combining **Time-Series Forecasting** with **Generative AI (RAG)**, it helps users understand not just where their money went, but where it’s going.

---

## 🌟 The Vision
The goal was to move beyond simple spreadsheets. FinSage creates a **"living conversation"** with data, allowing users to filter through 32,000+ records and receive instant, personalized coaching from an AI that actually understands the numbers on the screen.

---

## 🚀 Key Features

* **Context-Aware AI Analyst:** Uses a **Dynamic RAG (Retrieval-Augmented Generation)** pipeline. The AI doesn't give generic advice; it reads your active UI filters (Region, Education, Credit Score) to provide specific insights.
* **Predictive Forecasting:** Features an integrated **ARIMA(1, 1, 1)** model that analyzes historical spending to project future expenses, helping users stay ahead of inflation and price shifts.
* **Interactive Data Engine:** A high-performance dashboard capable of processing **32,424 records** with real-time KPI updates and multi-dimensional filtering.
* **Professional Reporting:** One-click **PDF Report Generation** that packages your data session, AI analysis, and dashboard stats into a clean, shareable document.

---

## 🛠️ Technical Stack

| Category | Technology |
| :--- | :--- |
| **AI Engine** | Google Gemini 1.5 Flash (Dynamic Prompting) |
| **Frontend** | Streamlit |
| **Data Analysis** | Pandas, NumPy |
| **Forecasting** | Statsmodels (ARIMA) |
| **PDF Engine** | FPDF |

---

## 🧠 How It Works

1.  **Filter:** Users select specific segments (e.g., "Post-grads in Asia with High Credit Scores").
2.  **Analyze:** The app calculates real-time metrics and feeds this "filtered truth" to the AI.
3.  **Consult:** Users chat with FinSage to uncover hidden trends or get a personal financial roadmap.
4.  **Export:** Findings are exported to a PDF for a permanent audit trail.

---



## 🔧 Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yourusername/FinSage-AI.git](https://github.com/yourusername/FinSage-AI.git)