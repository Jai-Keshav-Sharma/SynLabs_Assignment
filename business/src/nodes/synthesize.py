from src.models import GraphState, TechnicalSpecification
from src.config import Config
from src.prompts import SYNTHESIZE_PROMPT
from src.utils import save_report


def synthesize_report(state: GraphState) -> GraphState:
    """
    Node 5: Synthesize all information into a comprehensive Markdown report.
    
    Generates:
    - Well-formatted technical specification
    - Saves to Outputs folder
    """
    print("📝 Synthesizing technical specification...")
    
    llm = Config.get_llm(temperature=0.3)
    
    # Use structured output
    structured_llm = llm.with_structured_output(TechnicalSpecification)
    
    # Generate final report
    spec = structured_llm.invoke(
        SYNTHESIZE_PROMPT.format(
            requirement=state.requirement,
            analysis=state.analysis.model_dump_json(indent=2),
            modules=state.modules.model_dump_json(indent=2),
            schemas=state.schemas.model_dump_json(indent=2),
            pseudocode=state.pseudocode.model_dump_json(indent=2)
        )
    )
    
    # Update state
    state.final_report = spec.markdown_content
    
    # Save to file
    report_path = save_report(state.title, spec.markdown_content)
    
    print(f"✅ Report saved to: {report_path}")
    return state