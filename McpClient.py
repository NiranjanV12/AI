from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage

import asyncio

import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

#from langchain_openai import ChatOpenAI
#model = ChatOpenAI(model="gpt-4o")
from langchain_ollama import ChatOllama

#local_llm = "mistral:7b-instruct"

local_llm = "qwen2.5:7B"
#local_llm = "DeepSeek-R1:1.5b"

model = ChatOllama(model=local_llm, temperature=0.0)


async def get_json():
  async with MultiServerMCPClient(
      {
          # "math": {
          #     "command": "python",
          #     # Make sure to update to the full absolute path to your math_server.py file
          #     "args": ["/home/niranjanv/2024/2025/AI/001-LANGGRAPH-ROUND2-master/McpMathServer.py"],
          #     "transport": "stdio",
          # },
          # # "weather": {
          # #     # make sure you start your weather server on port 8000
          # #     "url": "http://localhost:8000/sse",
          # #     "transport": "sse",
          # # },
          # "tavily_websearch": {
          #       "command": "python",
          #       "args": ["/home/niranjanv/2024/2025/AI/001-LANGGRAPH-ROUND2-master/McpTavaliyServer.py"],
          #       "transport": "stdio",
          #   },
          "mcp-server-time": {
               "command": "python",
               "args": ["-m", "mcp_server_time", "--local-timezone", "Asia/Kolkata"]
  
            },
          "file-system": {
            "command": "npx",
            "args": [
              "-y",
              "@modelcontextprotocol/server-filesystem",
              "/home/niranjanv/AI_workspace"
            ]
          }
      }
  ) as client:
      agent = create_react_agent(model, client.get_tools())
      system_message = SystemMessage(content=(
                "You have access to multiple tools that can help answer queries. "
                "Use them dynamically and efficiently based on the user's request. if you dont have answers you can do websearch using tavily_websearch tool"
        ))
      #math_response = await agent.ainvoke({"messages": "math operation: what's (3 + 5) x 12?"})
      #weather_response = await agent.ainvoke({"messages": "what is the weather in nyc?"})
      #required_data = await agent.ainvoke({"messages": "do websearch to find todays Nifty points?"})
      required_data = await agent.ainvoke({"messages": [system_message, HumanMessage(content=query)]})


      #print(math_response)
      #print("------------------------")
      #print(weather_response)
      print("------------------------")
      print(required_data)
      print("------------------------")
      print("------------------------")
      print("Final Output: "+required_data["messages"][-1].content)

while True: 
   query = input("Query:")
   if query.lower() == "exit":
     break
   elif query.strip() == "":
      print("")
   else:
     loop = asyncio.get_event_loop()
     loop.run_until_complete(get_json())

     #create feature file prompt in cucumber for login with user id and password field, for scenarios like incorrect creds, write output to featurefile_{timestamp}.txt, replace {timestamp} with get_current_time in format ddMMyyyyHHmmss with Asia/Kolkata as timezone 
