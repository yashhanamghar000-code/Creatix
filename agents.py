from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# ── Model ─────────────────────────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0
)

# ── Search Agent (Tool Binding) ───────────────────
def build_search_agent():
    return llm.bind_tools([web_search])

# ── Reader Agent (Tool Binding) ───────────────────
def build_reader_agent():
    return llm.bind_tools([scrape_url])

# ── Writer Chain ──────────────────────────────────
writer_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an expert research writer."),
    ("human", """Write a detailed report.

Topic: {topic}

Research:
{research}

Structure:
- Introduction
- Key Findings
- Conclusion
- Sources""")
])

writer_chain = writer_prompt | llm | StrOutputParser()

# ── Critic Chain ──────────────────────────────────
critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a strict critic."),
    ("human", """Review this report:

{report}

Give:
- Score /10
- Strengths
- Weaknesses
- Final verdict""")
])

critic_chain = critic_prompt | llm | StrOutputParser()