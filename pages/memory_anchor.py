import streamlit as st 
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


inp = st.text_input("Input word")
but = st.button("create")

if but:
    prompt = "using the the word "+str(inp)+" Generate a list of MAWs for a given set of words by dividing them into syllables based on vowel sounds, and then combining them. Additionally, allow for variations in the placement of vowels within each syllable"
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.56,
        max_tokens=2066,
        top_p=1,
        frequency_penalty=0.35,
        presence_penalty=0
    )
    out= response.choices[0].text
    st.write(out)
    st.stop()