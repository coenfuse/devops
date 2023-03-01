#### 1. Python venv on Linux
- Create a venv by typing 
```python3 -m venv venv```
- Then activate it by source by typing
```./venv/bin/activate```

Do not ask me why source is required, it is just required and it work.
More info at https://stackoverflow.com/questions/14604699/how-to-activate-virtualenv-in-linux

- **NOTE** : You may require installing the python's venv package manually by typing command ```sudo apt-get install python3.8-venv``` on Debian systems

### 2. pip install paho-mqtt fail
If you get the following error while trying to install paho-mqtt package,
```
ERROR: Command errored out with exit status 1:
   command: /home/sarthak/Documents/dev/lamina/venv/bin/python3 -u -c 'import sys, setuptools, tokenize; sys.argv[0] = '"'"'/tmp/pip-install-gfifsq6d/paho-mqtt/setup.py'"'"'; __file__='"'"'/tmp/pip-install-gfifsq6d/paho-mqtt/setup.py'"'"';f=getattr(tokenize, '"'"'open'"'"', open)(__file__);code=f.read().replace('"'"'\r\n'"'"', '"'"'\n'"'"');f.close();exec(compile(code, __file__, '"'"'exec'"'"'))' bdist_wheel -d /tmp/pip-wheel-g6ifz8ye
       cwd: /tmp/pip-install-gfifsq6d/paho-mqtt/
  Complete output (6 lines):
  usage: setup.py [global_opts] cmd1 [cmd1_opts] [cmd2 [cmd2_opts] ...]
     or: setup.py --help [cmd1 cmd2 ...]
     or: setup.py --help-commands
     or: setup.py cmd --help
  
  error: invalid command 'bdist_wheel'
  ----------------------------------------
  ERROR: Failed building wheel for paho-mqtt
```
- Install the wheel package first as,
```pip install wheel```
- Then uninstall previously failed paho-mqtt installation as ```pip uninstall paho-mqtt```
- The install paho-mqtt again as ```pip install paho-mqtt```