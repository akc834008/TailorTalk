# 📅 TailorTalk - AI Calendar Booking Assistant

TailorTalk is an AI-powered appointment scheduling assistant that uses **FastAPI**, **LangChain**, **Mistral**, and **Google Calendar API** to automatically understand and book meetings from natural language input.

---

## 🚀 Features

- Conversational interface with **Streamlit** frontend
- Natural language understanding using **Mistral LLM**
- Books meetings to your **Google Calendar** using service account credentials
- Prevents double bookings with slot availability check
- Suggests next available time slot if desired time is busy

---

## 📁 Project Structure

```
tailor_talk/
├── backend/
│   ├── main.py                # FastAPI backend
│   ├── agent.py               # LangChain agent with Mistral + calendar tools
│   ├── calendar_service.py    # Google Calendar integration
│   ├── schemas.py             # Pydantic models
│
├── frontend/
│   └── app.py                 # Streamlit chatbot UI
│
├── config/
│   ├── credential.json        # 🔐 Google service account credentials (ignored)
│   └── settings.py            # Settings loader
│
├── .env                       # 🔐 Environment variables (ignored)
├── .gitignore
├── requirements.txt
├── README.md                  # ✅ You're here
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/TailorTalk.git
cd TailorTalk
```

### 2. Create & Activate Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root with:

```env
MISTRAL_API_KEY=your_mistral_api_key
GOOGLE_CALENDAR_ID=your_calendar_email@gmail.com
```

> ⚠️ Never commit `.env` or `credential.json` to GitHub.

### 5. Add Google Service Account Credentials

Place your `credential.json` file inside `config/` directory:

```
config/credential.json
```

Share your calendar with the service account's email (found inside the JSON).

---

## 💻 Running the Project

### Start Backend (FastAPI)

```bash
cd tailor_talk
venv\Scripts\activate
python -m uvicorn backend.main:app --reload --port 8000
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

### Start Frontend (Streamlit)

Open a **new terminal**:

```bash
cd tailor_talk/frontend
streamlit run app.py
```

Visit: [http://localhost:8501](http://localhost:8501)

---

## ✅ Sample Prompts

- "Book a meeting for tomorrow at 4 PM"
- "Schedule a call next Monday at 11 AM"
- "Am I free at 3 PM today?"

---

## 🛡️ Security Note

If you accidentally committed `credential.json` or `.env`, use this to remove it from Git history:

```bash
git filter-repo --path config/credential.json --invert-paths --force
```

---

## 🧠 Powered By

- [LangChain](https://github.com/langchain-ai/langchain)
- [Mistral API](https://docs.mistral.ai)
- [Google Calendar API](https://developers.google.com/calendar/api)
- [Streamlit](https://streamlit.io)
- [FastAPI](https://fastapi.tiangolo.com)

---

## 📬 Contact

Made with ❤️ by [Abhishek](mailto\:akc834008@gmail.com)

