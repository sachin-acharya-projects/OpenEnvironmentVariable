import sys
from colorama import Fore, init as colorama_init
from py_setenv import setenv
import ctypes, subprocess, argparse

colorama_init(autoreset=True)

class Cooperate:
    def __init__(self, arguments: argparse.Namespace):
        self.isUser = True
        # print((dict(vars(arguments))))
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
                print("")
                print("{}UAC Elevation is not found. Defaulting scope to USER".format(Fore.LIGHTCYAN_EX))
            else:
                print("""{}Cannot Execute the Process
                    [Reason]
                        Permission Denied (UAC Elevation is Required)
                    [Why]
                        Why UAC Elevation is Required?
                            To perform CRUD (CREATE, READ, WRITE, DELETE) operation on administrator scope, we need UAC.
                            To perform same operations on user scope, UAC is not necessary    
                    [Restart] The Process with Administrator Permission (Run As Administrator)
            """.format(Fore.RED))
        if arguments.get_variable:
            print("{}: {}".format(arguments.get_variable, setenv(arguments.get_variable, suppress_echo=True, user=self.isUser)))
        if arguments.path_add:
            path_list = setenv('path', user=self.isUser, suppress_echo=True).split(";")
            if not arguments.path_add in path_list:
                setenv("path", value=arguments.path_add, append=True, user=self.isUser, suppress_echo=True)
        if arguments.path_show:
            path_list = setenv('path', user=self.isUser, suppress_echo=True).split(";")
            print("")
            print("""{}[LIST OF PATHS]""".format(Fore.LIGHTBLACK_EX))
            print("{}_".format(Fore.LIGHTBLACK_EX) * 60)
            print("")
            for varlst in path_list:
                print("{}".format(Fore.CYAN)+varlst)
                print("")
        if arguments.set_variable:
            if not arguments.value:
                variable_value = input("Enter Value: ")
            else:
                variable_value = arguments.value
            variable_name = arguments.set_variable
            setenv(variable_name, value=variable_value, user=self.isUser, suppress_echo=True)
            print("{}VARIABLE {} HAS BEEN ASSIGNED TO {}".format(Fore.BLUE, variable_name, variable_value))
        if arguments.delete:
            variable_name = arguments.delete
            setenv(variable_name, user=self.isUser, suppress_echo=True, delete=True)
        if arguments.show_variables:
            variables = dict(setenv(list_all=True, suppress_echo=True, user=self.isUser))
            var_list = list(variables.keys())
            print("")
            print("""{}Available Varibles are displayed below""".format(Fore.LIGHTBLACK_EX))
            print("{}_".format(Fore.LIGHTBLACK_EX) * 60)
            print("")
            for varlst in sorted(var_list):
                print("{}".format(Fore.CYAN)+varlst)
                print("")
    def isAdmin():
        try:
            __isAdmin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except:
            __isAdmin = False
        return __isAdmin
def main():
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
    Cooperate(parser.parse_args())
if __name__ == '__main__':
    main()