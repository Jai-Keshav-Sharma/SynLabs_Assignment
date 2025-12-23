from src.models import GraphState, ModuleDecomposition
from src.config import Config
from src.prompts import DECOMPOSE_PROMPT


def decompose_modules(state: GraphState) -> GraphState:
    """
    Node 2: Decompose system into modules/components.
    
    Generates:
    - Module names
    - Responsibilities
    - Tech stack suggestions
    - Dependencies
    """
    print("🏗️  Decomposing system into modules...")
    
    llm = Config.get_llm(temperature=0.5)
    
    # Use structured output
    structured_llm = llm.with_structured_output(ModuleDecomposition)
    
    # Generate modules
    modules = structured_llm.invoke(
        DECOMPOSE_PROMPT.format(
            analysis=state.analysis.model_dump_json(indent=2)
        )
    )
    
    # Update state
    state.modules = modules
    
    print(f"✅ Identified {len(modules.modules)} modules")
    return state