import streamlit as st
import requests

st.set_page_config(page_title="Question Answering with LangChain + FastAPI")
st.title("Ask Me Anything")

# Input field
question = st.text_input("Enter your question:")

if st.button("Ask"):
    if question.strip():
        try:
            # Send to FastAPI backend
            response = requests.post(
                "http://127.0.0.1:8000/ask",
                json={"question": question}
            )
            if response.status_code == 200:
                st.success("Answer:")
                st.write(response.json()["answer"])
            else:
                st.error(f"Error: {response.json().get('answer')}")
        except Exception as e:
            st.error(f"Failed to connect to backend: {e}")
    else:
        st.warning("Please enter a valid question.")
