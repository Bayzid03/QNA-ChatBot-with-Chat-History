import streamlit as st
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash-preview-04-17")
chat = model.start_chat(history=[])

def get_response(question):
    try:
        response = chat.send_message(question, stream=True)
        return response
    except Exception as e:
        st.error(f"Error: {e}")
        return []

st.set_page_config(page_title="Q&A ChatBot")
st.header("Gemini LLM Application")

if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

user_input = st.text_input("Input: ", key="input")
submit = st.button("Ask the question")

if submit and user_input:
    response = get_response(user_input)
    st.session_state['chat_history'].append(("You", user_input))
    st.subheader("The Response is")
    full_response = ""
    for chunk in response:
        st.write(chunk.text)
        full_response += chunk.text
    st.session_state['chat_history'].append(("Bot", full_response))

st.subheader("The Chat History is")
for role, text in st.session_state['chat_history']:
    st.write(f"{role}: {text}")


## stream= True : It send back response in chunks as soon as they're generated, rather than waiting for the entire text.(Display Text in Real Time)
##                Which make the Interaction more Dynamic and Responsive.



## Maintaining Conversation State: Ability to remember previous interaction in the ongoing session.

#Example : 
#import google.generativeai as genai

#genai.configure(api_key="YOUR_GOOGLE_API_KEY") 

#model = genai.GenerativeModel("gemini-pro")

#chat = model.start_chat(history=[
    #{"role": "user", "content": "Tell me about AI."},
    #{"role": "assistant", "content": "AI stands for artificial intelligence, the field focused on creating intelligent systems."}
#])

# Now we ask a follow-up question without repeating the context
#response = chat.send_message("Can you give an example of AI in daily life?", stream=True)

# Process and print each chunk of the streamed response
#print("AI Response:")
#for chunk in response:
    #print(chunk.text)

# Here, the model understands that "AI" refers to "artificial intelligence" from the previous interaction.


# Multi Turn Conversation : A multi-turn conversation is an interaction where the user and the AI exchange several back-and-forth messages, with each new message often relating to previous ones.
# Multi-turn conversation and Maintaining conversation state are closely related concepts. Maintaining the conversation state makes multi-turn conversations meaningful.