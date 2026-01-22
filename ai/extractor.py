import re
from pathlib import Path
import pandas as pd

EXTRACTED_DIR = Path("data/extracted")
PROCESSED_DIR = Path("data/processed")

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def extract_projects_from_text(text, source_file):
    """
    Extract project-level information from raw text
    """
    projects = []

    # Split text into blocks (heuristic)
    blocks = re.split(r"\n{2,}", text)

    for block in blocks:
        if "%" not in block:
            continue

        project = {
            "source_file": source_file,
            "project_name": None,
            "sector": None,
            "progress_percent": None,
            "cost_cr": None
        }

        # Project name (heuristic)
        name_match = re.search(r"(Project|Work|Section)\s*[:\-]?\s*(.+)", block, re.IGNORECASE)
        if name_match:
            project["project_name"] = name_match.group(2).strip()

        # Sector
        if "rail" in block.lower():
            project["sector"] = "Railways"
        elif "road" in block.lower() or "nh-" in block.lower():
            project["sector"] = "Roads"

        # Progress %
        progress_match = re.search(r"(\d{1,3})\s*%", block)
        if progress_match:
            project["progress_percent"] = int(progress_match.group(1))

        # Cost in crore
        cost_match = re.search(r"(₹|Rs\.?)\s*(\d+(\.\d+)?)\s*(Cr|Crore)", block, re.IGNORECASE)
        if cost_match:
            project["cost_cr"] = float(cost_match.group(2))

        if project["progress_percent"] is not None:
            projects.append(project)

    return projects


def run_extraction():
    all_projects = []

    for txt_file in EXTRACTED_DIR.glob("*.txt"):
        print(f"Processing: {txt_file.name}")

        with open(txt_file, "r", encoding="utf-8") as f:
            text = f.read()

        projects = extract_projects_from_text(text, txt_file.name)
        all_projects.extend(projects)

    if not all_projects:
        print("No projects extracted.")
        return

    df = pd.DataFrame(all_projects)
    output_path = PROCESSED_DIR / "projects.csv"
    df.to_csv(output_path, index=False)

    print(f"Saved structured data to {output_path}")


if __name__ == "__main__":
    run_extraction()
