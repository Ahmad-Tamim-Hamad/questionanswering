import streamlit as st
import requests

st.title("Question answering")

# Input field for the question
question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question.strip():
        # Send a request to the backend
        response = requests.post("http://127.0.0.1:5000/ask", json={"question": question})
        if response.status_code == 200:
            st.write("### Answer:")
            st.write(response.json()['answer'])
        else:
            st.error(f"Error: {response.json().get('error', 'Unknown error')}")
    else:
        st.warning("Please enter a valid question.")
