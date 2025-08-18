#  Cold Email Generator using LLMs & Portfolio Matcher

This is a Streamlit-based app that allows you to **generate personalized cold emails** by:
- Scraping job descriptions from public job listing URLs
- Extracting role, skills, experience from the description using an LLM (Groq + Llama 3)
- Matching extracted skills with your **project portfolio** stored locally (CSV + ChromaDB)
- Generating a tailored cold email that you can copy-paste or customize

---

##  Features

1. **End-to-End Automation** from URL input to cold email output.
2. **LLM-Powered Extraction**: Uses `langchain_groq` with Llama 3 to parse job listings.
3. **Skill Matching with Portfolio**: Uses ChromaDB as a lightweight vector store to find projects matching required skills.
4. **Personalized Email Generator**: Creates custom emails tailored to each job with project links embedded.
5. **Clean UI**: Built with Streamlit, single-page intuitive interface.

---

##  How it Works

1. **User Inputs a Job URL** (e.g. Amazon/Google career page).
2. **Web Scraping** is done using `WebBaseLoader`.
3. The content is cleaned and passed to a **Groq-hosted LLM**, which extracts:
   - Role
   - Required Skills
   - Description
   - Experience
4. The extracted **skills are searched in your portfolio** using ChromaDB.
5. A **cold email is generated**, referencing the job role and matching projects from your portfolio.
6. The email is displayed and ready to copy!

---

##  Setup Instructions (Local)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/cold-email-generator.git
cd cold-email-generator
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate it (Windows)
venv\Scripts\activate

# OR (macOS/Linux)
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Groq API Key

Create a `.env` file in the root directory and add your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> Get your key from: https://console.groq.com

### 5. Run the Streamlit app

```bash
streamlit run main.py
```

---

##  Folder Structure

```
cold-email-generator/
├── .devcontainer/
├── resources/
│   └── my_portfolio.csv       # Portfolio CSV file
├── chains.py                  # LLM chaining logic
├── main.py                    # Streamlit UI logic
├── portfolio.py               # Portfolio vector store + query logic
├── utils.py                   # Helper cleaning and utilities
├── .env                       # (create manually)
├── .gitignore
├── requirements.txt
└── README.md
```

---

##  Portfolio CSV Format

Make sure your `my_portfolio.csv` inside `resources/` looks like this:

| Project | Description | Techstack | Link |
|---------|-------------|-----------|------|
| Cold Email Generator | Built using LangChain and Groq | LangChain, Groq, Streamlit | https://github.com/... |

---

##  Example Flow

1. Paste a job URL like  
   `https://www.amazon.jobs/en/jobs/2884156/2025-graduate-software-dev-engineer`
2. App scrapes job data → extracts info using LLM → matches with your projects → generates email.
3. You get a personalized cold email in seconds!

---

##  Credits

Built with ❤️ using:
- [Streamlit](https://streamlit.io/)
- [LangChain](https://www.langchain.com/)
- [Groq API](https://console.groq.com)
- [ChromaDB](https://www.trychroma.com/)

Made with 💡 by Mohan at AtliQ.
