from langchain.agents import initialize_agent, Tool
from langchain.llms import HuggingFaceHub
from modules.recon import perform_recon
from modules.scanner import perform_scan
from modules.fuzzer import perform_fuzz
from modules.ai_prioritizer import prioritize_findings

tools = [
    Tool(name="Recon", func=perform_recon, description="Run reconnaissance on a target domain."),
    Tool(name="Scan", func=perform_scan, description="Scan a URL for vulnerabilities. Requires url and type."),
    Tool(name="Fuzz", func=perform_fuzz, description="Fuzz an endpoint with payloads. Requires endpoint and payloads_file."),
    Tool(name="Prioritize", func=prioritize_findings, description="Prioritize list of findings.")
]

def create_cai_agent(tools):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl")  # Set HUGGINGFACEHUB_API_TOKEN env var
    agent = initialize_agent(tools, llm, agent_type="zero-shot-react-description")
    return agent

def run_agent(query, tools):
    agent = create_cai_agent(tools)
    return agent.run(query)
