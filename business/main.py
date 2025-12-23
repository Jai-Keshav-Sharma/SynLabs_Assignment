import sys
from src.models import GraphState
from src.graph import create_workflow


def main():
    """Main entry point for the requirement conversion pipeline."""
    
    print("=" * 80)
    print("🤖 AI-Based Requirement to Technical Specification Pipeline")
    print("=" * 80)
    print()
    
    # Example requirement (you can change this or take input)
    requirement = "Build a system that recommends products to users based on browsing history."
    
    # Allow custom requirement via command line
    if len(sys.argv) > 1:
        requirement = " ".join(sys.argv[1:])
    
    print(f"📋 Business Requirement:")
    print(f"   {requirement}")
    print()
    print("🔄 Starting conversion pipeline...")
    print("-" * 80)
    print()
    
    # Create initial state
    initial_state = GraphState(requirement=requirement)
    
    # Create and run workflow
    app = create_workflow()
    result = app.invoke(initial_state)
    
    # Extract title from result dictionary
    title = result.get("title", "Unknown Project")
    
    print()
    print("-" * 80)
    print("✨ Pipeline completed successfully!")
    print(f"📁 Technical specification generated for: '{title}'")
    print("=" * 80)


if __name__ == "__main__":
    main()