import streamlit as st
import requests

st.set_page_config(
    page_title="SchoolOps AI",
    page_icon="🏫",
    layout="centered"
)

try:
    OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    st.error("API key not found. Add OPENROUTER_API_KEY to your Streamlit secrets.")
    st.stop()

def generate(prompt: str) -> str:
    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "google/gemini-2.0-flash-exp:free",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        data = response.json()
        if "choices" not in data:
            return f"API error: {data}"
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Something went wrong: {e}"

st.sidebar.title("SchoolOps AI")
st.sidebar.caption("Free AI tools for educators")
tool = st.sidebar.radio(
    "Choose a tool",
    ["Parent Email Generator", "Staff Announcement Writer", "Meeting Notes Summarizer"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.markdown("Built by a student. 100% free.")
feedback_url = "https://forms.gle/your-form-link-here"
st.sidebar.markdown(f"[Give feedback]({feedback_url})")

if tool == "Parent Email Generator":
    st.title("Parent Email Generator")
    st.caption("Generate professional parent emails in seconds.")

    situation = st.selectbox("Situation type", [
        "Student missing assignments",
        "Behavioral concern",
        "Attendance / tardiness",
        "Positive achievement",
        "Upcoming event or field trip",
        "Schedule change",
        "Request for a meeting",
        "Other (describe below)",
    ])

    tone = st.radio("Tone", ["Warm and supportive", "Neutral and professional", "Firm but respectful"], horizontal=True)

    context = st.text_area(
        "Additional context (optional)",
        placeholder="e.g. Student name is Alex, missed 3 homework assignments this week, first time this has happened.",
        height=100
    )

    if st.button("Generate email", type="primary"):
        with st.spinner("Writing..."):
            prompt = f"""You are an experienced school administrator helping a teacher write a professional parent email.

Situation: {situation}
Tone: {tone}
Additional context: {context if context else "None provided"}

Write a complete, ready-to-send parent email. Include:
- A clear subject line (prefix with "Subject: ")
- A greeting (use "Dear Parent/Guardian," if no name given)
- A clear, concise body (2-3 short paragraphs max)
- A professional sign-off with a placeholder for the teacher's name

Do not add any preamble or explanation — just the email itself."""

            result = generate(prompt)

        st.markdown("---")
        st.subheader("Your email")
        st.text_area("", value=result, height=300, label_visibility="collapsed")
        st.caption("Copy the text above and paste it into your email client.")

elif tool == "Staff Announcement Writer":
    st.title("Staff Announcement Writer")
    st.caption("Turn bullet points into a clean, professional announcement.")

    announcement_type = st.selectbox("Announcement type", [
        "All-staff memo",
        "Department update",
        "Policy or procedure change",
        "Upcoming event reminder",
        "Emergency or urgent notice",
        "Recognition / positive news",
    ])

    key_info = st.text_area(
        "Key information to include",
        placeholder="e.g. Professional development day is Friday May 30. School closes at 12pm. All staff must attend the afternoon session in the gym. Lunch will be provided.",
        height=120
    )

    audience = st.text_input("Who is this for?", placeholder="e.g. All teachers, Math department, Support staff")

    if st.button("Generate announcement", type="primary"):
        if not key_info.strip():
            st.warning("Please enter the key information to include.")
        else:
            with st.spinner("Writing..."):
                prompt = f"""You are a school principal writing a staff announcement.

Type: {announcement_type}
Audience: {audience if audience else "All staff"}
Key information: {key_info}

Write a complete, professional staff announcement. It should be:
- Clear and easy to skim
- Appropriately formal but not stiff
- Organized with any important dates or actions clearly visible
- Concise (under 200 words unless the content requires more)

Do not add any preamble — just the announcement itself."""

                result = generate(prompt)

            st.markdown("---")
            st.subheader("Your announcement")
            st.text_area("", value=result, height=300, label_visibility="collapsed")
            st.caption("Copy the text above to use in your email or bulletin.")

elif tool == "Meeting Notes Summarizer":
    st.title("Meeting Notes Summarizer")
    st.caption("Paste raw meeting notes and get a clean structured summary.")

    raw_notes = st.text_area(
        "Paste your meeting notes here",
        placeholder="Paste anything — bullet points, stream of consciousness, partial sentences. The messier the better.",
        height=250
    )

    include_actions = st.checkbox("Include action items section", value=True)
    include_decisions = st.checkbox("Include key decisions section", value=True)

    if st.button("Summarize notes", type="primary"):
        if not raw_notes.strip():
            st.warning("Please paste your meeting notes first.")
        else:
            with st.spinner("Summarizing..."):
                sections = []
                if include_actions:
                    sections.append("- Action items (who does what by when, if mentioned)")
                if include_decisions:
                    sections.append("- Key decisions made")

                prompt = f"""You are an assistant helping a school administrator clean up meeting notes.

Raw notes:
{raw_notes}

Write a clean, structured meeting summary. Always include:
- A brief overview (2-3 sentences)
- Main discussion points (as short bullets)
{chr(10).join(sections)}

Be concise. Only include what's actually in the notes — do not invent details.
Do not add any preamble — just the summary itself."""

                result = generate(prompt)

            st.markdown("---")
            st.subheader("Your summary")
            st.text_area("", value=result, height=350, label_visibility="collapsed")
            st.caption("Copy and paste into your meeting record or send to attendees.")
