from langgraph.graph import StateGraph, END
from src.models import GraphState
from src.nodes import (
    analyze_requirements,
    decompose_modules,
    design_schemas,
    generate_pseudocode,
    synthesize_report
)


def create_workflow():
    """Create the LangGraph workflow for requirement conversion."""
    
    # Initialize the graph
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("analyze", analyze_requirements)
    workflow.add_node("decompose", decompose_modules)
    workflow.add_node("schemas", design_schemas)
    workflow.add_node("pseudocode", generate_pseudocode)
    workflow.add_node("synthesize", synthesize_report)
    
    # Define the flow
    workflow.set_entry_point("analyze")
    workflow.add_edge("analyze", "decompose")
    workflow.add_edge("decompose", "schemas")
    workflow.add_edge("schemas", "pseudocode")
    workflow.add_edge("pseudocode", "synthesize")
    workflow.add_edge("synthesize", END)
    
    # Compile the graph
    app = workflow.compile()
    
    return app