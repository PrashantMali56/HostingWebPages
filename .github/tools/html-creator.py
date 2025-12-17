import os
from pathlib import Path
from datetime import datetime

def find_html_files(docs_path):
    """Find all HTML files in subfolders under Docs directory."""
    html_files = {}
    docs_dir = Path(docs_path)
    
    if not docs_dir.exists():
        print(f"Warning: {docs_path} does not exist")
        return html_files
    
    # Iterate through subdirectories
    for subfolder in docs_dir.iterdir():
        if subfolder.is_dir():
            folder_name = subfolder.name
            html_files[folder_name] = []
            
            # Find all HTML files in this subfolder
            for html_file in subfolder.glob('*.html'):
                if html_file.name != 'index.html':  # Skip index files
                    html_files[folder_name].append({
                        'name': html_file.stem,
                        'path': f"{folder_name}/{html_file.name}"
                    })
    
    return html_files

def generate_landing_page(html_files, output_path):
    """Generate the landing page HTML."""
    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sample Pages - Index</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }
        
        header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }
        
        header p {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .content {
            padding: 40px;
        }
        
        .section {
            margin-bottom: 40px;
            padding: 30px;
            background: #f8f9fa;
            border-radius: 10px;
            border-left: 5px solid #667eea;
        }
        
        .section:last-child {
            margin-bottom: 0;
        }
        
        .section h2 {
            color: #333;
            font-size: 1.8em;
            margin-bottom: 20px;
            display: flex;
            align-items: center;
        }
        
        .section h2::before {
            content: "📁";
            margin-right: 10px;
        }
        
        .file-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 15px;
            list-style: none;
        }
        
        .file-item {
            background: white;
            border-radius: 8px;
            transition: all 0.3s ease;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        
        .file-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .file-item a {
            display: block;
            padding: 20px;
            color: #333;
            text-decoration: none;
            font-size: 1.1em;
            font-weight: 500;
        }
        
        .file-item a::before {
            content: "📄";
            margin-right: 10px;
        }
        
        .file-item a:hover {
            color: #667eea;
        }
        
        .empty-folder {
            color: #999;
            font-style: italic;
            padding: 20px;
        }
        
        footer {
            background: #333;
            color: white;
            text-align: center;
            padding: 20px;
            font-size: 0.9em;
        }
        
        .stats {
            display: flex;
            justify-content: space-around;
            margin-top: 30px;
            padding: 20px;
            background: white;
            border-radius: 10px;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-number {
            font-size: 2em;
            font-weight: bold;
            color: #667eea;
        }
        
        .stat-label {
            color: #666;
            margin-top: 5px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🚀 Sample Pages Collection</h1>
            <p>Browse through our HTML samples organized by categories</p>
        </header>
        
        <div class="content">
"""
    
    # Count total files and folders
    total_folders = len(html_files)
    total_files = sum(len(files) for files in html_files.values())
    
    # Add statistics
    html_content += f"""
            <div class="stats">
                <div class="stat-item">
                    <div class="stat-number">{total_folders}</div>
                    <div class="stat-label">Folders</div>
                </div>
                <div class="stat-item">
                    <div class="stat-number">{total_files}</div>
                    <div class="stat-label">HTML Files</div>
                </div>
            </div>
"""
    
    # Generate sections for each folder
    if not html_files:
        html_content += """
            <div class="section">
                <p class="empty-folder">No HTML files found in any subfolders</p>
            </div>
"""
    else:
        for folder_name, files in sorted(html_files.items()):
            html_content += f"""
            <div class="section">
                <h2>{folder_name.replace('_', ' ').title()}</h2>
"""
            
            if files:
                html_content += """                <ul class="file-grid">\n"""
                for file in sorted(files, key=lambda x: x['name']):
                    html_content += f"""                    <li class="file-item">
                        <a href="{file['path']}">{file['name']}</a>
                    </li>\n"""
                html_content += """                </ul>\n"""
            else:
                html_content += """                <p class="empty-folder">No HTML files found in this folder</p>\n"""
            
            html_content += """            </div>\n"""
    
    # Close HTML with timestamp
    html_content += f"""        </div>
        
        <footer>
            <p>Generated automatically by GitHub Actions | Last updated: {current_time}</p>
        </footer>
    </div>
</body>
</html>
"""
    
    # Write to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Landing page generated successfully at {output_path}")
    print(f"📁 Total folders: {total_folders}")
    print(f"📄 Total HTML files: {total_files}")
    
    # List found files for debugging
    if html_files:
        print("\n📋 Found files:")
        for folder, files in sorted(html_files.items()):
            print(f"  {folder}: {len(files)} file(s)")
            for file in files:
                print(f"    - {file['name']}")

if __name__ == "__main__":
    # Define paths
    docs_path = "./Docs"
    output_file = os.path.join(docs_path, "index.html")
    
    print(f"🔍 Scanning for HTML files in: {docs_path}")
    
    # Find all HTML files
    html_files = find_html_files(docs_path)
    
    # Generate landing page
    generate_landing_page(html_files, output_file)