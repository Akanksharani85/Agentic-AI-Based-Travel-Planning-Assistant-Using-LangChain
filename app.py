import streamlit as st
import asyncio

# --- FIX: Event Loop Error Fix for Windows ---
try:
    asyncio.get_event_loop()
except RuntimeError:
    asyncio.set_event_loop(asyncio.new_event_loop())

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from tools import search_flights, search_hotels, search_places, get_weather

# --- Page Config ---
st.set_page_config(page_title="AI Travel Agent", page_icon="✈️")

st.title("✈️ AI Travel Agent 🌍")
st.write("Main hoon tumhara AI Agent. Flights, Hotels, aur Places sab dhoond dunga!")

# --- Sidebar for API Key ---
st.sidebar.header("🔑 Secret Key")
api_key = st.sidebar.text_input("Apni Google API Key yahan daalo:", type="password")

if api_key:
    # --- Agent Setup ---
    # Model Setup
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        temperature=0
    )

    # Tools Setup
    tools = [
        Tool(
            name="Search Flights",
            func=search_flights,
            description="Use this tool to find flights. Input: 'Source, Destination'"
        ),
        Tool(
            name="Search Hotels",
            func=search_hotels,
            description="Use this tool to find hotels. Input: City Name"
        ),
        Tool(
            name="Search Places",
            func=search_places,
            description="Use this tool to find tourist places. Input: City Name"
        ),
        Tool(
            name="Check Weather",
            func=get_weather,
            description="Use this tool to check weather. Input: City Name"
        )
    ]

    # Prompt Template
    template = '''Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:{agent_scratchpad}'''

    prompt = PromptTemplate.from_template(template)

    # Agent Creation
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

    # --- Chat Interface ---
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Purani chat dikhana
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Naya input lena
    user_input = st.chat_input("Kahan jana hai? (e.g. Plan a trip from Mumbai to Goa)")

    if user_input:
        # User ka message dikhana
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # AI ka sochna
        with st.chat_message("assistant"):
            with st.spinner("Soch raha hoon... 🧠"):
                try:
                    response = agent_executor.invoke({"input": user_input})
                    result = response['output']
                    st.markdown(result)
                    st.session_state.messages.append({"role": "assistant", "content": result})
                except Exception as e:
                    st.error(f"Error aaya: {e}")

else:
    st.warning("👈 Pehle left side mein apni API Key daalo!")