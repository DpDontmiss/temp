import subprocess
import uuid
import os
import tempfile
import shutil
from typing import Optional, Tuple

class Sandbox:
    def __init__(self, image_name: str = "mcp-sandbox"):
        self.image_name = image_name
        self.container_name = f"sandbox-{uuid.uuid4().hex[:8]}"
        self.is_running = False
        self.sandbox_dir = None

    def start(self):
        """Starts the sandbox (creates a temp dir)."""
        if self.is_running:
            return

        self.sandbox_dir = tempfile.mkdtemp(prefix="mcp-sandbox-")
        print(f"Started local sandbox at {self.sandbox_dir}")
        self.is_running = True

    def stop(self):
        """Stops the sandbox (removes temp dir)."""
        if not self.is_running:
            return
        
        if self.sandbox_dir and os.path.exists(self.sandbox_dir):
            shutil.rmtree(self.sandbox_dir)
        self.is_running = False

    def run_python(self, code: str) -> Tuple[str, str, int]:
        """Runs python code in the sandbox."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")

        # Write code to a file in the sandbox
        script_path = os.path.join(self.sandbox_dir, "script.py")
        with open(script_path, "w") as f:
            f.write(code)

        # Execute
        # We run in the sandbox dir
        cmd = [sys.executable, "script.py"]
        result = subprocess.run(cmd, cwd=self.sandbox_dir, capture_output=True, text=True)
        return result.stdout, result.stderr, result.returncode

    def copy_to(self, local_path: str, remote_path: str):
        """Copies a local file to the sandbox."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")
        
        # Handle /sandbox/ prefix
        if remote_path.startswith("/sandbox/"):
            rel_path = remote_path[len("/sandbox/"):]
        else:
            rel_path = remote_path.lstrip("/")
            
        dest_path = os.path.join(self.sandbox_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        shutil.copy2(local_path, dest_path)

    def copy_from(self, remote_path: str, local_path: str):
        """Copies a file from the sandbox to local."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")
            
        # Handle /sandbox/ prefix
        if remote_path.startswith("/sandbox/"):
            rel_path = remote_path[len("/sandbox/"):]
        else:
            rel_path = remote_path.lstrip("/")
            
        src_path = os.path.join(self.sandbox_dir, rel_path)
        shutil.copy2(src_path, local_path)

    def list_dir(self, path: str) -> str:
        """Lists directory contents in the sandbox."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")
            
        # Handle /sandbox/ prefix
        if path.startswith("/sandbox/"):
            rel_path = path[len("/sandbox/"):]
        else:
            rel_path = path.lstrip("/")
        
        target_dir = os.path.join(self.sandbox_dir, rel_path)
        if not os.path.exists(target_dir):
            return f"Directory not found: {path}"
            
        cmd = ["ls", "-R", target_dir]
        result = subprocess.run(cmd, capture_output=True, text=True)
        return result.stdout

    def read_file(self, remote_path: str) -> str:
        """Reads a text file from the sandbox."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")
            
        # Handle /sandbox/ prefix
        if remote_path.startswith("/sandbox/"):
            rel_path = remote_path[len("/sandbox/"):]
        else:
            rel_path = remote_path.lstrip("/")
            
        src_path = os.path.join(self.sandbox_dir, rel_path)
        with open(src_path, "r") as f:
            return f.read()

    def write_file(self, remote_path: str, content: str):
        """Writes text content to a file in the sandbox."""
        if not self.is_running:
            raise RuntimeError("Sandbox is not running")
            
        # Handle /sandbox/ prefix
        if remote_path.startswith("/sandbox/"):
            rel_path = remote_path[len("/sandbox/"):]
        else:
            rel_path = remote_path.lstrip("/")
            
        dest_path = os.path.join(self.sandbox_dir, rel_path)
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        with open(dest_path, "w") as f:
            f.write(content)

import sys
