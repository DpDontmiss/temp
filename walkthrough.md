# MCP Spreadsheet Sandbox Walkthrough

I have implemented a sandboxed environment for AI agents to perform spreadsheet tasks using the Model Context Protocol (MCP).

## Architecture

1.  **MCP Server (`server.py`)**:
    *   Exposes tools for agents to interact with the sandbox.
    *   Tools: `get_manifest`, `get_task_files`, `run_python`, `read_file`, `write_file`, `list_directory`, `grade`.
    *   Uses `mcp` Python SDK (FastMCP).

2.  **Sandbox (`sandbox.py`)**:
    *   Manages the execution environment.
    *   **Note**: Due to Docker unavailability in the current environment, I implemented a **mock sandbox** using local temporary directories. This preserves the interface and logic but runs locally.
    *   The `Dockerfile` is provided for the "real" production environment.

3.  **Task Definition (`tasks/banking/`)**:
    *   `manifest.json`: Defines the "Banking Reserve Calculation" task.
    *   `cash_flows.ods`: Generated input data.
    *   `grader.py`: Validates the agent's submission.

## How to Run

### Prerequisites
*   Python 3.11+
*   `mcp`, `pandas`, `odfpy`

### Steps

1.  **Install Dependencies**:
    ```bash
    pip install mcp pandas odfpy
    ```

2.  **Generate Data**:
    ```bash
    python3 generate_data.py
    ```

3.  **Run the Test Agent**:
    I created a `test_agent.py` that simulates an AI agent. It connects to the server, reads the task, solves it using `pandas`, and submits it for grading.
    ```bash
    python3 test_agent.py
    ```

### Expected Output
The test agent should output:
```
--- Step 1: Get Manifest ---
Manifest: { ... }

--- Step 2: Get Task Files ---
Files: {"files": ["/sandbox/cash_flows.ods"]}

--- Step 3: Solving Task ---
Execution Result: {"stdout": "Solution saved to solutions/solution.ods\n", ...}

--- Step 4: Grading ---
Grade Result: {"status": "pass"}
```

## Files Created
*   `mcp-spreadsheet-sandbox/`
    *   `server.py`: The MCP server.
    *   `sandbox.py`: Sandbox abstraction (Mock implementation).
    *   `Dockerfile`: For real Docker deployment.
    *   `generate_data.py`: Data generator.
    *   `test_agent.py`: End-to-end verification script.
    *   `tasks/banking/`: Task files.
    *   `README.md`: Task description.
