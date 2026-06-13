import os
from pathlib import Path
from typing import Dict, List

import streamlit as st
from dotenv import load_dotenv

try:
    from google import genai
    from google.genai import types
except ImportError:  # pragma: no cover - shown as a runtime setup hint in Streamlit
    genai = None
    types = None


APP_TITLE = "NayePankh AI Volunteer Assistant"
MODEL_NAME = "gemini-2.5-flash"
BASE_DIR = Path(__file__).parent
KNOWLEDGE_BASE_PATH = BASE_DIR / "knowledge_base.txt"


AVAILABLE_ROLES = [
    "Full Stack Development",
    "Front End Development",
    "Web Development",
    "Artificial Intelligence",
    "Data Analytics",
    "Java Development",
    "Python Development",
    "Machine Learning",
    "Backend Development",
    "UI/UX Design",
    "AI Agent Development",
    "No Code Development",
    "Mobile App Development",
    "WordPress Development",
    "AI Web Development",
]


ROLE_KEYWORDS: Dict[str, List[str]] = {
    "AI Agent Development": ["agent", "llm", "gemini", "openai", "rag", "prompt", "langchain"],
    "Artificial Intelligence": ["ai", "artificial intelligence", "deep learning", "nlp", "computer vision"],
    "Machine Learning": ["machine learning", "ml", "model", "sklearn", "pandas", "numpy"],
    "Python Development": ["python", "fastapi", "django", "flask", "automation"],
    "Backend Development": ["backend", "api", "fastapi", "django", "database", "sql", "mongodb"],
    "Data Analytics": ["data", "analytics", "sql", "excel", "power bi", "tableau", "dashboard"],
    "Full Stack Development": ["full stack", "react", "node", "frontend", "backend", "api"],
    "Front End Development": ["frontend", "front end", "react", "html", "css", "javascript", "typescript"],
    "Web Development": ["web", "html", "css", "javascript", "react", "website"],
    "UI/UX Design": ["ui", "ux", "figma", "design", "wireframe", "prototype"],
    "Mobile App Development": ["mobile", "android", "ios", "flutter", "react native", "kotlin"],
    "Java Development": ["java", "spring", "spring boot", "oops"],
    "WordPress Development": ["wordpress", "cms", "elementor", "php"],
    "No Code Development": ["no code", "nocode", "bubble", "webflow", "zapier"],
    "AI Web Development": ["ai web", "ai app", "llm", "streamlit", "web", "chatbot"],
}


ROLE_DESCRIPTIONS: Dict[str, str] = {
    "Full Stack Development": "build complete web features across frontend, backend, and APIs",
    "Front End Development": "create responsive user interfaces with HTML, CSS, JavaScript, or React",
    "Web Development": "design and develop websites and practical web applications",
    "Artificial Intelligence": "work on AI concepts, intelligent features, and applied AI use cases",
    "Data Analytics": "analyze data, create reports, and build dashboards using tools like SQL or Excel",
    "Java Development": "develop Java-based applications using OOP and backend fundamentals",
    "Python Development": "build scripts, automation, APIs, and backend utilities using Python",
    "Machine Learning": "work on data preprocessing, model training, evaluation, and ML projects",
    "Backend Development": "create APIs, database flows, and server-side application logic",
    "UI/UX Design": "design user flows, wireframes, prototypes, and clean product experiences",
    "AI Agent Development": "build chatbot and agent workflows using LLMs, prompts, memory, and APIs",
    "No Code Development": "create functional tools using no-code automation and app builder platforms",
    "Mobile App Development": "build mobile app screens and features for Android, iOS, or cross-platform apps",
    "WordPress Development": "create and customize CMS websites with WordPress themes and plugins",
    "AI Web Development": "combine AI features with web applications and interactive user interfaces",
}


def load_api_key() -> str:
    """Load Gemini API key from Streamlit secrets, environment, or a local .env file."""
    load_dotenv()
    try:
        return st.secrets.get("GEMINI_API_KEY", "") or os.getenv("GEMINI_API_KEY", "")
    except Exception:
        return os.getenv("GEMINI_API_KEY", "")


@st.cache_data(show_spinner=False)
def load_knowledge_base() -> str:
    if not KNOWLEDGE_BASE_PATH.exists():
        return "Knowledge base file is missing. Please add knowledge_base.txt."
    return KNOWLEDGE_BASE_PATH.read_text(encoding="utf-8")


def initialize_session_state() -> None:
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": (
                    "Hi! I am the NayePankh AI Volunteer Assistant. Ask me about internships, "
                    "volunteering, certificates, eligibility, or role recommendations."
                ),
            }
        ]


def build_system_instruction(knowledge_base: str) -> str:
    return f"""
You are the NayePankh AI Volunteer Assistant, a professional assistant for students,
freshers, and volunteers exploring NayePankh Foundation internships.

Use the knowledge base as the primary source of truth. If information is not present,
say that the official team can confirm it instead of inventing details.

Response rules:
- Be clear, warm, concise, and professional.
- Mention that the internship is unpaid when compensation is discussed.
- Recommend roles by matching user skills and interests to available roles.
- Keep the tone suitable for an NGO internship application setting.
- Do not claim the user is selected or guaranteed an internship.

Knowledge base:
{knowledge_base}
""".strip()


def get_gemini_client(api_key: str):
    if genai is None:
        raise RuntimeError("The google-genai package is not installed. Run: pip install -r requirements.txt")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY. Add it to .env locally or Streamlit secrets in deployment.")
    return genai.Client(api_key=api_key)


def format_chat_history(messages: List[Dict[str, str]]) -> str:
    recent_messages = messages[-10:]
    return "\n".join(f"{item['role'].title()}: {item['content']}" for item in recent_messages)


def generate_response(user_prompt: str, knowledge_base: str, api_key: str) -> str:
    client = get_gemini_client(api_key)
    system_instruction = build_system_instruction(knowledge_base)
    conversation_context = format_chat_history(st.session_state.messages)

    prompt = f"""
Conversation so far:
{conversation_context}

User message:
{user_prompt}
""".strip()

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.35,
                max_output_tokens=800,
            ),
        )
    except Exception as exc:
        raise RuntimeError(f"Gemini request failed: {exc}") from exc

    text = getattr(response, "text", None)
    if not text:
        return "I could not generate a response right now. Please try again in a moment."
    return text.strip()


def friendly_llm_error() -> str:
    return (
        "The AI service is temporarily busy, so I am showing a reliable knowledge-base response. "
        "Please try again shortly for a Gemini-generated answer."
    )


def build_role_overview(role: str) -> str:
    description = ROLE_DESCRIPTIONS.get(role, "explore a practical internship role at NayePankh Foundation")
    return f"""
**{role}** is a suitable NayePankh internship option if you want to {description}.

**Internship details**
- Duration: 1 month
- Mode: Remote
- Schedule: Flexible working hours
- Eligibility: Open to students and freshers
- Compensation: Unpaid internship

**Perks**
- Offer Letter
- Internship Certificate
- Appreciation Certificate
- Letter of Recommendation
- LinkedIn Recommendation

**Best next step**
Prepare 2-3 small projects or examples that show your interest in {role}, then apply with a clear summary of your skills.
""".strip()


def local_role_recommendation(skills: str, interests: str = "") -> List[str]:
    combined = f"{skills} {interests}".lower()
    scores = []

    for role, keywords in ROLE_KEYWORDS.items():
        score = sum(1 for keyword in keywords if keyword in combined)
        if score:
            scores.append((role, score))

    scores.sort(key=lambda item: item[1], reverse=True)
    return [role for role, _score in scores[:4]] or [
        "AI Agent Development",
        "Python Development",
        "Web Development",
    ]


def build_structured_recommendation(skills: str, interests: str, roles: List[str]) -> str:
    top_roles = roles[:4]
    role_lines = "\n".join(f"- **{role}**: Matches your skills and learning interests." for role in top_roles)

    return f"""
Based on your profile, the best internship role matches are:

{role_lines}

**Why these roles fit**
- Your skills: {skills.strip() or "Not provided"}
- Your interests: {interests.strip() or "Not provided"}
- These roles align with the remote, 1-month NayePankh internship format and are suitable for students and freshers.

**Recommended next step**
Prepare a short portfolio or project summary showing how you used these skills, then apply for the role that best matches your strongest area.
""".strip()


def generate_role_recommendation(skills: str, interests: str, knowledge_base: str, api_key: str) -> str:
    fallback_roles = local_role_recommendation(skills, interests)
    fallback_response = build_structured_recommendation(skills, interests, fallback_roles)
    prompt = f"""
Recommend the best NayePankh internship roles for this candidate.

Skills:
{skills}

Interests:
{interests}

Use only these role names when recommending roles:
{", ".join(fallback_roles)}

Return a complete answer in this exact structure:
Based on your profile, the best internship role matches are:
- **Role Name**: One short reason.
- **Role Name**: One short reason.

**Why these roles fit**
- Mention the candidate's skills.
- Mention the candidate's interests.
- Mention that the internship is remote and 1 month.

**Recommended next step**
One practical next step.
""".strip()

    try:
        response = generate_response(prompt, knowledge_base, api_key)
        if len(response.split()) < 35 or "recommended next step" not in response.lower():
            return fallback_response
        return response
    except RuntimeError:
        return (
            f"{fallback_response}\n\n"
            f"Note: {friendly_llm_error()}"
        )


def inject_custom_css() -> None:
    st.markdown(
        """
        <style>
            .stApp {
                background: #f8faf9;
                color: #15201b;
            }

            [data-testid="stSidebar"] {
                background: #12372a;
                color: #ffffff;
            }

            [data-testid="stSidebar"] * {
                color: #ffffff;
            }

            .hero {
                padding: 1.2rem 0 0.8rem;
                border-bottom: 1px solid #dbe5df;
                margin-bottom: 1rem;
            }

            .hero h1 {
                margin: 0;
                font-size: 2rem;
                letter-spacing: 0;
                color: #12372a;
            }

            .hero p {
                margin: 0.45rem 0 0;
                color: #4d5f56;
                max-width: 850px;
                font-size: 1rem;
            }

            .metric-list {
                display: grid;
                gap: 0.5rem;
                margin: 1rem 0;
            }

            .metric-item {
                padding: 0.65rem 0.75rem;
                border: 1px solid rgba(255,255,255,0.2);
                border-radius: 8px;
                background: rgba(255,255,255,0.08);
                font-size: 0.92rem;
            }

            .role-pill {
                margin-bottom: 0.35rem;
            }

            [data-testid="stSidebar"] .stButton button {
                width: 100%;
                justify-content: flex-start;
                min-height: 2rem;
                padding: 0.35rem 0.6rem;
                border-radius: 999px;
                border: 1px solid rgba(255,255,255,0.22);
                background: rgba(255,255,255,0.1);
                color: #ffffff;
                font-size: 0.82rem;
                line-height: 1.15;
                white-space: normal;
                text-align: left;
            }

            [data-testid="stSidebar"] .stButton button:hover {
                background: rgba(255,255,255,0.18);
                border-color: rgba(255,255,255,0.42);
                color: #ffffff;
            }

            div[data-testid="stChatMessage"] {
                border-radius: 8px;
                border: 1px solid #e0e8e3;
                background: #ffffff;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.04);
            }

            .stButton button {
                border-radius: 8px;
                border: 1px solid #0f6b4f;
                background: #0f6b4f;
                color: #ffffff;
                font-weight: 600;
            }

            .stButton button:hover {
                border-color: #0b513c;
                background: #0b513c;
                color: #ffffff;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> None:
    st.sidebar.title(APP_TITLE)
    st.sidebar.markdown(
        """
        <div class="metric-list">
            <div class="metric-item"><strong>Internship Duration:</strong> 1 Month</div>
            <div class="metric-item"><strong>Mode:</strong> Remote</div>
            <div class="metric-item"><strong>Schedule:</strong> Flexible Working Hours</div>
            <div class="metric-item"><strong>Open To:</strong> Students & Freshers</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.sidebar.subheader("Available Roles")
    for role in AVAILABLE_ROLES:
        if st.sidebar.button(role, key=f"role_{role}", use_container_width=True):
            st.session_state.messages.append({"role": "user", "content": f"Tell me about {role} internship."})
            st.session_state.messages.append({"role": "assistant", "content": build_role_overview(role)})
            st.rerun()

    st.sidebar.divider()
    if st.sidebar.button("Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()


def render_role_recommender(knowledge_base: str, api_key: str) -> None:
    with st.expander("Suggest Best Internship Role", expanded=False):
        with st.form("role_recommendation_form"):
            skills = st.text_area(
                "Skills",
                placeholder="Example: Python, Machine Learning, SQL, FastAPI",
                height=90,
            )
            interests = st.text_area(
                "Interests",
                placeholder="Example: I enjoy building AI tools and backend APIs.",
                height=90,
            )
            submitted = st.form_submit_button("Suggest Best Internship Role", use_container_width=True)

        if submitted:
            if not skills.strip() and not interests.strip():
                st.warning("Please add at least your skills or interests.")
                return

            with st.spinner("Finding the best role match..."):
                recommendation = generate_role_recommendation(skills, interests, knowledge_base, api_key)

            st.session_state.messages.append(
                {
                    "role": "user",
                    "content": f"Suggest roles for skills: {skills or 'Not provided'}; interests: {interests or 'Not provided'}",
                }
            )
            st.session_state.messages.append({"role": "assistant", "content": recommendation})
            st.rerun()


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="NP", layout="wide")
    inject_custom_css()
    initialize_session_state()

    knowledge_base = load_knowledge_base()
    api_key = load_api_key()

    render_sidebar()

    st.markdown(
        """
        <div class="hero">
            <h1>NayePankh AI Volunteer Assistant</h1>
            <p>
                Ask internship questions, explore volunteer opportunities, and get role recommendations
                based on your skills and interests.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not api_key:
        st.info("Add GEMINI_API_KEY in your .env file or Streamlit Cloud secrets to enable Gemini responses.")

    render_role_recommender(knowledge_base, api_key)

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_prompt = st.chat_input("Ask about internships, volunteering, certificates, or role recommendations...")
    if user_prompt:
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.markdown(user_prompt)

        with st.chat_message("assistant"):
            with st.spinner("Generating response..."):
                try:
                    assistant_response = generate_response(user_prompt, knowledge_base, api_key)
                except RuntimeError:
                    assistant_response = (
                        f"{friendly_llm_error()}\n\n"
                        "You can still ask about internship duration, mode, eligibility, perks, and available roles."
                    )
                st.markdown(assistant_response)

        st.session_state.messages.append({"role": "assistant", "content": assistant_response})


if __name__ == "__main__":
    main()
