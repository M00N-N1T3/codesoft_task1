# To-do list

## Table of Contents

- [To-do list](#to-do-list)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Commands and Features](#commands-and-features)
  - [Installation](#installation)
  - [Execution](#execution)
  - [Libraries](#libraries)
  - [Contributors](#contributors)

## Overview

A Todo List is a basic yet highly effective project for managing tasks. It allows users to create, read, update, and delete tasks, helping them organize their daily activities efficiently. The project typically includes the following [features](#commands-and-features):

## Commands and Features

Each command has feature of its own. By running the commands you gain access to its relevant feature

1. **Add-task** : The user can add new tasks to the list
2. **Change-status** : Change the status of a task
3. **Create-file** : Create a new todo_list file
4. **Delete-file** : Delete an existing task file
5. **Delete-task** : Delete an existing task
6. **List-all** : List all available todo lists
7. **Update-task** : Update an existing task.
8. **View-tasks** : Displays tasks from a selected todo_list

## Installation

1. Clone the Repository :

    ```bash
    git clone https://github.com/M00N-N1T3/codsoft_task1.git
    cd codsoft_task1
    ```

## Execution

```python
python3 app.py [command]
```

Alternatively you can run the commands with flags followed by your instruction / input.

```python
python3 app.py [command] [flag] ["instruction"]
```

- The available [commands](#commands-and-features).
- Each command comes with a set of its own flags. You can run the --help flag to gain more insight on each command.

    ```python
    python3 app.py [command] --help
    ```

## Libraries

- click - for the CLI (command line interface) design
- tabulate - used for displaying content in a neat manner on the terminal

You do not need to install this modules manually as they are all provided in the [lib](lib) package.

## Contributors

Should you wish to contribute to this project. All external modules should be added to the [lib](lib) package and referenced correctly when importing.
