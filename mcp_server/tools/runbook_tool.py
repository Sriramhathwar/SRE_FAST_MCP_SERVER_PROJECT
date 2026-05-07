from rag.retriever import retrieve_docs

def runbook_tool(query):
    return retrieve_docs(query)