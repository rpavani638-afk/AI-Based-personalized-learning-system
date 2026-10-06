import streamlit as st
import pandas as pd
from langchain_ollama import ChatOllama

st.set_page_config(
    page_title="AI Personalized Learning System",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI-Based Personalized Learning System")

st.write(
    "An AI system that creates a personalized learning plan "
    "based on student performance."
)

st.divider()


@st.cache_resource
def load_llm():
    return ChatOllama(
        model="llama3.2:3b",
        temperature=0.2,
        num_predict=500
    )


st.header("👨‍🎓 Student Profile")

col1, col2 = st.columns(2)

with col1:
    student_name = st.text_input(
        "Student Name",
        placeholder="Enter your name"
    )

    subject = st.selectbox(
        "Subject",
        [
            "Python Programming",
            "Data Structures",
            "Machine Learning",
            "Artificial Intelligence",
            "Database Management",
            "Computer Networks"
        ]
    )

    level = st.selectbox(
        "Learning Level",
        ["Beginner", "Intermediate", "Advanced"]
    )

with col2:
    weak_topic = st.text_input(
        "Difficult Topic",
        placeholder="Example: Python loops"
    )

    strong_topic = st.text_input(
        "Strong Topic",
        placeholder="Example: Python variables"
    )

    study_time = st.slider(
        "Available Study Time (minutes)",
        15,
        180,
        60,
        15
    )


st.divider()

st.header("📊 Learning Performance")

col1, col2, col3 = st.columns(3)

with col1:
    quiz_score = st.slider(
        "Latest Quiz Score (%)",
        0,
        100,
        50
    )

with col2:
    confidence = st.slider(
        "Confidence Level (%)",
        0,
        100,
        50
    )

with col3:
    previous_attempts = st.number_input(
        "Previous Attempts",
        0,
        20,
        1
    )


def analyze_performance(score):

    if score < 40:
        return "Needs significant improvement"
    elif score < 60:
        return "Needs improvement"
    elif score < 80:
        return "Good"
    else:
        return "Excellent"


def generate_learning_plan():

    performance = analyze_performance(quiz_score)

    prompt = f"""
You are an AI personalized learning assistant.

Student: {student_name}
Subject: {subject}
Level: {level}

Weak topic: {weak_topic}
Strong topic: {strong_topic}

Quiz score: {quiz_score}%
Confidence: {confidence}%
Previous attempts: {previous_attempts}
Study time: {study_time} minutes

Performance: {performance}

Create a short personalized learning plan.

Include:

1. Learning Diagnosis
2. Personalized Explanation
3. Simple Example
4. Practice Questions
5. Learning Strategy
6. Recommended Next Topic
7. Study Schedule

Keep the answer concise and easy to understand.
"""

    llm = load_llm()

    response = llm.invoke(prompt)

    return response.content


st.divider()

if st.button(
    "🚀 Generate Personalized Learning Plan",
    type="primary",
    use_container_width=True
):

    if not student_name.strip():
        st.warning("Please enter the student's name.")

    elif not weak_topic.strip():
        st.warning("Please enter the difficult topic.")

    else:

        with st.spinner("🤖 AI is creating your learning plan..."):

            try:

                result = generate_learning_plan()

                st.success(
                    "Personalized learning plan generated!"
                )

                st.header("📚 Your Learning Plan")

                st.markdown(result)

            except Exception as error:

                st.error(
                    "Could not connect to Ollama."
                )

                st.code(str(error))


st.divider()

st.header("📈 Performance Summary")

performance = analyze_performance(quiz_score)

summary = pd.DataFrame({
    "Metric": [
        "Subject",
        "Learning Level",
        "Quiz Score",
        "Confidence",
        "Performance",
        "Previous Attempts"
    ],
    "Value": [
        subject,
        level,
        f"{quiz_score}%",
        f"{confidence}%",
        performance,
        previous_attempts
    ]
})

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True
)