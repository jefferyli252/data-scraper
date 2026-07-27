
# 27, July, 2026
- Learn about dependencies and how to install them in Python: (it's very similar to `nodejs`)
    - `requirements.txt` file is used to list all the dependencies required for a Python project. It allows you to specify the packages and their versions that your project needs to run correctly. This file can be used with package managers like pip to install the listed dependencies easily.
- `uv` module is a Python library that provides an interface for working with the libuv library, which is a multi-platform support library with a focus on asynchronous I/O. The uv module allows you to perform non-blocking I/O operations, such as file and network operations, in a more efficient manner.

`System design`:
    - Select the right architecture for your project based on its requirements and scalability needs. Consider factors such as performance, maintainability, and security when designing the system.
    - Which LLM models are suitable to `planning`, `coding`, `testing`.

- **Add** a changelog.md file to track changes and updates to the project.
- Make a `tasks.md` file to list all the tasks and their status (e.g., pending, in progress, completed) for better project management and organization.

Technical details:
- Create new `branch` and checkout to it before making any changes to the codebase. This allows for better version control and collaboration among team members.
- Make a better structure for expanding your codebase in the future. Organize your code into modules, packages, and directories to improve maintainability and readability.
    ```
root
    |- src
    |   |- tools
    |   |- tests (optional for now)
    |   |- ...
    |- docs
    |- resources
    |- .gitignore
    |- requirements.txt
    |- main.py
    |- README.md
    |- tasks.md
    ```

> Note: Do the above tasts using WSL2 (linux) and not Windows. It will help you to learn Linux commands and make your project more compatible with Linux-based systems.
