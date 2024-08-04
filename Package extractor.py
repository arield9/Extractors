
import re
import subprocess


class PackageDumper:

    def __init__(self):
         self=self

    def PackageCommand(self):
        try:
            packages_list = subprocess.Popen(["C:\\Users\\Ariel davidpur\\Desktop\\platform-tools\\adb.exe", "shell", "pm", "list", "packages"], stdout=subprocess.PIPE, text=True)
            final_list = packages_list.communicate()
            
            for line in final_list:
                if line:
                    no_default_package = re.findall(r"(?m)^(?!.*\b(?:samsung|android|sec\.)\b).*", line)
                    package_lines = '\n'.join(no_default_package)
                    print(package_lines)
                else:
                    continue

        except subprocess.SubprocessError as e:
            print(f"Error while executing the command: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            
            

def main():
    PackageDumper().PackageCommand()

if __name__ == "__main__":
    main()