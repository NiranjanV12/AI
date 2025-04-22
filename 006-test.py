import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())
#ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]

#from langchain_anthropic import ChatAnthropic
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

#model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
#model2 = ChatAnthropic(model="claude-3-5-sonnet-20240620")
#chatModel4o = ChatAnthropic(model="claude-3-5-sonnet-20240620")


from langchain_ollama import ChatOllama

local_llm = "mistral:7b-instruct"
#local_llm = "DeepSeek-R1:1.5b"

model = ChatOllama(model=local_llm, temperature=0.0)

def add(a: float, b: float) -> float:
    """Add two numbers."""
    return a + b

def multiply(a: float, b: float) -> float:
    """Multiply two numbers."""
    return a * b

def web_search(query: str) -> str:
    """Search the web for information."""
    return (
        "Here are the headcounts for each of the FAANG companies in 2024:\n"
        "1. **Facebook (Meta)**: 67,317 employees.\n"
        "2. **Apple**: 164,000 employees.\n"
        "3. **Amazon**: 1,551,000 employees.\n"
        "4. **Netflix**: 14,000 employees.\n"
        "5. **Google (Alphabet)**: 181,269 employees."
    )

math_agent = create_react_agent(
    model=model,
    tools=[add, multiply],
    name="math_expert",
    prompt="You are a math expert. Always use one tool at a time."
)

research_agent = create_react_agent(
    model=model,
    tools=[web_search],
    name="research_expert",
    prompt="You are a world class researcher with access to web search. Do not do any math."
)

# Create supervisor workflow
workflow = create_supervisor(
    [research_agent, math_agent],
    model=model,
    prompt=(
        "You are a team supervisor managing a research expert and a math expert. "
        "For current events, use research_agent. "
        "For math problems, use math_agent."
    )
)

# Compile and run
app = workflow.compile()
result = app.invoke({
    "messages": [
        {
            "role": "user",
            "content": "create feature file prompt in cucumber for login with user id and password field, for scenarios like incorrect creds, login success, already logged in etc"
        }
    ]
})

print(result)
