import os
import shutil


# remove these directories if they exists for a clean bundle.
to_remove = ("build", "dist")

for remove in to_remove:
    if os.path.exists(remove):
        print(f"Deleting existing '{remove}' directory for clean bundling.")
        shutil.rmtree(remove)


osx_command = ("pyinstaller --onefile --windowed --clean --name=auxiclean_osx"
               " run.py; cd dist; zip -r auxiclean_osx.zip auxiclean_osx.app;"
               " cd ..")
linux_command = ("pyinstaller --onefile --windowed --clean --name=auxiclean"
                 "_linux run.py")
windows_command = ("pyinstaller --onefile --windowed --name=auxiclean_windows"
                   " run.py")

# we probably should not use os.system calls.
# TODO: change os.system to subprocess.Popen...

platform = os.sys.platform
if platform == "linux":
    print("Bundling for linux.")
    os.system(linux_command)
elif platform == "darwin":
    print("Bundling for OSX.")
    os.system(osx_command)
elif platform == "win32":
    print("Bundling for Windows.")
    os.system(windows_command)
else:
    raise OSError(f"OS '{platform}' not recognized... cannot bundle app.")
