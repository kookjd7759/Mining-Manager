from cx_Freeze import setup, Executable
import sys

buildOptions = {
	"packages":[
    	'sys', 'random', 'time', 'datetime',
        'PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 
        'requests', 'json'
    ],
    "excludes":[
        
    ]
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

exe = [Executable("Main.py", base=base)]
 
setup(
    name='Mining Manager',
    version='1.0.0b1',
    author='Donggyun_7759',
    options = dict(build_exe = buildOptions),
    executables = exe
)