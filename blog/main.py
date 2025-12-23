"""SEO Blog Automation - Entry Point"""

from src.workflow import create_workflow


def main():
    print("=" * 60)
    print("🚀 SEO Blog Automation - LangGraph Workflow")
    print("=" * 60)
    
    # Create and run workflow
    app = create_workflow()
    result = app.invoke({})
    
    # Print results
    print("\n" + "=" * 60)
    print("✅ WORKFLOW COMPLETE")
    print("=" * 60)
    print(f"📝 Blog Title: {result['blog_title']}")
    print(f"🔑 SEO Keywords: {result['seo_keywords']}")
    print(f"🔗 Live URL: {result['publish_url']}")
    print("=" * 60)


if __name__ == "__main__":
    main()