"""
Handles the main logic for operating with / writing on to our todo list
"""
import re

PRIORITIES = {
    "O" : "OPTIONAL",
    "L" : "LOW",
    "M" : "MEDIUM",
    "H" : "HIGH",
    "U" : "URGENT"
}

STATUS = {
    "N" : "NOT STARTED", # \u2610
    "I" : "IN PROGRESS", # \u25CB
    "C" : "COMPLETED" # u'\u2713'
}

DEFAULT_FILENAME = "todo_list.txt"
DEFAULT_TRIGGER = "ALL"
DEFAULT_STATE = "NOT STARTED"


def add_task(task_name: str, description: str, priority:str, file_name = DEFAULT_FILENAME,status = DEFAULT_STATE):
    """
    Adds a new task to the todo list

    Args:
        dir (str): save path of the todo list [DEFAULT = todo_list.txt]
        task_name (str): the name of task
        description (str): a small description regarding the task
        priority (str): PRIORITY of the task

    Returns:
        bool :
    """

    tasks = []

    try:
        # first we try to read the data on the file
        with open(file_name,"r") as file:
            tasks = file.readlines() # creating a list of all the available files
    except (FileNotFoundError):
        pass

    priority = get_dict_value(PRIORITIES,priority.upper())
    task = f'"{len(tasks)+1}" "{priority}" "{task_name}" "{description}" "{status}"'

    # appending new task to list of current tasks
    if len(tasks) >= 1 and not "\n" in tasks[len(tasks)-1][-1]: # [-1] indicates last element
        tasks.append(f'\n{task}')
    else:
        tasks.append(task)


    # overwriting the file with new data
    try :
        with open(file_name,"w") as file:
            file.writelines(tasks)
            file.close()
        return True
    except Exception as e:
        return False

def view_task( tasks: list,trigger = DEFAULT_TRIGGER):
    """
    Displays all the tasks on your todo list.

    Args:
        tasks (list) : a list containing all the available tasks
        trigger (str, optional) : Trigger flag , triggers an output for only the requested task of Priority n.
    Returns:
        (list): contains the correct data based off teh mode of the filter
    """

    for key, value in PRIORITIES.items():

        if trigger == DEFAULT_TRIGGER:
            break

        # if the trigger word is the same as any of values we break
        if trigger == value:
            break

        # in the event of an abbreviated trigger we use the key to get full trigger
        if trigger == key:
            trigger = value
            break

    data = []
    for task in tasks:
        data.append(task.strip())

    requested_data = []
    for task in data:
        if trigger == "ALL":
            requested_data.append(regex_split(task))
        else:
            if trigger in task:
                requested_data.append(regex_split(task))

    return requested_data


def delete_task(task_data: list, file_name = DEFAULT_FILENAME):
    """
    Deletes an existing task form our todo_list file

    Args:
        task_data (list): the data and index to update
        filename (str): the file in which the task exists in
    Returns:
        str : operation message_
    """

    index, tasks = task_data
    # confirm deleting
    choice = input(f"Confirm delete of task (y/yes): ").lower()

    if choice == 'y' or choice == 'yes':
        # deleting task
        del tasks[index]

        # overwriting the file with new data
        with open(file_name,"w") as file:
            file.writelines(tasks)
            file.close()

        return True
    else:
        return False


def update_task(task_data : list ,new_task_data:list, file_name = DEFAULT_FILENAME):
    """
    Updates an existing task within our todo_list file

    Args:
        task_data (list): the data and index to update
        new_task_data (list): the data to inject
        file_name (str, optional): todo_list file name if specified [Default = todo_list.txt]

    Returns:
        str: result message
    """
    write = False
    index, tasks = task_data

    # retrieving task from task
    task = regex_split(tasks[index])
    old_task_data = task_properties(task)


    new_task = modify_task(old_task_data,new_task_data)

    tasks[index] = new_task if index == len(tasks)-1 else f"{new_task}\n"

    # overwriting the file with new data
    try:
        with open(file_name,"w") as file:
            file.writelines(tasks)
            file.close()
        write = True
    except Exception as e:
        pass

    return write



def task_properties(task_data: list):
    """
    generates a list entity of the task

    Args:
        task_data (list): the task we need to break apart
    Return:
        list :
    """

    # task_data = [data for data in task]


    task_id = task_data[0].strip()
    task_priority = task_data[1].strip()
    task_name  = task_data[2].strip()
    task_description  = task_data[3].strip()
    task_state = task_data[4].strip()

    return [task_id,task_priority, task_name, task_description, task_state]



def modify_task(original_task_data: list, new_task_data: tuple):

    priority , task_name, description = new_task_data

    # priority only
    if task_name == "" and description == "" and priority != "":
        original_task_data[1] = priority

    # name only
    elif task_name != "" and description == "" and priority == "":
        original_task_data[2] = task_name

    # description
    elif task_name == "" and description != "" and priority == "":
        original_task_data[3] = description

    # name and description
    elif task_name != "" and description != "" and priority == "":
        original_task_data[2] = task_name
        original_task_data[3] = description

    # name and priority
    elif task_name != "" and description == "" and priority != "":
        original_task_data[1] = priority
        original_task_data[2] = task_name

    # priority and description
    elif task_name == "" and description != "" and priority != "":
        original_task_data[1] = priority
        original_task_data[3] = description

    # everything
    else:
        original_task_data[1] = priority
        original_task_data[2] = task_name
        original_task_data[3] = description

    return f'"{original_task_data[0]}" "{original_task_data[1]}" "{original_task_data[2]}" "{original_task_data[3]}" "{original_task_data[4]}"'


def change_status(task_data: list, status,file_name=DEFAULT_FILENAME):
    """
    Change the status of a task

    Args:
        index (int): the index of the task we want to modify
        file_name (str, optional): The name of the file we want to modify. Defaults to DEFAULT_FILENAME.

    Returns:
        boolean :
    """

    index, tasks = task_data

    task = regex_split(tasks[index])
    data = task_properties(task)
    new_task_data = f'"{data[0]}" "{data[1]}" "{data[2]}" "{data[3]}" "{status}"'
    tasks[index] = new_task_data if index == len(tasks)-1 else f"{new_task_data}\n"

    try:
        with open(file_name,"w") as file:
            file.writelines(tasks)
            file.close()
        return True
    except Exception as e:
        return False




def get_dict_value(dic: dict, given_key:str):
    """
    returns the value of a given key if the key exists in a given dictionary
    Args:
        dic (dict): dictionary to retrieve data from
        given_key (str): the key for teh value

    Returns:
        str : value
    """
    for key, value in dic.items():
        if key == given_key:
            return value

        if value == given_key:
            return value

def read_file(filename: str= DEFAULT_FILENAME):
    """
    reads data from a given file and returns a list of its contents

    Args:
        filename (str, optional): the name of the file. Defaults to todo_list.txt.

    Returns:
        list : a list of the lines in the file
    """
    tasks_read = []
    try:
        with open(filename) as file:
            tasks_read = file.readlines()
    except (FileNotFoundError):
        return ""

    return tasks_read

def regex_split(text: str):
    """
    splits the given string into a list based off the enclosed quotes

    Args:
        text (str): the string to split
    """
    pattern = re.compile('"([^"]*)"')
    data = re.split(pattern,text)

    data = [da for da in data if not da in [" ",""]]

    return data

