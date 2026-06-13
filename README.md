# NayePankh AI Volunteer Assistant

An AI-powered Streamlit assistant for students and volunteers exploring NayePankh Foundation internship opportunities. The project demonstrates AI agent development, Gemini LLM integration, session memory, prompt engineering, and a practical NGO use case.

## Project Overview

The assistant answers internship and volunteering questions using a local knowledge base. It can also recommend suitable internship roles based on the candidate's skills and interests.

Built for an AI Agent Development Internship submission.

## Features

- AI chat assistant for internship FAQs
- Google Gemini 2.5 Flash integration
- Knowledge-base grounded answers
- Internship role recommendations
- Session memory with `st.session_state`
- ChatGPT-like Streamlit chat interface
- Professional sidebar with program details and interactive roles
- Bonus role recommendation form
- Streamlit Cloud compatible configuration
- Environment variable based API key handling

## Tech Stack

- Frontend: Streamlit
- Backend: Python
- LLM: Google Gemini 2.5 Flash
- Storage: Streamlit Session State
- Deployment: Streamlit Cloud

## Folder Structure

```text
naye-pankh-ai-agent/
|-- app.py
|-- knowledge_base.txt
|-- requirements.txt
|-- README.md
|-- .env.example
`-- assets/
```

## Installation

Clone or open the project folder, then install dependencies:

```bash
pip install -r requirements.txt
```

## Setup

Create a local `.env` file from the example:

```bash
cp .env.example .env
```

Add your Gemini API key:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Never commit real API keys.

## Running Locally

From inside the project directory:

```bash
streamlit run app.py
```

Then open the local URL shown by Streamlit.

## How It Works

1. The app loads internship information from `knowledge_base.txt`.
2. User and assistant messages are stored in `st.session_state`.
3. Each Gemini call receives the knowledge base, recent chat history, and the latest user prompt.
4. The assistant responds professionally and avoids inventing information outside the knowledge base.
5. The role recommender uses Gemini, with a local keyword fallback if Gemini is unavailable.
6. Sidebar role buttons add instant role-specific guidance to the chat.

## Deployment Steps

### Streamlit Cloud

1. Push this project to a GitHub repository.
2. Go to Streamlit Cloud.
3. Create a new app and select the repository.
4. Set the main file path to:

```text
app.py
```

5. Add the following secret in Streamlit Cloud settings:

```toml
GEMINI_API_KEY = "your_gemini_api_key_here"
```

6. Deploy the app.

## Screenshots

### Home and Role Recommendation Form

![Home and role recommendation form](assets/screenshot-home-role-form.png)

### Interactive Sidebar Role Details

![Full Stack Development role details](assets/screenshot-full-stack-role.png)

### Chat History With Role Response

![Chat history with role response](assets/screenshot-chat-role-response.png)

### Complete Sidebar Role List

![Complete sidebar role list](assets/screenshot-sidebar-role-list.png)

## Example Questions

- What internships are available?
- How long is the internship?
- Is it paid?
- Who can apply?
- What certificates are provided?
- I know Python, Machine Learning, SQL and FastAPI. Which role is best for me?

## Future Improvements

- Add persistent database storage for long-term volunteer history
- Add admin dashboard for managing internship roles
- Add document upload for resume-based recommendations
- Add multilingual support
- Add analytics for frequently asked questions
- Add official application link integration

## Notes

This project uses the knowledge base as the source of truth. If a question asks for details not present in the knowledge base, the assistant should recommend contacting the official NayePankh Foundation team.
