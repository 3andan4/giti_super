import os
import sys
from giti_powercharged import powercharged
import json

# create a dictionary of commands with the commands/commands.json file
commands_list = []
description = {}
command_input = {}
message = {}

os.popen('clear')
git_status = os.popen('git status -s').readlines()

def is_a_command(command):
    global commands_list
    if command in commands_list:
        return True
    else:
        return False

def git_file():
    global git_status
    choice_loop = True
    while choice_loop:
        print("0. Exit")
        for line in git_status:
            print(f"{git_status.index(line) + 1}: {line[3:]}")
        choice = input("Which file do you want to commit? ")
        try:
            choice = int(choice) - 1
        except:
            print("Invalid input.")
            continue
        # check if the choice is valid
        if choice < -1 or choice >= len(git_status):
            print("Invalid choice")
        elif choice == -1:
            return False
        else:
            return git_status[choice][3:]


def load_commands():
    global commands_list, description, command_input, message
    file_data = json.load(open('commands/commands.json'))
    for entry in file_data:
        command_name = entry['command']
        if isinstance(command_name, list):
            for command in command_name:
                commands_list.append(command)
                description[command] = entry['description']
                command_input[command] = entry['input']
                message[command] = entry['message']
        else:
            commands_list.append(command_name)
            description[command_name] = entry['description']
            command_input[command_name] = entry['input']
            message[command_name] = entry['message']


def file_picker():
    file = git_file()
    if file == False:
        return 0
    else:
        return file

# read the commands.json file and load the commands into the program
def command_interpreter(command, file):
    global command_input, message
    inputs = command_input[command]
    msg = message[command]
    answer = []
    for qs in inputs:
        answer.append(input(f"{qs}: "))
    for x, item in enumerate(answer):
        msg = msg.replace(f"${x + 1}", item)
    msg = f"{file}:\n\t\t{msg}"
    return msg


def file_by_file(command):
    file = file_picker()
    if file == 0:
        print("Exiting...")
        return 0
    msg = command_interpreter(command, file)
    os.popen(f"git add *{file}")
    return msg

def main(params):
    global commands_list, description, command_input, message

    if len(params) == 1 or params[1] == "powercharged":
        powercharged()
    elif is_a_command(params[1]):
        command = params[1]
        msg = file_by_file(command)
        if msg == 0:
            exit()
        commit_title = input("Commit title: ")
        final_msg = f":sparkles: {commit_title}\n" + msg
        os.popen(f'git commit -m "{final_msg}"')
        print("Commit successful!")
    elif params[1] == 'help':
        print('''
        giti is a git commit interface that allows you to make commits without having to type them out.
        To use giti, type 'giti' followed by the command you want to run.
        The commands are:
        - powercharged (or none): a commit interface that allows you to make commits with extensive help.
        - help: displays this message.
        ''')
        x = 0
        for command in commands_list:
            print(f'''- {command}: {description[command]}''')
            x += 1
            if x == 6:
                x = 0
                input("----------")
    else:
        print("Command not found. Type 'giti help' for help.")


if __name__ == '__main__':
    load_commands()
    main(sys.argv)
