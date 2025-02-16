import streamlit as st
import os
import json
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from search_tool import search

# Set API key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize LLM
llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)

# Define Assistant Prompt
assistant_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI-powered admission expert specializing in providing concise, data-driven responses 
        based on the latest college cutoff information.
        If tool_outputs is present, use it to frame the output.

        ### **Tool: `search()`**
        - This tool retrieves college admission cutoffs based on various filters.
        - **Use `search()` when the query involves:** 
          - Specific colleges, programs, categories, quotas, or gender eligibility.
          - OpenRank (minimum rank) and Cutoff (maximum rank) filtering.
          - General admission trends based on rank.
        
        ### **Example Queries & Actions**
        **User:** "What is the cutoff for CS in IIT Bombay?"  
        **Action:** Call `search(college="Indian Institute of Technology Bombay", program="Computer Science and Engineering (4 Years, Bachelor of Technology)")` 

        ### **Example Queries & Actions**
        **User:** "What is the cutoff for CS in IIT Bombay?"  
        **Action:** Call `search(college="National Institute of Technology Nagaland", program="Computer Science and Engineering (4 Years, Bachelor of Technology)")` 

        If `tool_outputs` is empty, respond with: **"Will you please re-enter the requirements?"**
        """
    ),
    ("user", "{query}"),
    ("system", "{tool_outputs}")
])

# Bind tools
llm_with_tools = assistant_prompt | llm.bind_tools([search])

# Function to get LLM response
def llm_response(query, tool_outputs: Optional[str] = None):
    return llm_with_tools.invoke({"query": query, "tool_outputs": tool_outputs})

# Streamlit UI
st.set_page_config(page_title="Cadmi.ai by Soham Mhatre", layout="wide")

st.title("💬 Cadmi.ai by Soham Mhatre")
st.write("Ask me about college cutoffs and admission trends!")

# Chatbot history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
user_query = st.chat_input("Type your query here...")

if user_query:
    # Append user query to chat history
    st.session_state.messages.append({"role": "user", "content": user_query})

    # Generate response
    tool_outputs = {}
    result = llm_response(user_query, tool_outputs)
    tool_calls = result.additional_kwargs.get("tool_calls", [])
    if tool_calls:
        arguments_str = tool_calls[0]['function']['arguments']
        arguments_dict = json.loads(arguments_str)
        print("Parsed Arguments:", arguments_dict)
        if isinstance(arguments_dict, dict):
            tool_outputs["search"] = search.invoke(arguments_dict)
            search_output = str(tool_outputs.get("search", "No tool output available"))
            result = llm.invoke(
                f"This was the User_Query: {user_query} and this is the required tool output: {search_output}."
                "Please phrase this response as if you are an admission expert."
            )


        else:
            tool_outputs["search"] = "Invalid arguments format."
        
    bot_response = result.content if hasattr(result, "content") else "Sorry, I couldn't generate a response."
    st.session_state.messages.append({"role": "assistant", "content": bot_response})
    with st.chat_message("assistant"):
        st.markdown(bot_response)
