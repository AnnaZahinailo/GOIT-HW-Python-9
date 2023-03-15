import re

users = {}

def input_error(func):
    def inner(name, phone):
        if name == "" and phone == "":
            log = "Give me name and phone as '+380000000000' please."
        elif name.strip() == "":
            log = "Enter user name."
        elif not re.match(r"^\+[\d]{12}$", phone):
            log = "Give the phone number as '+380000000000'."
        else :
            try: 
                return func(name, phone)
            except KeyError:
                log = 'KeyError'
            except ValueError:
                log = 'ValueError'
            except IndexError:
                log = 'IndexError'
        return log
    return inner


def cmd_hello_func(): 
    return "How can I help you?"


@input_error
def cmd_add_func(name, phone):
    if name in users:
        return f"User {name} is already in the phone book. Give another name or change the number with 'change' command."
    elif phone in users.values():
        return f"The phone number {phone} is already registred in the phone book."
    else:
        users.update({name: phone})
        return f"{name} {phone} has been added to the phone book."

@input_error
def cmd_change_func(name, phone):
    if name not in users:
        return f"User {name} is not in the phone book."
    elif phone in users.values():
        return f"The phone number {phone} is already registred in the phone book."
    else:
        users[name] = phone    
    return f"The phone number for {name} has been changed for {phone}."


def cmd_phone_func(name):
    phone = users.get(name)
    if phone == None:
        return f"No user {name} in the phone book."
    else:
        return f"The phone number for {name} is {phone}."


def cmd_show_all_func():
    all = ""
    if len(users) == 0:
        return "No items in the phone book"
    else:
        for name, phone in users.items():
            all += name + ": " + phone + "\n"
        return all + "All users are displayed"


def cmd_exit_func(): 
    return "Good bye!\n"


def cmd_parser(command_line):
    command = ""
    name = ""
    phone = ""
    for cmd in COMMANDS:
        if command_line.lower().find(cmd) == 0:
            command = cmd
            i_name = len(cmd)
            if len(command_line) == i_name:
                continue
            elif cmd == 'phone' and command_line[i_name] == ' ':
                name = command_line[i_name + 1:]
            elif cmd in ('add', 'change') and command_line[i_name] == ' ' and command_line.find(' +') != -1 and command_line[command_line.find('+') + 1:].isdigit():
                i_phone = command_line.find('+')
                name = command_line[i_name + 1:i_phone - 1]
                phone = command_line[i_phone:]
            name = name.strip()
    return command, name, phone


COMMANDS = {
    'hello': cmd_hello_func,
    'add': cmd_add_func,
    'change': cmd_change_func,
    'phone': cmd_phone_func,
    'show all': cmd_show_all_func,
    'good bye': cmd_exit_func,
    'close': cmd_exit_func,
    'exit': cmd_exit_func
}


def get_handler(command, name, phone):
    if command == 'phone':
        return COMMANDS[command](name)
    elif command in ('add', 'change'):
        return COMMANDS[command](name, phone)
    else:
        return COMMANDS[command]()


def main():
    command_line = ""
    print("\nHello!")
    print("\nYou can manage your phone book with the commands:\nhello / add 'Name' '+380000000000' / change 'Name' '+380000000000' / phone 'Name' / show all / good bye / close / exit")

    while True:
        command_line = input("\nEnter command: ")
        if command_line.strip() == "":
            print("No command. Try again!")
        else:
            command, name, phone = cmd_parser(command_line)
            if command not in COMMANDS:
                print("Wrong command. Try again!")
            else:
                print(get_handler(command, name, phone))

            if command in ('good bye', 'close', 'exit'):
                break


if __name__ == "__main__":
    main()