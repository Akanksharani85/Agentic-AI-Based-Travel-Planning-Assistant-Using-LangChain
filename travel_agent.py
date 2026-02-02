import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool
from langchain_core.prompts import PromptTemplate
from tools import search_flights, search_hotels, search_places, get_weather

# --- 1. AI Setup ---
# API Key Yahan Daal
api_key = "AIzaSyBFQvq7VVxWTqMT072TSGuhFzylC61dLjU"

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",       
    google_api_key=api_key,
    temperature=0
)

# --- 2. Tools Connect Karna ---
tools = [
    Tool(
        name="Search Flights",
        func=search_flights,
        description="Use for finding flights. Input: 'Source, Destination'"
    ),
    Tool(
        name="Search Hotels",
        func=search_hotels,
        description="Use for finding hotels. Input: City Name"
    ),
    Tool(
        name="Search Places",
        func=search_places,
        description="Use for finding tourist places. Input: City Name"
    ),
    Tool(
        name="Check Weather",
        func=get_weather,
        description="Use for checking weather. Input: City Name"
    )
]

# --- 3. Prompt Template ---
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

# --- 4. Agent Banana ---
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)

# --- 5. Test Karna ---
if __name__ == "__main__":
    print("🤖 Travel Agent Ready Hai! (Type 'exit' to stop)")
    while True:
        user_input = input("\n✈️  Kahan jana hai? (Query likho): ")
        if user_input.lower() in ["exit", "quit"]:
            break
        
        try:
            print("\n... Soch raha hoon ...\n")
            response = agent_executor.invoke({"input": user_input})
            print(f"\n✅ AI Response:\n{response['output']}")
        except Exception as e:
            print(f"❌ Error aaya: {e}")