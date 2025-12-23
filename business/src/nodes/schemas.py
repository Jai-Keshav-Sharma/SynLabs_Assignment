from src.models import GraphState, DataSchemas
from src.config import Config
from src.prompts import SCHEMA_PROMPT


def design_schemas(state: GraphState) -> GraphState:
    """
    Node 3: Design data schemas for the system.
    
    Generates:
    - Entity/table definitions
    - Field specifications
    - Relationships
    - Indexes
    """
    print("🗄️  Designing data schemas...")
    
    llm = Config.get_llm(temperature=0.4)
    
    # Use structured output
    structured_llm = llm.with_structured_output(DataSchemas)
    
    # Generate schemas
    schemas = structured_llm.invoke(
        SCHEMA_PROMPT.format(
            analysis=state.analysis.model_dump_json(indent=2),
            modules=state.modules.model_dump_json(indent=2)
        )
    )
    
    # Update state
    state.schemas = schemas
    
    print(f"✅ Designed {len(schemas.schemas)} data schemas")
    return state