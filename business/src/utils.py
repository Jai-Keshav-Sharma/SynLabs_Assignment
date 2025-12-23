import os
import re
from pathlib import Path
from src.config import Config


def sanitize_filename(title: str) -> str:
    """Convert title to a valid folder name."""
    # Remove special characters, keep alphanumeric and spaces
    sanitized = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with underscores
    sanitized = re.sub(r'\s+', '_', sanitized)
    # Convert to lowercase
    sanitized = sanitized.lower()
    return sanitized


def save_report(title: str, markdown_content: str) -> str:
    """Save the technical specification report to a file."""
    # Create output directory if it doesn't exist
    output_dir = Path(Config.OUTPUT_DIR)
    output_dir.mkdir(exist_ok=True)
    
    # Create project-specific folder
    folder_name = sanitize_filename(title)
    project_dir = output_dir / folder_name
    project_dir.mkdir(exist_ok=True)
    
    # Save the report
    report_path = project_dir / "specification.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    
    return str(report_path)