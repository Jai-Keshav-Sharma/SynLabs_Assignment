ANALYZE_PROMPT = """You are a business analyst expert. Analyze the following business requirement and extract structured information.

Business Requirement:
{requirement}

Extract:
1. A short, clear title for this business idea (3-6 words)
2. The core business goal (one clear sentence)
3. Key actors/users who will interact with the system
4. Functional expectations (what the system should do)
5. Non-functional constraints as a list where each constraint has:
   - category: The type of constraint (performance, scalability, security, explainability, availability, etc.)
   - description: Specific details about that constraint

Provide a thorough analysis that will help developers understand the business context."""


DECOMPOSE_PROMPT = """You are a software architect. Based on the following business analysis, decompose the system into logical modules/components.

Business Analysis:
{analysis}

For each module, specify:
- Module name (clear and descriptive)
- Responsibility (what it does)
- Suggested tech stack (list of technologies)
- Dependencies on other modules (list of module names this depends on)

Think about:
- Frontend/UI components
- Backend services
- Databases
- External integrations
- APIs/Gateways
- Background jobs

Provide a comprehensive module breakdown that covers all aspects of the system."""


SCHEMA_PROMPT = """You are a database architect. Based on the system design, create detailed data schemas.

System Context:
Analysis: {analysis}
Modules: {modules}

Design data schemas including:
- Entity/Table names
- Fields with appropriate data types and constraints
- Relationships between entities (one-to-many, many-to-many, etc.)
- Recommended indexes for performance

Consider:
- Data normalization
- Query patterns
- Scalability
- Data integrity

Provide comprehensive schemas that support all system requirements."""


PSEUDOCODE_PROMPT = """You are a technical architect. Based on the complete system design, generate pseudo-code for the core workflows.

System Design:
Analysis: {analysis}
Modules: {modules}
Schemas: {schemas}

Generate clear, language-agnostic pseudo-code for:
1. Main user workflows (how users interact with the system)
2. Core business logic (algorithms, decision-making)
3. Data processing flows (how data moves through the system)

Each section should:
- Have a clear name and description
- Show step-by-step logic
- Include error handling considerations
- Reference the modules and schemas where applicable

Make it detailed enough that a developer can understand the implementation approach."""


SYNTHESIZE_PROMPT = """You are a technical documentation expert. Create a comprehensive, well-formatted technical specification document in Markdown.

You have the following information:
- Original Requirement: {requirement}
- Business Analysis: {analysis}
- System Modules: {modules}
- Data Schemas: {schemas}
- Pseudo-code: {pseudocode}

Create a developer-friendly document with these sections:

# Technical Specification: [Title]

## 1. Executive Summary
Brief overview of the requirement and solution

## 2. Business Requirement Analysis
- Core Business Goal
- Key Actors/Users
- Functional Expectations
- Non-Functional Constraints (organized by category)

## 3. System Architecture
### Module Overview
Detailed breakdown of each module with responsibilities and tech stack

### Module Dependencies
How modules interact with each other

## 4. Data Architecture
### Data Schemas
Complete schema definitions with fields, types, and relationships

### Data Flow
How data moves through the system

## 5. Implementation Logic
### Workflows
Pseudo-code for main workflows

### Business Logic
Core algorithms and decision-making logic

### Data Processing
How data is processed and transformed

## 6. Technical Recommendations
Key technical considerations for implementation

---

Format requirements:
- Use proper Markdown headers (##, ###)
- Use code blocks with ```sql, ```python, etc. where appropriate
- Use bullet points and numbered lists
- Use tables where helpful
- Make it visually clear and easy to scan
- Include all details from the provided information

Create a comprehensive, production-ready technical specification document."""