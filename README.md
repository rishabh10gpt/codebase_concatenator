# Codebase Concatenator for LLM

A Python utility that prepares your codebase for Large Language Model (LLM) processing by concatenating all source files with their relative paths as comments.

## Features

- **Smart file detection**: Automatically processes common source code files
- **Language-aware comments**: Uses appropriate comment syntax for each file type
- **Intelligent filtering**: Ignores build artifacts, dependencies, and environment files
- **Cross-platform**: Works on Windows, macOS, and Linux
- **Flexible output**: Output to stdout or save to file

## Quick Start

```bash
# Process current directory
python codebase_concatenator.py

# Process specific directory and save to file
python codebase_concatenator.py /path/to/project -o project_code.txt

# Only include specific file types
python codebase_concatenator.py --ext .py .js .md
```

## What Gets Ignored

**Python projects:**
- `__pycache__`, `env`, `venv`, `.venv`, `dist`, `build`
- Virtual environments and build artifacts

**JavaScript/Node.js projects:**
- `node_modules`, `.npm`, `.yarn`, `dist`, `build`, `.next`
- Package manager artifacts and build outputs

**General:**
- `.env` files, `.git`, `.DS_Store`, `.vscode`, log files
- Hidden directories and temporary files

## Comment Styles

The tool automatically uses the correct comment syntax:

```python
# File: src/main.py
def hello_world():
    print("Hello, World!")
```

```javascript
// File: src/app.js
function helloWorld() {
    console.log("Hello, World!");
}
```

```html
<!-- File: public/index.html -->
<!DOCTYPE html>
<html>...
```

## Command Line Options

```
positional arguments:
  directory             Directory to process (default: current directory)

options:
  -h, --help           Show help message
  -o, --output FILE    Output file (default: stdout)
  --ext EXT [EXT ...]  File extensions to include (e.g., .py .js .md)
  --all-ext            Process all text files regardless of extension
```

## Examples

```bash
# Basic usage - current directory to stdout
python codebase_concatenator.py

# Specific directory with output file
python codebase_concatenator.py ~/my-project -o codebase.txt

# Only Python and JavaScript files
python codebase_concatenator.py --ext .py .js .jsx .ts

# All text files in a directory
python codebase_concatenator.py /path/to/docs --all-ext
```

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only standard library)

## Installation

Simply download `codebase_concatenator.py` and run it with Python. No installation required!

## Use Cases

- Preparing code for LLM analysis or refactoring
- Creating comprehensive code reviews
- Generating documentation from source code
- Code backup and archival
- Sharing entire codebases in a single file
