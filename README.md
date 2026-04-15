# 🚀 Creatix Lab · AI Research Assistant

Creatix Lab is an **AI-powered research assistant** that automates the process of gathering, analyzing, and generating structured reports from web data using advanced AI techniques.

It combines **web search, content extraction, and language models** to provide high-quality research outputs in seconds.

---

## 🔥 Features & Their Importance

### 🔎 Smart Web Search (Search Agent)

Fetches relevant information from the internet using an AI-powered search API.

👉 **Why important?**
Traditional search gives links, but this directly retrieves useful content, saving time and improving research efficiency.

---

### 📄 Content Extraction (Reader Agent)

Extracts meaningful text from URLs and web pages.

👉 **Why important?**
Raw web pages contain noise (ads, scripts). This feature ensures only useful content is processed.

---

### ✍️ AI Report Generation (Writer Agent)

Generates a structured research report automatically.

👉 **Why important?**
Helps users avoid manual writing and provides well-organized, professional content instantly.

---

### 🧠 Multi-Agent System

Includes:

* Search Agent
* Reader Agent
* Writer Agent
* Critic Agent

👉 **Why important?**
Instead of a single AI, multiple specialized agents improve accuracy, modularity, and scalability.

---

### 📊 Structured Output

Reports are generated in sections:

* Introduction
* Key Findings
* Conclusion
* Sources

👉 **Why important?**
Ensures clarity, readability, and professional formatting — useful for assignments and reports.

---

### 🎯 AI Critic (Evaluation System)

Evaluates the generated report and provides:

* Score
* Strengths
* Weaknesses

👉 **Why important?**
Adds a feedback loop, improving reliability and helping users understand report quality.

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **LLM:** OpenAI (GPT-4o-mini)
* **Framework:** LangChain
* **Search API:** Tavily
* **Web Scraping:** BeautifulSoup

---

## ⚙️ Installation

### 1. Clone the repository

```bash id="c9l2mq"
git clone https://github.com/your-username/Creatix.git
cd Creatix
```

### 2. Create virtual environment

```bash id="z5w1kn"
python -m venv myenv
source myenv/bin/activate   # Mac/Linux
myenv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash id="y8x2rp"
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Create a `.env` file and add:

```env id="m2k9vn"
OPENAI_API_KEY=your_openai_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

## ▶️ Run the App

```bash id="t1q8sb"
streamlit run app.py
```

---

## 📌 Project Structure

```id="h3k2vb"
Creatix/
│── app.py
│── agents.py
│── tools.py
│── database.py
│── requirements.txt
│── README.md
```

---

## 🧠 How It Works

1. User enters a topic
2. 🔎 Search Agent collects relevant data
3. 📄 Reader Agent extracts useful content
4. ✍️ Writer Agent generates structured report
5. 🎯 Critic Agent evaluates the report

---

## 🚀 Future Improvements

* 🌍 Real-time news integration
* 🧠 Advanced agent orchestration (LangGraph)
* 📄 Export reports (PDF/DOCX)
* 🎨 Enhanced UI/UX

---

## 👨‍💻 Author

**Yash Hanamghar**
Final Year IT Student | AI/ML Enthusiast

---

⭐ If you like this project, consider giving it a star!
