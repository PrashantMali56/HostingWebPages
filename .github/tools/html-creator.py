from pathlib import Path
import os
import re
import argparse
from typing import Optional, List

TITLE_RE = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
INDEX_CANDIDATES = {"index.html"}

def get_pages_base_url() -> Optional[str]:
    base = os.getenv("PAGES_BASE_URL", "").strip()
    if base:
        return base.rstrip("/")
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()  # owner/repo
    if repo and "/" in repo:
        owner, name = repo.split("/", 1)
        return f"https://{owner}.github.io/{name}"
    return None

def discover_index_targets(docs_root: Path, debug: bool = False) -> List[str]:
    """
    Recursively find folders that contain an index.html/htm.
    Prune traversal within a folder once its own top-level index is found.
    Returns POSIX relative folder paths (e.g., 'a/b', not including docs_root itself).
    """
    results: List[str] = []
    if not docs_root.exists():
        if debug:
            print(f"[debug] docs_root not found: {docs_root}")
        return results

    for dirpath, dirnames, filenames in os.walk(docs_root, topdown=True):
        folder = Path(dirpath)
        is_root = (folder == docs_root)
        lower_names = {fn.lower() for fn in filenames}
        has_index = any(candidate in lower_names for candidate in INDEX_CANDIDATES)

        if debug:
            print(f"[debug] visit: {folder} | has_index={has_index} | children={dirnames}")

        if has_index and not is_root:
            rel = folder.relative_to(docs_root).as_posix()
            results.append(rel)
            if debug:
                print(f"[debug] -> add '{rel}', prune deeper in this branch")
            dirnames[:] = []  # prune subtree
            continue
        # else keep walking deeper

    results.sort(key=str.lower)
    if debug:
        print(f"[debug] results: {results}")
    return results

def build_index_html(rel_folders: List[str], base_url: Optional[str]) -> str:
    def href_for(rel_folder: str) -> str:
        return f"{base_url}/{rel_folder}/index.html" if base_url else f"{rel_folder}/index.html"

    items_html = "\n        ".join(
        f'<li><a href="{href_for(rel)}">{Path(rel).name}</a></li>' for rel in rel_folders
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
    <p>Links under the <code>/Docs</code> directory:</p>
    <ul>
        {items_html}
    </ul>
</body>
</html>
"""

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Generate Docs/index.html linking to nested folders' index.html/htm (pruning at first match).")
    p.add_argument("-d", "--docs-root", default="./Docs", help="Path to Docs directory (default: ./Docs)")
    p.add_argument("--debug", action="store_true", help="Enable debug output")
    return p.parse_args()

def main() -> None:
    args = parse_args()
    docs_root = Path(args.docs_root).resolve()
    if not docs_root.exists():
        print(f"Docs root not found: {docs_root}")
        return

    base_url = get_pages_base_url()
    targets = discover_index_targets(docs_root, debug=args.debug)
    html = build_index_html(targets, base_url)
    out_file = docs_root / "index.html"
    out_file.write_text(html, encoding="utf-8")
    print(f"Wrote {out_file} with {len(targets)} link(s). Base URL: {base_url or '(relative)'}")

if __name__ == "__main__":
    main()