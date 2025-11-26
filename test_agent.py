import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Path to server.py
SERVER_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "server.py")

async def run():
    # Start the server
    server_params = StdioServerParameters(
        command=sys.executable,
        args=[SERVER_PATH],
        env=os.environ.copy()
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # 1. Get Manifest
            print("\n--- Step 1: Get Manifest ---")
            manifest = await session.call_tool("get_manifest", {})
            print(f"Manifest: {manifest.content[0].text}")

            # 2. Get Task Files
            print("\n--- Step 2: Get Task Files ---")
            files = await session.call_tool("get_task_files", {})
            print(f"Files: {files.content[0].text}")

            # 3. Solve Task
            print("\n--- Step 3: Solving Task ---")
            # We'll write a script to calculate reserves
            solution_code = """
import pandas as pd
import os

# Read input
input_path = "cash_flows.ods"
df = pd.read_excel(input_path, engine="odf")

# Calculate Reserve
df["Reserve"] = df["Amount"] * 0.1

# Save output
os.makedirs("solutions", exist_ok=True)
output_path = "solutions/solution.ods"
df.to_excel(output_path, engine="odf", index=False)
print("Solution saved to", output_path)
"""
            result = await session.call_tool("run_python", {"code": solution_code})
            print(f"Execution Result: {result.content[0].text}")

            # 4. Grade
            print("\n--- Step 4: Grading ---")
            grade_result = await session.call_tool("grade", {"submission_path": "solutions/solution.ods"})
            print(f"Grade Result: {grade_result.content[0].text}")

if __name__ == "__main__":
    asyncio.run(run())
