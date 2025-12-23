from src.models import GraphState, BusinessAnalysis
from src.config import Config
from src.prompts import ANALYZE_PROMPT


def analyze_requirements(state: GraphState) -> GraphState:
    """
    Node 1: Analyze business requirements and extract structured information.
    
    Extracts:
    - Business title
    - Core goal
    - Key actors
    - Functional expectations
    - Non-functional constraints
    """
    print("📊 Analyzing business requirements...")
    
    llm = Config.get_llm(temperature=0.3)
    
    # Use structured output with Pydantic
    structured_llm = llm.with_structured_output(BusinessAnalysis)
    
    # Generate analysis
    analysis = structured_llm.invoke(
        ANALYZE_PROMPT.format(requirement=state.requirement)
    )
    
    # Update state
    state.title = analysis.title
    state.analysis = analysis
    
    print(f"✅ Analysis complete. Project: '{analysis.title}'")
    return state