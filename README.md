# Transactional-Assistant-using-GroqLLM
BankMitra is a smart assistant built with 'FastAPI' and 'Groq LLM' that helps users perform basic banking operations via natural language.

## 🚀 Features
- 🆕 Create account  
- ✅ Check balance  
- ➕ Credit money  
- ➖ Debit money (with PIN)  
- 🧾 Pay insurance  
- 📄 View transaction history  
- 📢 Register complaints  

## 🛠 Tech Stack
- Python 3, FastAPI, Groq LLM API
- JSON for lightweight storage

## ▶️ Run Locally

```bash
git clone https://github.com/yourusername/bankmitra.git
cd bankmitra
pip install -r requirements.txt
```

Add your Groq API key in .env:
```ini
GROQ_API_KEY=your_api_key
```

Start the server:
```bash
uvicorn main:app --reload
```

🧾 Sample Request
```json

POST /customer-service/invoke

{
  "input": "Please credit 500 to my account number 123123"
}
```

