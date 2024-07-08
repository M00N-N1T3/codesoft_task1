from os import get_terminal_size
from lib import click, tabulate
from logic import logic
from logic.os_mod import DOWNLOADS, CWD, HOME,join, basename, exists, isfile, remove, listdir, mkdir


def main_path():
    """main path where all the todo_list files gets stored

    Returns:
        str : the path to the directory
    """
    return join(DOWNLOADS,"TaskIT")

def file_path(file:str ):
    """
    generates a string that contains the path and filename

    Args:
        file (str): the file we want to create/use

    Returns:
        str : the full path including the file name
    """
    file = f"{file}.txt" if not ".txt" in file else file
    return join(DOWNLOADS,"TaskIT",file)


PR_PROMPT = str(logic.PRIORITIES.values()).strip("dict_values()")
STATUS_PROMPT = str(logic.STATUS.values()).strip("dict_values()")
CONFIG_DIR = join(HOME,"betterMe")
MAIN_PATH = main_path()
clear_term ="\033c"


@click.group()
def main():
    return


@main.command(help ="Add a new task to your todo-list")
@click.option("-n","--name",prompt = "Enter task name", required = True,help = "task name")
@click.option("-d","--description", prompt ="Enter task description",help = "task description")
@click.option("-p","--priority", prompt ="Enter task priority" + PR_PROMPT,help = "task priority")
@click.option("-f","--file-name",default = "",help = "to-do_list filename")
def add_task(name: str,description:str ,priority: str, file_name:str ):
    """
    Adds a new task to our todo list
    Args:
        name (str):the task name
        description (str):task description
        priority (str): the priority of the task
        file_name (str, optional): todo_list file name if specified [Default = todo_list.txt]
    """

    if file_name == "":
        user_input = input(f"Enter file in which to save the todo list ({logic.DEFAULT_FILENAME}): ")
        if user_input == "":
            file_name = file_path(logic.DEFAULT_FILENAME)
        else:
            file_name = file_path(user_input)
    else:
        file_name = file_path(file_name)

    operation = logic.add_task(name,description,priority,file_name)

    result = "Successfully added" if operation else "Failed to add"
    message = f"{name} to {basename(file_name)}"

    tab = tabulate.tabulate([[f"{result} {message}"]],tablefmt="fancy_grid")
    print(tab)
    return


@main.command(help="update an existing task.")
@click.option("-i","--index",type=int,prompt = "Enter the task number",help="the index of the task you want to update")
@click.option("-n","--name",help="the new name if you wish to update the name of the task",default = "")
@click.option("-d","--description",help = "the new description for the task if you wish to change the task description",default="")
@click.option("-p","--priority",help=f"the new priority if you wish to update the task priority {PR_PROMPT}",default="")
@click.option("-f","--filename",prompt = f"Enter the name of the file",default =logic.DEFAULT_FILENAME,help="the absolute path + filename of your todo list file")
def update_task(index: int, name: str, description: str, priority: str ,filename: str):
    """
    Updates an existing task
    Args:
        index (int): the index to update
        name (str):the task name
        description (str):task description
        priority (str): the priority of the task
        file_name (str, optional): todo_list file name if specified [Default = todo_list.txt]
    """

    filename = file_path(filename)
    tasks = logic.read_file(filename)

    if not validate_tasks(tasks,filename) or not valid_task_index(index,tasks):
        return

    # index correction so that we can retrieve correct data
    index -=1
    if name == "" and description == "" and priority =="":
        new_task_data, message = update_menu()
        if new_task_data == ["","",""]:
            tab = tabulate.tabulate([[f"{message} \nAborting operation..."]],tablefmt="fancy_grid")
            print(tab)
            return
    else:
        # new_task_data, updating_data = [priority.upper(),name,description,]
        new_task_data = [priority.upper(),name,description,]

    # the priority selected by the user
    if new_task_data[0] != "":
        if new_task_data[0] in logic.PRIORITIES.keys():
            new_task_data[0] = logic.PRIORITIES.get(new_task_data[0])
        elif new_task_data[0] in logic.PRIORITIES.values():
            pass
        else:
            m1 = f"You have chosen an invalid priority {new_task_data[2]}"
            m2 = f" \nThese are the available priorities {PR_PROMPT}"
            tab = tabulate.tabulate([[m1 + m2]],tablefmt="fancy_grid")
            print(tab)
            return

    selected_index, selected_message = display_index(tasks,index)

    message = update_message(new_task_data)
    result = logic.update_task([index,tasks],new_task_data,filename)

    result_message = "Successfully" if result else "Failed to"
    message = f"{result_message} updated the {message} of task {selected_index}."

    print_result(selected_message,message)
    return


@main.command(help = "delete an existing task")
@click.option("-i","--index",type=int,prompt = "Enter the task number",help="the index of the task you want to update")
@click.option("-f","--filename",default =logic.DEFAULT_FILENAME,help="the name of the todo list file")
def delete_task(index,filename):
    """
    Deletes an existing task form our todo_list file

    Args:
        index (int): the task ID number you want to delete
        filename (str): the file in which the task exists in
    """
    filename = file_path(filename)
    tasks = logic.read_file(filename)

    if not validate_tasks(tasks,filename) or not valid_task_index(index,tasks):
        return

    index -=1
    selected_index, selected_message = display_index(tasks,index)

    operation = logic.delete_task([index,tasks],filename)

    result_message = "Successfully deleted" if operation else "Failed to delete"
    message = f"{result_message} task {index+1} in {basename(filename)}"

    print_result(selected_message,message)
    return


@main.command(help="displays tasks from a selected todo_list")
@click.option("-s","--show",help="filter to display certain tasks based off of their priority",default = "ALL")
@click.option("-f","--filename",help="the filename of the todo_list file if not specified",default=logic.DEFAULT_FILENAME)
def view_tasks(show,filename):
    """
    Lists all the available tasks in a todo_lits file

    Args:
        filter (str,optional): used to control which tasks gets shown. [Default = ALL]
        path (str,optional): the name of the todo list file. [Default = todo_list.txt]
    """
    filename = file_path(filename)
    tasks = logic.read_file(filename)

    if not validate_tasks(tasks, filename):
        return

    try:
        terminal_size = get_terminal_size() + 10
    except Exception as e:
        terminal_size = 50

    requested_data = logic.view_task(tasks,show.upper())
    headers = ["ID","PRIORITY","NAME","DESCRIPTION","STATUS"]
    tab = tabulate.tabulate(requested_data,headers=headers,tablefmt="fancy_grid",maxcolwidths=terminal_size)
    print(tab)

    return


@main.command(help = "change the status of a task")
@click.option("-i","--index",type=int,required=1,prompt = "Enter the task number",help="the index of the task you want to update")
@click.option("-s","--status",prompt = f"Select a new status {STATUS_PROMPT}",help="change progress of task [NOT STARTED, IN PROGRESS, COMPLETED]")
@click.option("-f","--filename",required =1,prompt = f"Enter filename",default =logic.DEFAULT_FILENAME,help="the name of the todo list file")
def change_status(index,status,filename):
    """
    Changes the status of a task. Status include "COMPLETED", "IN PROGRESS" and "NOT STARTED"

    Args:
        index (int): the task ID number you want to delete
        status (str): the new status of the task
        filename (str): the file in which the task exists in
    """
    filename = file_path(filename)
    tasks = logic.read_file(filename)
    status = logic.get_dict_value(logic.STATUS,status.upper().strip())

    if not validate_tasks(tasks,filename) or not valid_task_index(index,tasks):
        return

    if status == None:
        tab = tabulate.tabulate([["Aborting operation. \nIncorrect status."]],tablefmt="fancy_grid")
        print(tab)
        return


    index -=1
    selected_index, selected_message = display_index(tasks,index)

    operation = logic.change_status([index,tasks],status.upper(),filename)

    # if the state is in progress than user has started the task
    state = status.lower()
    if state == "in progress":
        state = "started"

    state_message = f"You have {state}" if state != "not started" else 'State set to "not started" for'

    result_message = "Failed to update status of task" if not operation else f'{state_message} task'
    message = f"{result_message} {index+1} in {basename(filename)}"

    print_result(selected_message,message)
    return



@main.command(help = "create a new todo_list file")
@click.option("-f","--filename",required=1, prompt = "Enter the name of the file")
def create_file(filename):
    """
    Creates a new todo_list file. All new files gets saved in the Downloads/TaskIT

    Args:
        filename (str): file name
    """
    file = file_path(filename)

    if exists(file) and isfile(file):
        tab = tabulate.tabulate([[f"{basename(file)} already exists."]],tablefmt="fancy_grid")
        print("\n",end=tab)
        choice = input(f"\nOverwrite file (y/n): ").lower()
        if choice in ["yes","y"]:
            with open(file,"w") as f:
                f.close()
            tab = tabulate.tabulate([[f"{basename(file)} has been created"]],tablefmt="fancy_grid")
        else:
            tab = tabulate.tabulate([[f"Could not create {basename(file)}."]],tablefmt="fancy_grid")
    elif not exists(filename):
        with open(file,"w") as f:
            f.close()
        tab = tabulate.tabulate([[f"{basename(file)} has been created"]],tablefmt="fancy_grid")
    else:
        tab = tabulate.tabulate([[f"Error could not create {basename(file)}"]],tablefmt="fancy_grid")

    print(tab)
    return

@main.command(help="delete an existing task file")
@click.option("-f","--filename",required=1, prompt = "Enter the name of the file")
def delete_file(filename):
    """
    Deletes the to_do_list file if it exists
    """

    files = listdir(MAIN_PATH)
    filename = file_path(filename)
    choice = ""


    if basename(filename) in files:
        choice = input("Confirm (yes/no): ").lower().strip()
    else:
        tab = tabulate.tabulate([[f"{basename(filename)} does not exist."]],tablefmt="fancy_grid")
        print(tab)
        return

    if choice in ["yes","y"] and exists(filename) and isfile(filename):
        remove(file_path(filename))
        tab = tabulate.tabulate([[f"{basename(filename)} has been deleted"]],tablefmt="fancy_grid")

    else:
        if not isfile(filename):
            print(f"{filename} .")
            tab = tabulate.tabulate([[f"{basename(filename)} is a dir. \n Aborting operation"]],tablefmt="fancy_grid")
            print(tab)
            return
        tab = tabulate.tabulate([["Aborting operation"]],tablefmt="fancy_grid")

    print(tab)

    return

@main.command(help="list all available todo lists")
def list_all():
    """
    Lists all the available todo list files in your Downloads/TaskIT folder
    """

    files = listdir(MAIN_PATH)
    clean_data = [file for file in files if ".txt" in file]

    if len(clean_data) < 1:
        tab = tabulate.tabulate([["You currently do not have any todo_lists"]],tablefmt="fancy_grid")
        print(tab)
        return

    # creating a numbering system
    todo_list_files = [[clean_data.index(file)+1 ,file] for file in clean_data]

    # tabulating data
    tab = tabulate.tabulate(todo_list_files,headers=["","Available Files"],tablefmt="fancy_grid")
    print(tab)

# helpers
def update_menu():
    """
    task update controller. Only triggers if user does not specify what they want to
    change via flags

    Returns:
        tuple : [str,str,str],message
    """


    header = ["","options"]
    tab = tabulate.tabulate([[1,"Change Priority"],[2, "Change task name"],
        [3, "Change description"],[4,"Change all"],
        [0,"Cancel"]],tablefmt="outline",headers=header)

    breaker = 0

    while True:
        print(clear_term)
        print(tab)
        choice = input('Select only one of the above options: ').lower().strip()

        if breaker > 2 or choice == "0":
            message = "Canceled"
            if choice != "0":
                message = "To many attempts"
            return ["","",""], message

        print()
        if choice == "1":
            priority = input(f"Enter new priority {PR_PROMPT}: ")
            return [priority.upper(),"",""], ""
        elif choice == "2":
            name = input(f"Enter the new task name: ")
            return ["",name,""], ""
        elif choice == "3":
            desc= input("Enter the new task description: ")
            return ["","",desc], ""
        elif choice == "4":
            priority = input(f"Enter new priority {PR_PROMPT}: ")
            name = input(f"Enter the new task name: ")
            desc= input("Enter the new task description: ")
            return [priority.upper(),name,desc], ""

        breaker +=1

def update_message(updated_data:list ):
    """
    creates a custom message based of what got updated in the task
    """

    priority , name, description = updated_data

    if priority != "" and name == "" and description =="":
        message = "priority"
    elif name != "" and priority == "" and description =="":
        message = "name"
    elif description != "" and name == "" and priority =="":
        message = "description"
    else:
        message = "name, description and priority"

    return message

def validate_tasks(tasks: list, filename:str ):
    """
    validates the given list of tasks.

    Args:
        tasks (list): the list containing our task
        filename (str): the name of teh file where we extracted the list from

    Returns:
        bool : default True
    """
    if tasks == "":
        tab = tabulate.tabulate([[f"Todo list does not exist: {basename(filename)}"]],tablefmt="fancy_grid")
        print(tab)
        return False

    if len(tasks) < 1:
        tab = tabulate.tabulate([["You have no available tasks."]],tablefmt="fancy_grid")
        print(tab)
        return False

    return True

def valid_task_index(index: int, tasks: list):
    """
    validates the given index

    Args:
        index (int):the index we want to validate
        tasks (list): a list containing our tasks

    Returns:
        bool : default True
    """
    if index == 0 or index > len(tasks):
        tab = tabulate.tabulate([['The selected task number does not exists.']],tablefmt="fancy_grid")
        print(tab)
        return False

    return True

def display_index(tasks: list, index: int):
    """
    returns a string formatted version of the index and a message. The message
    can be used for showcasing the index to the user

    Args:
        tasks (list): the list of tasks
        index (_type_): the selected index

    Returns:
        tuple : selected_index, message
    """
    # selecting task number and task name
    selected_index = tasks[index].split(" ")[0].strip('\" \"')
    selection_message = f'Selected task {selected_index}: {tasks[index][3].strip(" ")}'
    return selected_index, selection_message

def print_result(selected_message: str ,message: str):
    """
    prints our the given message in a tabulated format

    Args:
        selected_message (str): selected message contains teh result of the operation
        we performed. Example, update will have a selected_message of Successfully or Failed to
        message (str): the result string
    """
    tab = tabulate.tabulate([[f"{selected_message} \n{message}"]],tablefmt="fancy_grid")
    print(tab)

if __name__ == "__main__":

    if not exists(MAIN_PATH):
        mkdir(MAIN_PATH)
    main()





