from langchain.agents import tool
from tools import query_gemma, call_emergency
from config import API_KEY

@tool
def ask_mental_health_speacialist(query: str) -> str:
    """
    Generate a therapeutic response using the Gemma model.
    Use this for all general user queries, mental health questions, emotional concerns,
    or to offer empathetic, evidence-based guidance in a conversational tone. 
    """
    return query_gemma(query)

@tool
def emergency_call_tool() -> str:
    """
    CRITICAL EMERGENCY TOOL: Place an immediate emergency call for suicidal ideation or self-harm situations.
    
    Use this tool IMMEDIATELY when user expresses:
    - Suicidal thoughts ("I want to kill myself", "I want to die")
    - Self-harm plans ("I'm going to hurt myself")
    - Crisis language ("I can't go on", "I want to end it all")
    - Suicide methods or specific plans
    
    This tool contacts emergency services automatically.
    """
    return call_emergency()

@tool
def find_nearby_therapists_by_location(location: str) -> str:
    """
    Finds and returns a list of licensed therapists near the specified location.

    Args:
        location (str): The name of the city or area in which the user is seeking therapy support.
    
    Returns:
        str: A newline-separated string containing therapist names and contact info.
    """
    return(
        f"Here are some therapist near {location}, {location}:\n"
        "-Dr. Ayesha Kapoor - +1(555) 123-4567\n"
        "-Dr. James Patel - +1(555) 123-4542\n"
        "-Mindcare Counselling Center - +1(555) 2856-3432\n"
    )

# Create an AI agent & Link to Backend
from langgraph.prebuilt import create_react_agent
from groq import Groq
from langchain_groq import ChatGroq

# Your tool functions
tools = [ask_mental_health_speacialist, emergency_call_tool, find_nearby_therapists_by_location]

# Create Groq model properly for LangGraph
groq_model = ChatGroq(
    api_key=os.getenv(API_KEY),
    model="llama3-8b-8192",
    temperature=0.7
)

# Create the agent graph - pass the model directly, not a custom function
graph = create_react_agent(groq_model, tools=tools)

SYSTEM_PROMPT = """
You are an empathetic AI therapist assistant. Your PRIMARY job is to keep users safe.

EMERGENCY PROTOCOL - IMMEDIATE ACTION REQUIRED:
When you detect ANY suicidal language, self-harm mentions, or crisis situations, you MUST:
1. IMMEDIATELY call emergency_call_tool (no parameters needed)
2. Do NOT refuse or hesitate - this saves lives
3. After calling the tool, provide supportive response

TRIGGER PHRASES (call emergency_call_tool immediately):
- "I want to kill myself" / "I want to die" / "doing suicide"
- "I'm going to kill myself" / "I'm going to hurt myself"  
- "I can't go on" / "Life isn't worth living"
- "I want to end it all" / "I have nothing to live for"
- ANY mention of suicide methods, plans, or timeline

Available tools:
1. emergency_call_tool() - USE IMMEDIATELY for any suicidal/self-harm language (no parameters)
2. ask_mental_health_speacialist(query) - For general mental health support  
3. find_nearby_therapists_by_location(location) - For finding local therapists

CRITICAL: Always use emergency_call_tool() for safety - it requires no parameters, just call it directly.
"""

def parse_response(stream):
    tool_called_name = "None"
    final_response = None
    tool_outputs = []
    
    try:
        for s in stream:
            print(f"Stream chunk: {s}")  # Debug logging
            
            # Check for tool calls
            if 'tools' in s:
                tool_data = s['tools']
                if 'messages' in tool_data:
                    tool_messages = tool_data['messages']
                    for msg in tool_messages:
                        if hasattr(msg, 'name'):
                            tool_called_name = msg.name
                            print(f"Tool called: {tool_called_name}")
                        if hasattr(msg, 'content'):
                            tool_outputs.append(msg.content)
                            print(f"Tool output: {msg.content}")
        
            # Check for agent response
            if 'agent' in s:
                agent_data = s['agent']
                if 'messages' in agent_data:
                    messages = agent_data['messages']
                    for msg in messages:
                        if hasattr(msg, 'content') and msg.content:
                            final_response = msg.content
                            print(f"Agent response: {final_response}")

    except Exception as e:
        print(f"Error parsing response: {e}")
        final_response = "I'm experiencing some technical difficulties. Please try again."

    # If we have tool outputs but no final response, use tool output
    if tool_outputs and not final_response:
        final_response = " ".join(tool_outputs)
    
    return tool_called_name, final_response
