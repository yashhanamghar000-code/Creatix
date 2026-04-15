from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv
import streamlit as st
import os

load_dotenv()

# ── Load API KEY safely ─────────────────────────────
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY is missing")

# ── SINGLE LLM INSTANCE (FIXED) ────────────────────
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    api_key=api_key
)

# ── Search Agent ────────────────────────────────────
def build_search_agent():
    return llm.bind_tools([web_search])

# ── Reader Agent ────────────────────────────────────
def build_reader_agent():
    return llm.bind_tools([scrape_url])

# ── Writer Chain ────────────────────────────────────
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

# ── Critic Chain ────────────────────────────────────
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