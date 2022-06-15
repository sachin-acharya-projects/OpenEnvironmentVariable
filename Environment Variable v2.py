from colorama import Fore, init as colorama_init
from tkinter import messagebox
from py_setenv import setenv
import ctypes, subprocess, argparse, sys, os

colorama_init(autoreset=True)

help_text = """
usage: Environment Variable v2.py [-h] [-gui] [-s] [-D VARIABLE_NAME] [-set VARIABLE_NAME] [-val VARIABLE_VALUE] [-P] [-p PATH] [-g VARIABLE_NAME]
                                  [-S] [--silent]

This commandline tools helps you to perform CRUD operation on System Environment

options:
  -h, --help            show this help message and exit
  -gui                  Opens Up GUI for Environment Variable where you can use CRUD operation Graphically, If no options, provided then this will
                        be default option
  -s, --show-variables  Shows all the system-variable within the given scope
  -D VARIABLE_NAME, --delete VARIABLE_NAME
                        Delete given variable from system environment if available
  -set VARIABLE_NAME, --set-variable VARIABLE_NAME
                        Add new variable to system-environment, overide if availble. Use with --value
  -val VARIABLE_VALUE, --value VARIABLE_VALUE
                        Value for given environment variable
  -P, --path-show       Display the value of PATH variable
  -p PATH, --path-add PATH
                        Append to PATH variable, omiting dublications
  -g VARIABLE_NAME, --get-variable VARIABLE_NAME
                        Display value of GIVEN variable if available
  -S, --system          Assign Scope of the variables to SYSTEM (Default Scope: USER)
  --silent              This option with silently run the command (without print statement) -- donot use for query
"""

class Namespace:
    def __init__(self, **kargs):
        self.__dict__.update(kargs)

class ArgumentParser_:
    def __init__(self, args: list, argument_req: list):
        self.result_dict = {
            
        }
        
        for argument, *argument_2, action in argument_req:
            argument_name = str(argument).removeprefix('-').removeprefix('-').replace('-', '_')
            if argument_2:
                argument_name = str(argument_2[0]).removeprefix('-').removeprefix('-').replace('-', '_')
            if action:
                self.result_dict[argument_name] = True if argument in args else True if not len(argument_2) <= 0 and argument_2[0] in args else False
            else:
                try:
                    self.result_dict[argument_name] = args[args.index(argument) + 1] if argument in args else args[args.index(argument_2[0]) + 1] if argument_2[0] in args else None
                except:
                    print(f"{Fore.RED}Positional argument {argument} cannot accept empty value. Please use --help to find out more")
                    sys.exit()
    @property
    def parse_args_all(self):
        return Namespace(**self.result_dict)

# Useless
def argparser_():
        parser = argparse.ArgumentParser(description="This commandline tools helps you to perform CRUD operation on System Environment")
        # Done
        parser.add_argument('-gui', help="Opens Up GUI for Environment Variable where you can use CRUD operation Graphically, If no options, provided then this will be default option", action='store_true')
        # Done
        parser.add_argument("-s", "--show-variables", help='Shows all the system-variable within the given scope', action='store_true')
        # Done
        parser.add_argument("-D", "--delete", help='Delete given variable from system environment if available', metavar='VARIABLE_NAME')
        # Done
        parser.add_argument('-set', '--set-variable', help="Add new variable to system-environment, overide if availble. Use with --value", metavar='VARIABLE_NAME')
        # Done
        parser.add_argument('-val', '--value', help="Value for given environment variable", metavar='VARIABLE_VALUE')
        # Done
        parser.add_argument('-P', '--path-show', help='Display the value of PATH variable', action='store_true')
        # Done
        parser.add_argument('-p', '--path-add', help='Append to PATH variable, omiting dublications', metavar='PATH')
        # Done
        parser.add_argument('-g', '--get-variable', help='Display value of GIVEN variable if available', metavar='VARIABLE_NAME')
        # Done
        parser.add_argument('-S', '--system', help="Assign Scope of the variables to SYSTEM (Default Scope: USER)", action='store_true')
        
        parser.add_argument('--silent', help="This option with silently run the command (without print statement) -- do not use for query", action='store_true')

class Cooperate:
    def __init__(self, arguments: Namespace):
        self.isUser = True
        self.isSilent = True if arguments.silent else False
        # print((dict(vars(arguments))))
        if arguments.help:
            self.printStatement(f"{Fore.CYAN}{help_text}")
            sys.exit()
        if arguments.gui or len(sys.argv) <= 1:
            try:
                subprocess.check_output("rundll32 sysdm.cpl,EditEnvironmentVariables", stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError as e:
                with open('environment_opener.txt', 'w') as file:
                    file.write(str(e))
                ctypes.windll.user32.MessageBoxW(0, "Some error has been occured during execution process. Please check 'environment_opener.txt' for full details", "Execution Error", 0)
        if arguments.system:
            if self.isAdmin:
                self.isUser = False
                self.printStatement("")
                self.printStatement("{}UAC Elevation is not found. Defaulting scope to USER".format(Fore.LIGHTCYAN_EX))
            else:
                self.printStatement("""{}Cannot Execute the Process
                    [Reason]
                        Permission Denied (UAC Elevation is Required)
                    [Why]
                        Why UAC Elevation is Required?
                            To perform CRUD (CREATE, READ, WRITE, DELETE) operation on administrator scope, we need UAC.
                            To perform same operations on user scope, UAC is not necessary    
                    [Restart] The Process with Administrator Permission (Run As Administrator)
            """.format(Fore.RED))
        if arguments.get_variable:
            self.printStatement("{}: {}".format(arguments.get_variable, setenv(arguments.get_variable, suppress_echo=True, user=self.isUser)))
        if arguments.path_add:
            path_list = setenv('path', user=self.isUser, suppress_echo=True).split(";")
            path_loc = arguments.path_add
            if not path_loc in path_list:
                if path_loc == '.':
                    path_loc = os.getcwd()
                if messagebox.askyesno("Confirmation", "Do you want to add '{}' to PATH variable?".format(path_loc)):
                    setenv("path", value=path_loc, append=True, user=self.isUser, suppress_echo=True)
                    self.printStatement("{}`{}` has been added to PATH variable".format(Fore.LIGHTCYAN_EX, path_loc))
        if arguments.path_show:
            path_list = setenv('path', user=self.isUser, suppress_echo=True).split(";")
            self.printStatement("")
            self.printStatement("""{}[LIST OF PATHS]""".format(Fore.LIGHTBLACK_EX))
            self.printStatement("{}_".format(Fore.LIGHTBLACK_EX) * 60)
            self.printStatement("")
            for varlst in path_list:
                self.printStatement("{}".format(Fore.CYAN)+varlst)
                self.printStatement("")
        if arguments.set_variable:
            if not arguments.value:
                variable_value = input("Enter Value: ")
            else:
                variable_value = arguments.value
            variable_name = arguments.set_variable
            if messagebox.askyesno("Confirmation", "Do you want to set '{}' to '{}'?".format(variable_name, variable_value)):
                setenv(variable_name, value=variable_value, user=self.isUser, suppress_echo=True)
                self.printStatement("{}VARIABLE {}{} HAS BEEN ASSIGNED TO {}".format(Fore.LIGHTBLUE_EX, f"{Fore.LIGHTCYAN_EX}{variable_name}", Fore.LIGHTBLUE_EX, f"{Fore.LIGHTCYAN_EX}{variable_value}"))
        if arguments.delete:
            variable_name = arguments.delete
            if messagebox.askyesno("Confirmation", "Do you want to delete '{}'?".format(variable_name)):
                setenv(variable_name, user=self.isUser, suppress_echo=True, delete=True)
        if arguments.show_variables:
            variables = dict(setenv(list_all=True, suppress_echo=True, user=self.isUser))
            var_list = list(variables.keys())
            self.printStatement("")
            self.printStatement("""{}Available Varibles are displayed below""".format(Fore.LIGHTBLACK_EX))
            self.printStatement("{}_".format(Fore.LIGHTBLACK_EX) * 60)
            self.printStatement("")
            for varlst in sorted(var_list):
                self.printStatement("{}".format(Fore.CYAN)+varlst)
                self.printStatement("")
    def isAdmin():
        try:
            __isAdmin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except:
            __isAdmin = False
        return __isAdmin
    def printStatement(self, statement):
        if not self.isSilent:
            print(statement)
def main():
    parser = ArgumentParser_(sys.argv, [
        ('-h', '--help', True),
        ('-gui', True),
        ('-s', '--show-variables', True),
        ('-D', '--delete', False),
        ('-set', '--set-variable', False),
        ('-val', '--value', False),
        ('-P', '--path-show', True),
        ('-p', '--path-add', False),
        ('-g', '--get-variable', False),
        ('-S', '--system', True),
        ('--silent', True)
    ])
    Cooperate(parser.parse_args_all)
if __name__ == '__main__':
    main()