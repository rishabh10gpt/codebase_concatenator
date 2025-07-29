#!/usr/bin/env python3
"""
Codebase Concatenator for LLM
Concatenates source files with commented file paths for LLM processing.
Supports Python and JavaScript projects with appropriate exclusions.
"""

import os
import sys
import argparse
from pathlib import Path

# Default extensions to include
DEFAULT_EXTENSIONS = {
    '.py', '.js', '.jsx', '.ts', '.tsx', '.json', '.md', '.yaml', '.yml',
    '.html', '.css', '.scss', '.sass', '.less', '.sql', '.sh', '.bat', '.ps1',
    '.dockerfile', '.gitignore', '.gitattributes', '.editorconfig'
}

# Directories and files to ignore
IGNORE_PATTERNS = {
    # Python
    '__pycache__', '.pytest_cache', 'env', 'venv', '.venv', '.env', 'ENV',
    'env.bak', 'venv.bak', '.Python', 'build', 'develop-eggs', 'dist',
    'downloads', 'eggs', '.eggs', 'lib', 'lib64', 'parts', 'sdist', 'var',
    'wheels', '*.egg-info', '.installed.cfg', '*.egg', 'MANIFEST',
    
    # JavaScript/Node.js
    'node_modules', '.npm', '.yarn', 'yarn-error.log', '.pnp', '.pnp.js',
    'coverage', '.nyc_output', '.grunt', 'bower_components', '.bower-cache',
    '.sass-cache', '.cache', '.parcel-cache', '.next', '.nuxt', 'dist',
    'build', 'out',
    
    # General
    '.git', '.svn', '.hg', '.DS_Store', 'Thumbs.db', '.vscode', '.idea',
    '.vs', '*.swp', '*.swo', '*~', '.tmp', '.temp', 'logs', '*.log',
    '.env', '.env.local', '.env.development.local', '.env.test.local',
    '.env.production.local'
}

# Files to ignore
IGNORE_FILES = {
    '.env', '.env.local', '.env.development', '.env.production', '.env.test',
    '.env.development.local', '.env.test.local', '.env.production.local',
    'package-lock.json', 'yarn.lock', 'poetry.lock', 'Pipfile.lock'
}

def get_comment_style(file_path):
    """Get appropriate comment style based on file extension."""
    ext = file_path.suffix.lower()
    
    if ext in {'.py', '.sh', '.yml', '.yaml', '.dockerfile'}:
        return '#'
    elif ext in {'.js', '.jsx', '.ts', '.tsx', '.css', '.scss', '.sass', '.less', '.sql'}:
        return '//'
    elif ext in {'.html', '.xml'}:
        return '<!-- {} -->'
    elif ext in {'.md', '.txt'}:
        return '#'
    else:
        return '#'  # Default to hash

def should_ignore(path, base_path):
    """Check if path should be ignored based on ignore patterns."""
    rel_path = path.relative_to(base_path)
    
    # Check if any part of the path matches ignore patterns
    for part in rel_path.parts:
        if part in IGNORE_PATTERNS or part.startswith('.'):
            # Allow some dotfiles
            if part not in {'.gitignore', '.gitattributes', '.editorconfig'}:
                return True
    
    # Check if filename is in ignore list
    if path.name in IGNORE_FILES:
        return True
    
    # Check for wildcard patterns
    if any(pattern.startswith('*') and path.name.endswith(pattern[1:]) 
           for pattern in IGNORE_PATTERNS if '*' in pattern):
        return True
    
    return False

def is_text_file(file_path):
    """Check if file is likely a text file."""
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(1024)
            if b'\0' in chunk:  # Binary files often contain null bytes
                return False
        return True
    except:
        return False

def concatenate_files(directory, output_file=None, extensions=None):
    """
    Concatenate files from directory with commented file paths.
    
    Args:
        directory: Directory to scan
        output_file: Output file path (stdout if None)
        extensions: Set of file extensions to include
    """
    directory = Path(directory).resolve()
    extensions = extensions or DEFAULT_EXTENSIONS
    
    if not directory.exists():
        print(f"Error: Directory '{directory}' does not exist.", file=sys.stderr)
        return False
    
    if not directory.is_dir():
        print(f"Error: '{directory}' is not a directory.", file=sys.stderr)
        return False
    
    # Collect all files to process
    files_to_process = []
    
    for root, dirs, files in os.walk(directory):
        root_path = Path(root)
        
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not should_ignore(root_path / d, directory)]
        
        for file in files:
            file_path = root_path / file
            
            # Skip if should be ignored
            if should_ignore(file_path, directory):
                continue
            
            # Check extension
            if extensions and file_path.suffix.lower() not in extensions:
                continue
            
            # Check if it's a text file
            if not is_text_file(file_path):
                continue
            
            files_to_process.append(file_path)
    
    # Sort files for consistent output
    files_to_process.sort()
    
    # Open output file or use stdout
    output = open(output_file, 'w', encoding='utf-8') if output_file else sys.stdout
    
    try:
        total_files = len(files_to_process)
        print(f"Processing {total_files} files from '{directory}'...", file=sys.stderr)
        
        for i, file_path in enumerate(files_to_process, 1):
            try:
                rel_path = file_path.relative_to(directory)
                comment_style = get_comment_style(file_path)
                
                # Write file header
                if comment_style == '<!-- {} -->':
                    header = comment_style.format(f" File: {rel_path} ")
                else:
                    header = f"{comment_style} File: {rel_path}"
                
                output.write(f"{header}\n")
                
                # Write file content
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    output.write(content)
                    
                    # Ensure file ends with newline
                    if content and not content.endswith('\n'):
                        output.write('\n')
                
                # Add separator between files
                output.write('\n')
                
                if i % 10 == 0:  # Progress indicator
                    print(f"Processed {i}/{total_files} files...", file=sys.stderr)
                    
            except Exception as e:
                print(f"Warning: Could not process {file_path}: {e}", file=sys.stderr)
                continue
        
        print(f"Successfully processed {total_files} files.", file=sys.stderr)
        return True
        
    finally:
        if output_file:
            output.close()

def main():
    parser = argparse.ArgumentParser(
        description="Concatenate codebase files for LLM processing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s                          # Process current directory, output to stdout
  %(prog)s /path/to/project         # Process specific directory
  %(prog)s -o output.txt            # Save to file
  %(prog)s --ext .py .js .md        # Only process specific extensions
  %(prog)s --all-ext                # Process all text files
        """
    )
    
    parser.add_argument('directory', nargs='?', default='.', 
                       help='Directory to process (default: current directory)')
    parser.add_argument('-o', '--output', help='Output file (default: stdout)')
    parser.add_argument('--ext', nargs='+', metavar='EXT',
                       help='File extensions to include (e.g., .py .js .md)')
    parser.add_argument('--all-ext', action='store_true',
                       help='Process all text files regardless of extension')
    
    args = parser.parse_args()
    
    # Determine extensions to process
    if args.all_ext:
        extensions = None  # Process all text files
    elif args.ext:
        extensions = set(ext if ext.startswith('.') else f'.{ext}' for ext in args.ext)
    else:
        extensions = DEFAULT_EXTENSIONS
    
    # Process files
    success = concatenate_files(args.directory, args.output, extensions)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
