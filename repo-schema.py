import os
import json
import re
import sys
import time
import mimetypes
from datetime import datetime
from pathspec import PathSpec

# Configuration Constants
# ----------------------

# Debug mode flag (set to False to disable debug messages)
DEBUG = False

# Define the base directory and output files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_JSON = os.path.join(BASE_DIR, "repo-schema.json")
OUTPUT_MD = os.path.join(BASE_DIR, "repo-schema.md")

# File processing limits and exclusions
FILE_SIZE_LIMIT = 1 * 1024 * 1024  # 1MB in bytes - prevents processing of large files

# Known binary file extensions to exclude from processing
BINARY_EXTENSIONS = {
    '.exe', '.dll', '.so', '.dylib', '.bin',
    '.zip', '.tar', '.gz', '.7z', '.rar',
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.ico', '.webp',
    '.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx',
    '.pyc', '.pyo', '.class', '.o', '.a', '.lib',
    '.mp3', '.mp4', '.wav', '.avi', '.mov',
    '.db', '.sqlite', '.mdb'
}

# Common file type descriptions
FILE_TYPE_DESCRIPTIONS = {
    '.py': 'Python source code file',
    '.js': 'JavaScript source code file',
    '.jsx': 'React JavaScript component file',
    '.ts': 'TypeScript source code file',
    '.tsx': 'React TypeScript component file',
    '.json': 'JSON configuration or data file',
    '.md': 'Markdown documentation file',
    '.txt': 'Plain text file',
    '.html': 'HTML web page file',
    '.css': 'CSS stylesheet file',
    '.scss': 'SASS stylesheet file',
    '.yaml': 'YAML configuration file',
    '.yml': 'YAML configuration file',
    '.sh': 'Shell script file',
    '.bat': 'Windows batch script file',
    '.gitignore': 'Git ignore rules file',
    '.env': 'Environment variables file',
    'package.json': 'Node.js package configuration and dependencies',
    'requirements.txt': 'Python package dependencies file',
    'Dockerfile': 'Docker container build instructions',
    'README.md': 'Project documentation and overview',
    'LICENSE': 'Project license terms',
    '.prettierrc': 'Prettier code formatter configuration',
    '.eslintrc': 'ESLint code linter configuration',
    'tsconfig.json': 'TypeScript compiler configuration',
    'next.config.js': 'Next.js framework configuration',
    'webpack.config.js': 'Webpack bundler configuration'
}

def debug_print(*args, **kwargs):
    """Print debug messages only when DEBUG is True"""
    if DEBUG:
        print(*args, **kwargs)

def load_gitignore_patterns(base_dir):
    """Load and parse .gitignore patterns using pathspec."""
    gitignore_path = os.path.join(base_dir, ".gitignore")
    if not os.path.exists(gitignore_path):
        return None

    try:
        with open(gitignore_path, "r", encoding="utf-8") as f:
            patterns = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Handle patterns with leading slashes
                    if line.startswith('/'):
                        line = line[1:]  # Remove leading slash
                    patterns.append(line)
        debug_print("\nDEBUG: Loaded .gitignore patterns:")
        for pattern in patterns:
            debug_print(f"  - {pattern}")
        return PathSpec.from_lines("gitwildmatch", patterns)
    except Exception as e:
        print(f"Warning: Error reading .gitignore: {e}")
        return None

# Initialize gitignore spec
GITIGNORE_SPEC = load_gitignore_patterns(BASE_DIR)

def is_git_path(path):
    """Check if a path starts with .git"""
    path_parts = path.split(os.sep)
    return any(part.startswith('.git') for part in path_parts)

def is_ignored(file_path):
    """Check if a path should be ignored based on .gitignore patterns and Git paths."""
    # Get relative path once and normalize it
    rel_path = os.path.relpath(file_path, BASE_DIR)
    
    # First check if it's a Git path
    if is_git_path(rel_path):
        debug_print(f"DEBUG: Ignoring Git path: {rel_path}")
        return True
        
    # Then check gitignore patterns
    if GITIGNORE_SPEC:
        # Try multiple path formats to ensure proper matching
        paths_to_try = [
            rel_path,                    # normal relative path
            '/' + rel_path,             # with leading slash
            rel_path.replace('\\', '/'), # normalize windows paths
            '/' + rel_path.replace('\\', '/') # normalized with leading slash
        ]
        
        for path in paths_to_try:
            if GITIGNORE_SPEC.match_file(path):
                debug_print(f"DEBUG: Ignoring gitignored path: {rel_path} (matched as {path})")
                return True
    return False

# File Analysis Functions
# ----------------------

def is_text_file(file_path):
    try:
        ext = os.path.splitext(file_path)[1].lower()
        if ext in BINARY_EXTENSIONS:
            return False
        if os.path.getsize(file_path) > FILE_SIZE_LIMIT:
            return False
        mime_type = mimetypes.guess_type(file_path)[0]
        if mime_type and not mime_type.startswith('text/'):
            return False
        with open(file_path, 'rb') as f:
            chunk = f.read(512)
            try:
                chunk.decode('utf-8')
                return True
            except UnicodeDecodeError:
                return False
    except Exception:
        return False

def get_ai_description(file_path, file_name, content=None):
    """Generate an AI-like description based on file type and name"""
    # First check for exact filename matches
    if file_name in FILE_TYPE_DESCRIPTIONS:
        return FILE_TYPE_DESCRIPTIONS[file_name]
        
    # Then check file extension
    ext = os.path.splitext(file_name)[1].lower()
    if ext in FILE_TYPE_DESCRIPTIONS:
        return FILE_TYPE_DESCRIPTIONS[ext]
        
    # For unknown files, try to make an educated guess
    if not ext:  # No extension
        if file_name.lower().startswith('readme'):
            return 'Project documentation file'
        if file_name.lower().startswith('license'):
            return 'Project license file'
        if file_name.lower().startswith('dockerfile'):
            return 'Docker container configuration'
        return 'Configuration or data file'
        
    return f'File with {ext} extension'

def get_file_metadata(file_path):
    """Get file metadata including both extracted and AI-generated descriptions"""
    try:
        file_name = os.path.basename(file_path)
        metadata = {
            "modified": datetime.fromtimestamp(os.path.getmtime(file_path)).isoformat(),
            "type": os.path.splitext(file_path)[-1].lower(),
            "ai_description": get_ai_description(file_path, file_name),
            "extracted_description": ""
        }
        
        # Get file size
        try:
            size = os.path.getsize(file_path)
            if size == 0:
                metadata["extracted_description"] = "(Empty file)"
                return metadata
        except:
            metadata["extracted_description"] = "(Error reading file)"
            return metadata
            
        if is_text_file(file_path):
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.readline()
                    if content.strip():
                        metadata["extracted_description"] = content.replace("\n", " ").strip()[:100]
                    else:
                        metadata["extracted_description"] = "(Empty content)"
            except Exception:
                metadata["extracted_description"] = "(Unreadable content)"
        else:
            metadata["extracted_description"] = "(Binary file)"
            
        return metadata
    except Exception as e:
        return {
            "modified": "",
            "type": "",
            "ai_description": "Unknown file type",
            "extracted_description": f"(Error: {str(e)})"
        }

def generate_repo_schema(base_dir):
    schema = {
        "project": "UltraRepo Documentation",
        "version": "1.0",
        "taxonomy": [],
        "files_scanned": 0,
        "files_processed": 0
    }
    
    for root, dirs, files in os.walk(base_dir, topdown=True):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d))]
        
        rel_root = os.path.relpath(root, base_dir)
        if is_ignored(root):
            continue
            
        entry = {
            "folder": rel_root,
            "files": [],
            "subfolders": dirs
        }
        
        # Filter and process files
        for file in files:
            file_path = os.path.join(root, file)
            schema["files_scanned"] += 1
            
            if is_ignored(file_path):
                continue
                
            schema["files_processed"] += 1
            
            # Print progress indicator
            sys.stdout.write(f"\rFiles Scanned: {schema['files_scanned']} | Files Processed: {schema['files_processed']}")
            sys.stdout.flush()
            
            rel_path = os.path.relpath(file_path, base_dir)
            entry["files"].append({
                "name": file,
                "path": rel_path,
                "metadata": get_file_metadata(file_path)
            })
        
        if entry["files"]:
            schema["taxonomy"].append(entry)
    
    print("\n")  # New line after progress indicator
    return schema

def format_metadata(file, file_prefix):
    """Helper function to format file metadata"""
    metadata = file['metadata']
    # Use the same prefix as the file node plus additional indentation
    indent = file_prefix + "    "  # Four spaces for alignment
    meta_str = ""
    meta_str += f"{indent}Type: {metadata['type']}\n"
    meta_str += f"{indent}Modified: {metadata['modified']}\n"
    meta_str += f"{indent}Description: {metadata['ai_description']}\n"
    if metadata['extracted_description']:
        meta_str += f"{indent}Content: {metadata['extracted_description']}\n"
    return meta_str

def format_tree(entries, prefix=""):
    tree = ""
    base_indent = "    "  # Base indentation for all items
    
    # Sort entries by folder path alphabetically
    folder_entries = sorted([entry for entry in entries if entry['folder'] != '.'], 
                          key=lambda x: x['folder'].lower())
    root_files_entry = next((entry for entry in entries if entry['folder'] == '.'), None)
    
    # Track processed paths to avoid duplicates
    processed_paths = set()
    
    # Helper function to add folder structure
    def add_folder_structure(path, current_prefix=""):
        if path in processed_paths:
            return ""
        
        parts = path.split(os.sep)
        result = ""
        current_path = ""
        
        for i, part in enumerate(parts):
            if not part:
                continue
                
            current_path = os.path.join(current_path, part) if current_path else part
            full_path = os.path.join(BASE_DIR, current_path)
            
            if is_ignored(full_path):
                return ""
                
            if current_path in processed_paths:
                continue
            
            processed_paths.add(current_path)
            indent = base_indent + "    " * i
            result += f"{current_prefix}{indent}📁 {part}\n"
        
        return result
    
    # Process folders hierarchically
    for entry in folder_entries:
        folder_path = os.path.join(BASE_DIR, entry['folder'])
        if is_ignored(folder_path):
            continue
            
        # Add folder structure
        tree += add_folder_structure(entry['folder'])
        
        # Add files with metadata (sorted alphabetically)
        if entry['files']:
            files = sorted(entry['files'], key=lambda x: x['name'].lower())
            folder_depth = entry['folder'].count(os.sep) + 2  # Add 1 for base indentation
            file_prefix = "    " * folder_depth
            
            for idx, file in enumerate(files):
                file_path = os.path.join(BASE_DIR, file['path'])
                if is_ignored(file_path):
                    continue
                is_last_file = idx == len(files) - 1
                tree += f"{file_prefix}{'└── ' if is_last_file else '├── '}📄 {file['name']}\n"
                # Add metadata indented under the file
                tree += format_metadata(file, file_prefix)
    
    # Process root-level files (sorted alphabetically)
    if root_files_entry and root_files_entry['files']:
        tree += f"\n{base_indent}📁 ./\n"  # Add base indentation
        files = sorted(root_files_entry['files'], key=lambda x: x['name'].lower())
        file_prefix = base_indent + "    "  # One level deeper than base
        for idx, file in enumerate(files):
            file_path = os.path.join(BASE_DIR, file['path'])
            if is_ignored(file_path):
                continue
            is_last = idx == len(files) - 1
            tree += f"{file_prefix}{'└── ' if is_last else '├── '}📄 {file['name']}\n"
            # Add metadata indented under the file
            tree += format_metadata(file, file_prefix)
    
    return tree

def generate_markdown(schema):
    markdown = f"# {schema['project']} v{schema['version']}\n\n"
    markdown += "## Project Structure with Details\n\n"
    
    # Generate the enhanced tree structure with embedded metadata
    markdown += format_tree(schema['taxonomy'])
    
    return markdown

def main():
    """Main execution function"""
    print("\nWelcome to Repo Schema, a tool to chart details of your repository.")
    print("Repo Schema will scan and parse all files in your repo.")
    print("To exclude a directory, add it to the .GITIGNORE file at the root of your repo.")
    
    response = input("Proceed to scan and parse all files? [Y/N]: ")
    if response.lower() != 'y':
        print("Operation cancelled.")
        sys.exit(0)

    print("\nStarting repository analysis...")
    schema = generate_repo_schema(BASE_DIR)
    
    # Generate JSON output
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2)
    
    # Generate Markdown output
    markdown_content = generate_markdown(schema)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    
    print(f"\n\nTask completed:")
    print(f"  [{schema.get('files_scanned', 0)}] Files Scanned | [{schema.get('files_processed', 0)}] Files Parsed")
    print(f"View output files at:")
    print(f"  - {os.path.basename(OUTPUT_JSON)}")
    print(f"  - {os.path.basename(OUTPUT_MD)}")

if __name__ == "__main__":
    main()

