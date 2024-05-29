import platform
import subprocess
import os


def run_shell_command(command):
    result = subprocess.run(command, capture_output=False, text=True, shell=True, encoding='cp949')
    ## print(result.stdout)
    return result.stdout

def install_exe_package():
    CurrOS = platform.system()
    if CurrOS == 'Windows':
        release_command = 'pyinstaller.exe --clean --noconsole -F main.py'
    else : 
        release_command = 'pyinstaller -w -F main.py'
    run_shell_command(release_command)

def remove_dist_folder(folder):
    build_folder = os.path.join(folder, 'build') 
    exist = os.path.exists(build_folder)
    if exist == True:
        run_shell_command('rmdir /S /Q build')

    dist_folder = os.path.join(folder, 'dist')      
    exist = os.path.exists(dist_folder)
    if exist == True:
       run_shell_command('rmdir /S /Q dist')

def copy_ui_to_dist():
    run_shell_command('copy /Y Gsi_writer.ui dist')

current_directory = os.getcwd()
remove_dist_folder(current_directory)
print(f'=====> current directory :  {current_directory}')
install_exe_package()
copy_ui_to_dist()