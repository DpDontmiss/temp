This project is a small MCP-based environment for spreadsheet tasks.

An MCP server (`server.py`) exposes tools that let an external agent:
- read the task manifest,
- copy starter files into an isolated `/sandbox` filesystem,
- run Python code against those files,
- and call a grader to check the result.

The example task lives in `tasks/banking/` and asks the agent to add a `Reserve = Amount * 0.1` column to an ODS file. The grader compares the submission against the original data and returns a simple JSON status (`pass` / `fail`), which can be used as a reward signal or just as a correctness check.