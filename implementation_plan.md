# Implementation Plan - MCP Spreadsheet Sandbox

## Goal
Build a safe, sandboxed RL environment where AI agents can perform spreadsheet tasks in LibreOffice/Python, interacting via the Model Context Protocol (MCP).

## Architecture

### 1. The Sandbox (Docker)
- **Image**: `python:3.11-slim`
- **Dependencies**:
    - `libreoffice` (for spreadsheet operations if needed, though `odfpy`/`pandas` might be sufficient for the programmatic mode, the prompt mentions LibreOffice is pre-installed).
    - Python libs: `odfpy`, `pandas`, `openpyxl`, `pyexcel-ods`.
- **Execution**: The container will be started for a task. The MCP server will use `docker exec` to run commands and Python scripts inside.
- **Persistence**: A temporary directory will be mounted or we will just copy files in/out using `docker cp`. Given the "Sandboxed environments that reset" requirement, ephemeral containers are best.

### 2. The MCP Server (Python)
- **Library**: `mcp` (Python SDK).
- **Transport**: Stdio (standard for local MCP servers).
- **Tools**:
    - `server.get_manifest()`: Returns task config.
    - `server.get_task_files()`: Lists/copies starter files.
    - `sandbox.run_python(code)`: Executes Python code in the container.
    - `sandbox.read_file(path)`: Reads file from container.
    - `sandbox.write_file(path, content)`: Writes file to container.
    - `sandbox.list_directory(path)`: Lists files in container.
    - `grader.grade(submission_path)`: Runs the grading script.

### 3. Task Structure
- **Location**: `tasks/<task_name>/`
- **Files**:
    - `manifest.json`: Metadata (problem statement, expected output).
    - `grader.py`: Logic to validate the submission.
    - `*.ods`: Starter files.

## Proposed Changes

### [Infrastructure]
#### [NEW] [Dockerfile](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/Dockerfile)
- Defines the sandbox environment.

#### [NEW] [server.py](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/server.py)
- Main MCP server implementation.
- Handles Docker container lifecycle (start on init, destroy on exit/timeout).

#### [NEW] [sandbox.py](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/sandbox.py)
- Helper class to manage Docker interactions (exec, cp, etc.).

### [Task Data]
#### [NEW] [tasks/banking/manifest.json](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/tasks/banking/manifest.json)
#### [NEW] [tasks/banking/grader.py](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/tasks/banking/grader.py)
#### [NEW] [tasks/banking/cash_flows.ods](file:///Users/devpatel/.gemini/antigravity/scratch/mcp-spreadsheet-sandbox/tasks/banking/cash_flows.ods)
- We will generate a dummy ODS file for testing.

## Verification Plan
1. **Build Docker Image**: Ensure it builds correctly.
2. **Start MCP Server**: Run locally.
3. **Test Tools**:
    - Use an MCP client (or a script mocking one) to call `server.get_manifest`.
    - Call `sandbox.run_python` to modify a spreadsheet.
    - Call `grader.grade` to verify.
