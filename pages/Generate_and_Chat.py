import streamlit as st
import openai
import os
import json
import base64
from streamlit_chat import message

openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(
    page_title="Quiz Generator and Quiz Mode",
    page_icon=":robot:"
)

st.header("Quiz Generator and Quiz Mode")

st.subheader("Question & Answer Generation")

topic = st.text_input("Enter topic here")
num_quest = st.slider('Number of questions to generate', 0, 4, 1)
result = st.button("Submit")

if result:
    form = """
    [
      {
        "question": "Question here?",
        "answer": "Answer here.",
        "Question": "Question here?"
      },
      { 
        "question": "Question here?",
        "answer": "Answer here.",
        "Question": "Question here?"
      }
    ]
    """

    prompt = f"generate {num_quest} short answer questions with short answers on the topic of {topic}, with the all the possible correct comprehensive answers, show the output in following json list format:\n {form}."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.56,
        max_tokens=2100,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    output = response.choices[0].text.strip()
    json_output = json.loads(output)

    if 'json_output' not in st.session_state:
        st.session_state.json_output = json_output

try:
    st.subheader("Refining section ")

    for i, item in enumerate(st.session_state.json_output):
        st.write(f"question {i+1}")
        question = st.text_input("question", item["question"], key=f"question_{i}")
        answer = st.text_area("answer", item["answer"], key=f"answer_{i}")

        st.session_state.json_output[i]["Question"] = question
        st.session_state.json_output[i]["answer"] = answer

except AttributeError:
    st.warning("Type a topic and generate some questions to refine them")

st.header("Start Quiz")
start_quiz = st.button("Start Quiz")

if start_quiz:
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0

    questions = [q['question'] for q in st.session_state.json_output]

    if st.session_state.current_question < len(questions):
        current_question = questions[st.session_state.current_question]
        message(current_question, is_user=False, key=str(st.session_state.current_question))
        user_input = st.text_input("You: ", "", key="input")

        if user_input:
            if 'past' not in st.session_state:
                st.session_state.past = []

            st.session_state.past.append(user_input)
            st.session_state.current_question += 1

        st.sidebar.header("Conversation History")
        for i, question in enumerate(questions):
            if i < st.session_state.current_question:
                st.sidebar.write(question)
                st.sidebar.write("You: " + st.session_state.past[i])

    else:
        responses = []
        for i, question in enumerate(questions):
            response = {
                "question": question,
                "response": st.session_state.past[i]
            }
            responses.append(response)

        # with open("responses.json", "w") as outfile:

        #     json.dump(responses, outfile)

        message("Thank you for answering all the questions. Your responses have been saved.", is_user=False)
        st.sidebar.write("Thank you for answering all the questions. Your responses have been saved.")

        st.sidebar.download_button(
            label="Download Responses",
            data=json.dumps(responses),
            file_name="responses.json",
            mime="application/json"
        )

        if 'generated' in st.session_state:
            for i in range(len(st.session_state.generated) - 1, -1, -1):
                message(st.session_state.generated[i], key=str(i))
                message(st.session_state.past[i], is_user=True, key=str(i) + '_user')
                st.sidebar.write("Bot: ", st.session_state.generated[i])
