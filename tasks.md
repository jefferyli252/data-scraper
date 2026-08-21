
# 12, August, 2026

- [ ]  Read about `.gitignore` files, how it works and why you should use it in your project. (https://www.freecodecamp.org/news/gitignore-file/)
- [ ]  Read about MARKDOWN: https://daringfireball.net/projects/markdown/
    - [ ] Benefits
    - [ ]  Why AI using it
    - [ ]  What are the option of formatting
    - [ ]  What is the difference between `Markup` and `Markdown`
- [ ] Read about Docker containers:
  - [ ] What is it?
  - [ ] How to create a docker image?
  - [ ] What is `Docker Compose`?
  - [ ] When to use `docker compose`?
- Make an additional files in the project:
  - [ ] `gitignore` with files which should not be added to `git`.
  - [ ] Create `docker-compose.yml` file for deployment with correct information for deployment.

# 27, July, 2026

- [ ]  Learn about dependencies and how to install them in Python: (it's very similar to `nodejs`)
    - [ ]  `requirements.txt` file is used to list all the dependencies required for a Python project. It allows you to specify the packages and their versions that your project needs to run correctly. This file can be used with package managers like pip to install the listed dependencies easily.
- [ ]  `uv` module is a Python library that provides an interface for working with the libuv library, which is a multi-platform support library with a focus on asynchronous I/O. The uv module allows you to perform non-blocking I/O operations, such as file and network operations, in a more efficient manner.

`System design`:
    - [ ]  Select the right architecture for your project based on its requirements and scalability needs. Consider factors such as performance, maintainability, and security when designing the system.
    - [ ]  Which LLM models are suitable to `planning`, `coding`, `testing`.
        - [ ] https://www.youtube.com/watch?v=pYax2rupKEY

- [ ]  **Add** a changelog.md file to track changes and updates to the project.
- [ ]  Make a `tasks.md` file to list all the tasks and their status (e.g., pending, in progress, completed) for better project management and organization.

Technical details:
- [ ]  Create new `branch` and checkout to it before making any changes to the codebase. This allows for better version control and collaboration among team members.
- [ ]  Make a better structure for expanding your codebase in the future. Organize your code into modules, packages, and directories to improve maintainability and readability.

Example:
```
root
    |- src
    |   |- tools <-- store all your tools, such as fetching the data, organizing data, more small scripts to do small tasks.
    |   |- tests (optional for now) <-- writen test scripts that are responsible of executing automated test cases, similar to `src` folder, but for tests.
    |   |- ... <-- you can add `infra/` directory to store all your logics, which is: classes, functions, logical scripts, etc.
    |- docs
    |- resources <-- json files, html static contents, etc.
    |- .gitignore
    |- requirements.txt
    |- main.py
    |- README.md
    |- tasks.md
    ```

> Note: Do the above tests using WSL2 (linux) and not Windows. It will help you to learn Linux commands and make your project more compatible with Linux-based systems.
