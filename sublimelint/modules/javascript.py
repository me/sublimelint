# javascript.py - sublimelint package for checking javascript files

import subprocess, os
import sublime

def check(codeString, filename):
    info = None
    config_file = None
    if os.name == 'nt':
        info = subprocess.STARTUPINFO()
        info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        info.wShowWindow = subprocess.SW_HIDE
    
    args = ['jsl', '-stdin']

    config_file = os.path.join(sublime.packages_path(), 'User', 'jslint.conf')

    if os.path.exists(config_file):
        args += ["-conf", config_file]

    process = subprocess.Popen(
        args, 
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, 
        startupinfo=info
    )
    result = process.communicate(codeString)[0]
    return result


# start sublimelint Javascript plugin

import re
__all__ = ['run', 'language']
language = 'JavaScript'
description =\
'''* view.run_command("lint", "JavaScript")
        Turns background linter off and runs the jsl Javascript linter (http://www.javascriptlint.com/), 
        assumed to be on $PATH, on current view.
        If a file named "jslint.conf" is found in the Sublime Text 2 "User" packages directory, it will passed
        to jsl.
'''

def run(code, view, filename='untitled'):
  errors = check(code, filename)
  
  lines = set()
  underline = [] # leave this here for compatibility with original plugin
  
  errorMessages = {}
  def addMessage(lineno, message):
    message = str(message)
    if lineno in errorMessages:
      errorMessages[lineno].append(message)
    else:
      errorMessages[lineno] = [message]
  
  for line in errors.splitlines():
    match = re.match(r'^\((?P<line>\d+)\):\s+(?P<error>.+)', line)

    if match:
      error, line = match.group('error'), match.group('line')

      lineno = int(line) - 1
      lines.add(lineno)
      addMessage(lineno, error)

  return underline, lines, errorMessages, True
