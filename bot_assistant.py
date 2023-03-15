import re

users = {}

def input_error(func):
    def inner(*args):
        try: 
            return func(*args)
        except KeyError:
            return f"No record with param {' '.join(args)}"
        except ValueError:
            return "The parameter must be in the specified format.\
                For more info, type 'help'"
        except IndexError:
            return "Type all params for command. For help, type 'help'"
    return inner


def cmd_hello_func(): 
    return "How can I help you?"


@input_error
def cmd_add_func(*args):
    name = args[0]
    phone = args[1]
    
    if not re.match(r"^\+[\d]{12}$", phone):
        raise ValueError
    
    if name in users:
        return f"User {name} is already in the phone book.\
            Give another name or change the number with 'change' command."
    elif phone in users.values():
        return f"The phone number {phone} is already registred in the phone book."
    else:
        users.update({name: phone})
        return f"{name} {phone} has been added to the phone book."


@input_error
def cmd_change_func(*args):
    name = args[0]
    phone = args[1]
    
    if name not in users:
        return f"User {name} is not in the phone book."
    elif phone in users.values():
        return f"The phone number {phone} is already registred in the phone book."
    else:
        users[name] = phone    
    return f"The phone number for {name} has been changed for {phone}."


@input_error
def cmd_phone_func(*args):
    name = args[0]
    phone = users[name]
    return f"The phone number for {name} is {phone}."


def cmd_show_all_func(*args):
    all = ""
    if len(users) == 0:
        return "No items in the phone book"
    else:
        for name, phone in users.items():
            all += name + ": " + phone + "\n"
        return all + "All users are displayed"


def cmd_help(*args):
    return """You can manage your phone book with the commands:
          hello
          add 'Name' '+380000000000'
          change 'Name' '+380000000000'
          phone 'Name'
          show all
          good bye
          close
          exit"""


def cmd_exit_func(*args): 
    return "Good bye!\n"


COMMANDS = {
    'hello': cmd_hello_func,
    'add': cmd_add_func,
    'change': cmd_change_func,
    'phone': cmd_phone_func,
    'show all': cmd_show_all_func,
    'good bye': cmd_exit_func,
    'close': cmd_exit_func,
    'exit': cmd_exit_func,
    'help': cmd_help,
}


def cmd_parser(command_line: str):
    for cmd in COMMANDS:
        if command_line.startswith(cmd):
            return COMMANDS[cmd], command_line.replace(cmd, '').strip().split()
    return None, []


def main():
    command_line = ""
    print("\nHello!")
    print(cmd_help())

    while True:
        command_line = input("\nEnter command: ")
        
        command, data = cmd_parser(command_line)
        
        if not command:
            print("No command. Try again!")
            continue
        
        print(command(*data))
        
        if command == cmd_exit_func:
            break
        
        
if __name__ == "__main__":
    main()