import platform
import subprocess
import os


def run_shell_command(command):
    result = subprocess.run(command, capture_output=False, text=True, shell=True, encoding='cp949')
    ## print(result.stdout)
    return result.stdout

def install_exe_package(CurrOS):
    if CurrOS == 'Windows':
        release_command = 'pyinstaller --clean --onefile --add-data "Gsi_writer.ui:." main.py'
    else : 
        release_command = 'pyinstaller --clean --noconsole --onefile --add-data "Gsi_writer.ui:." main.py'
    run_shell_command(release_command)

def remove_dist_folder(folder, CurrOS):
    build_folder = os.path.join(folder, 'build') 
    exist = os.path.exists(build_folder)
    if exist == True:
        if CurrOS == "Windows":
            run_shell_command('rmdir /S /Q build')
        else:
            run_shell_command('rm -rf build')
    dist_folder = os.path.join(folder, 'dist')      
    exist = os.path.exists(dist_folder)
    if exist == True:
        if CurrOS == "Windows":
            run_shell_command('rmdir /S /Q dist')
        else:
            run_shell_command('rm -rf /S /Q dist')
            
def copy_ui_to_dist(CurrOS):
    if CurrOS == 'Windows':
        run_shell_command('copy /Y Gsi_writer.ui dist')
    else:
        run_shell_command('cp Gsi_writer.ui .main')

CurrOS = platform.system()
current_directory = os.getcwd()
remove_dist_folder(current_directory, CurrOS)
print(f'=====> current directory :  {current_directory}')
install_exe_package(CurrOS)
copy_ui_to_dist(CurrOS)