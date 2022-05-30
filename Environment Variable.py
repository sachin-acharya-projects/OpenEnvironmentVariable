import subprocess, ctypes

try:
    subprocess.check_output("rundll32 sysdm.cpl,EditEnvironmentVariables", stderr=subprocess.STDOUT)
except subprocess.CalledProcessError as e:
    with open('environment_opener.txt', 'w') as file:
        file.write(str(e))
    ctypes.windll.user32.MessageBoxW(0, "Some error has been occured during execution process. Please check 'environment_opener.txt' for full details", "Execution Error", 0)
# os.system("rundll32 sysdm.cpl,EditEnvironmentVariables")