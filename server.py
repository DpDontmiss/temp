from mcp.server.fastmcp import FastMCP
from sandbox import Sandbox
import os
import json
import shutil
import subprocess

# Initialize Sandbox
sandbox = Sandbox()
sandbox.start()

# Initialize MCP Server
mcp = FastMCP("mcp-sandboxed-spreadsheets")

# Constants
TASKS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks")
CURRENT_TASK = "banking"  # Default task

def get_task_dir(task_name):
    return os.path.join(TASKS_DIR, task_name)

@mcp.tool()
def get_manifest() -> str:
    """Returns the task configuration and manifest."""
    task_dir = get_task_dir(CURRENT_TASK)
    manifest_path = os.path.join(task_dir, "manifest.json")
    
    if not os.path.exists(manifest_path):
        return json.dumps({"error": "Manifest not found"})
        
    with open(manifest_path, "r") as f:
        return f.read()

@mcp.tool()
def get_task_files() -> str:
    """Lists and copies starter files to the sandbox."""
    task_dir = get_task_dir(CURRENT_TASK)
    files = []
    
    # Copy all files from task dir to sandbox
    for filename in os.listdir(task_dir):
        if filename in ["manifest.json", "grader.py"]:
            continue # Don't expose these directly if not needed, or maybe we do?
            # The prompt says "Returns all starter files". 
            # Usually we don't give the grader to the agent.
        
        local_path = os.path.join(task_dir, filename)
        if os.path.isfile(local_path):
            remote_path = f"/sandbox/{filename}"
            sandbox.copy_to(local_path, remote_path)
            files.append(remote_path)
            
    return json.dumps({"files": files})

@mcp.tool()
def run_python(code: str) -> str:
    """Executes Python code inside the sandbox."""
    stdout, stderr, returncode = sandbox.run_python(code)
    return json.dumps({
        "stdout": stdout,
        "stderr": stderr,
        "returncode": returncode
    })

@mcp.tool()
def read_file(path: str) -> str:
    """Reads a file from the sandbox."""
    try:
        content = sandbox.read_file(path)
        return content
    except Exception as e:
        return f"Error reading file: {str(e)}"

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Writes a file to the sandbox."""
    try:
        sandbox.write_file(path, content)
        return "Success"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool()
def list_directory(path: str = ".") -> str:
    """Lists directory contents in the sandbox."""
    try:
        return sandbox.list_dir(path)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@mcp.tool()
def grade(submission_path: str) -> str:
    """Validates the submission."""
    task_dir = get_task_dir(CURRENT_TASK)
    grader_path = os.path.join(task_dir, "grader.py")
    
    if not os.path.exists(grader_path):
        return json.dumps({"status": "error", "message": "Grader not found"})
        
    # Copy submission from sandbox to local temp
    local_submission = os.path.join(task_dir, "submission_temp.ods")
    try:
        sandbox.copy_from(submission_path, local_submission)
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Could not retrieve submission: {str(e)}"})
        
    # Run grader locally
    # The grader should take the submission path as an argument or we can modify it to do so.
    # Assuming grader.py has a main function or we run it as a script.
    # We'll pass the submission path and task dir (for oracle) as env vars or args.
    
    try:
        cmd = ["python3", grader_path, "--submission", local_submission, "--task-dir", task_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        # Clean up
        if os.path.exists(local_submission):
            os.remove(local_submission)
            
        if result.returncode == 0:
            # Try to parse JSON output from grader if possible, or just return stdout
            try:
                return json.dumps(json.loads(result.stdout))
            except:
                return json.dumps({"status": "pass", "output": result.stdout})
        else:
            return json.dumps({"status": "fail", "output": result.stdout, "error": result.stderr})
            
    except Exception as e:
        return json.dumps({"status": "error", "message": f"Grading failed: {str(e)}"})

if __name__ == "__main__":
    mcp.run()
