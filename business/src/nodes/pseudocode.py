from src.models import GraphState, PseudoCode
from src.config import Config
from src.prompts import PSEUDOCODE_PROMPT


def generate_pseudocode(state: GraphState) -> GraphState:
    """
    Node 4: Generate pseudo-code for core workflows.
    
    Generates:
    - Main user workflows
    - Business logic
    - Data processing flows
    """
    print("💻 Generating pseudo-code...")
    
    llm = Config.get_llm(temperature=0.6)
    
    # Use structured output
    structured_llm = llm.with_structured_output(PseudoCode)
    
    # Generate pseudo-code
    pseudocode = structured_llm.invoke(
        PSEUDOCODE_PROMPT.format(
            analysis=state.analysis.model_dump_json(indent=2),
            modules=state.modules.model_dump_json(indent=2),
            schemas=state.schemas.model_dump_json(indent=2)
        )
    )
    
    # Update state
    state.pseudocode = pseudocode
    
    print(f"✅ Generated {len(pseudocode.sections)} pseudo-code sections")
    return state