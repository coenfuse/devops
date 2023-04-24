On Windows with PS type ```./tools/build.ps1 <command>```
On Linux with Bash type ```bash tools/build.sh <command>```


Building script is to be done from Windows only due to limitation of pyinstaller
To build binaries for Windows, one must have Python 3.11 or above installed.
TO build binaries for Linux, one must have Docker installed on the machine.

To start binaries builder open powershell at the root of repo and type
```./tools/build.ps1```


To be frank. Building Lamina as a cross-platform has been a mess actually.
Apart from signalling and thread issues, the builder - PyInstaller didn't help us
much either. Being a good tool, it was very odd for it to not support cross-platform.

To finally get around this requirement, I had to do several patches and doing
possibly stupid stuff that is hanging by a thread currently.

Problem 1 : PyInstaller can't build on Windows and Linux simulataneously. That
means, to build your python application for Linux using PyInstaller, you must
use Linux. And this is the same for Windows. So naively, one has to switch
back-and-fro between VMs to develop on both platforms.

Problem 2 : You can't run Windows container for Docker on Windows (apparantly)

Solution?
Keep windows as base building platform.
To build for windows, use virtual environment to not pollute system with 
dependencies and build executable using Pyinstaller.
To build for Linux, create a docker container build binaries inside of it and then
copy them out back to the host building platform (here windows)

Wrap this all up with extensive powershell and bash scripts on Windows and pray.