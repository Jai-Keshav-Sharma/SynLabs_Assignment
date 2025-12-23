from pydantic import BaseModel, Field
from typing import List


class Constraint(BaseModel):
    """A single non-functional constraint."""
    category: str = Field(description="Type of constraint (e.g., performance, scalability, security)")
    description: str = Field(description="Details about the constraint")


class BusinessAnalysis(BaseModel):
    """Structured output for requirement analysis."""
    title: str = Field(description="Short, clear title for the business idea")
    business_goal: str = Field(description="Core business objective in one sentence")
    actors: List[str] = Field(description="Key users or stakeholders")
    functional_expectations: List[str] = Field(description="What the system should do")
    constraints: List[Constraint] = Field(description="Non-functional requirements like performance, scalability, security")


class Module(BaseModel):
    """Represents a system module/component."""
    name: str = Field(description="Module name")
    responsibility: str = Field(description="What this module does")
    tech_stack: List[str] = Field(description="Suggested technologies")
    dependencies: List[str] = Field(description="Other modules this depends on")


class ModuleDecomposition(BaseModel):
    """Collection of system modules."""
    modules: List[Module] = Field(description="List of system modules")


class SchemaField(BaseModel):
    """Database field definition."""
    name: str = Field(description="Field name")
    type: str = Field(description="Data type")
    constraints: str = Field(default="", description="Field constraints like NOT NULL, UNIQUE, etc.")


class DataSchema(BaseModel):
    """Database schema/entity definition."""
    entity: str = Field(description="Table or collection name")
    fields: List[SchemaField] = Field(description="Schema fields")
    relationships: List[str] = Field(description="Relationships with other entities")
    indexes: List[str] = Field(description="Recommended indexes for performance")


class DataSchemas(BaseModel):
    """Collection of data schemas."""
    schemas: List[DataSchema] = Field(description="List of data schemas")


class PseudoCodeSection(BaseModel):
    """Pseudo-code for a specific workflow."""
    name: str = Field(description="Workflow name")
    description: str = Field(description="What this workflow does")
    pseudocode: str = Field(description="Step-by-step pseudo-code")


class PseudoCode(BaseModel):
    """Collection of pseudo-code sections."""
    sections: List[PseudoCodeSection] = Field(description="List of pseudo-code sections")


class TechnicalSpecification(BaseModel):
    """Final technical specification document."""
    markdown_content: str = Field(description="Complete specification in Markdown format")


# Separate state class without structured output constraints
class GraphState(BaseModel):
    """State object passed through the LangGraph workflow."""
    requirement: str
    title: str = ""
    analysis: BusinessAnalysis | None = None
    modules: ModuleDecomposition | None = None
    schemas: DataSchemas | None = None
    pseudocode: PseudoCode | None = None
    final_report: str = ""
    
    class Config:
        arbitrary_types_allowed = True