from pathlib import Path
import os
import re
from typing import Optional, List

DOCS_ROOT = Path("./Docs")
TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)

def get_pages_base_url() -> Optional[str]:
    # Prefer explicit env
    base = os.getenv("PAGES_BASE_URL", "").strip()
    if base:
        return base.rstrip("/")
    # Derive from GitHub Actions env
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()  # owner/repo
    if repo and "/" in repo:
        owner, name = repo.split("/", 1)
        return f"https://{owner}.github.io/{name}"
    return None

def discover_subindexes(docs_root: Path) -> List[str]:
    """Return list of subfolder names that contain an index.html."""
    items: List[str] = []
    if not docs_root.exists():
        return items
    for sub in sorted(docs_root.iterdir(), key=lambda p: p.name.lower()):
        if sub.is_dir() and (sub / "index.html").exists():
            items.append(sub.name)
    return items

def build_index_html(folders: List[str], base_url: Optional[str]) -> str:
    # Build href for each folder
    def href_for(folder: str) -> str:
        # Absolute for Pages if base_url available, else relative from Docs root
        return f"{base_url}/{folder}/index.html" if base_url else f"{folder}/index.html"

    # Link title is the folder name
    items_html = "\n        ".join(
        f'<li><a href="{href_for(folder)}">{folder}</a></li>' for folder in folders
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Documentation</title>
</head>
<body>
    <h1>Documentation</h1>
    <p>Below are the included markdown files from the <code>/Docs</code> directory:</p>
    <ul>
        {items_html}
    </ul>
</body>
</html>
"""

def main():
    base_url = get_pages_base_url()
    folders = discover_subindexes(DOCS_ROOT)
    html = build_index_html(folders, base_url)
    out_file = DOCS_ROOT / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote {out_file} with {len(folders)} link(s). Base URL: {base_url or '(relative)'}")

if __name__ == "__main__":
    main()