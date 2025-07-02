import os
from dotenv import load_dotenv
from backend.calendar_service import create_event, suggest_free_slot

from langchain.agents import tool, create_tool_calling_agent, AgentExecutor
from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_mistralai import ChatMistralAI

# ✅ Load API key from .env
load_dotenv()
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

# ✅ Tool 1: Book a meeting
@tool
def book_meeting(date_time: str, summary: str = "Appointment via TailorTalk") -> str:
    """
    Book a calendar meeting on the given date_time.
    The date_time can be natural language (e.g., "tomorrow at 5pm") or ISO format.
    """
    result = create_event(summary=summary, date_time_str=date_time)
    if result["success"]:
        return f"✅ Meeting booked! [Click to view]({result['event_link']})"
    else:
        return f"❌ Booking failed: {result['event_link']}"

# ✅ Tool 2: Suggest next available slot
@tool
def check_free_time(date: str = "tomorrow") -> str:
    """
    Suggests the next available time slot for the given date (default is tomorrow).
    """
    return suggest_free_slot(date)

# ✅ LLM setup
llm = ChatMistralAI(
    model="mistral-small-latest",
    temperature=0.7,
    api_key=MISTRAL_API_KEY
)

# ✅ System prompt with examples
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are TailorTalk, an AI assistant that helps users book meetings using Google Calendar.\n\n"
        "1. Use the `book_meeting` tool when the user provides a specific date/time — like 'book a meeting tomorrow at 4 PM'.\n"
        "2. Use the `check_free_time` tool when the user asks things like 'suggest a free slot tomorrow', or 'when am I free on Friday?'.\n\n"
        "Natural language like 'next Monday at 3' is acceptable."
    ),
    MessagesPlaceholder(variable_name="messages"),
    MessagesPlaceholder(variable_name="agent_scratchpad")
])

# ✅ Tool-calling agent with both tools
agent = create_tool_calling_agent(llm=llm, tools=[book_meeting, check_free_time], prompt=prompt)
agent_executor = AgentExecutor(agent=agent, tools=[book_meeting, check_free_time], verbose=True)

# ✅ Entry point for FastAPI
def run_agent(message: str) -> str:
    try:
        result = agent_executor.invoke({"messages": [HumanMessage(content=message)]})
        print("🧠 Agent output:", result)
        return result.get("output", "❌ No response generated.")
    except Exception as e:
        return f"❌ Agent Error: {str(e)}"
