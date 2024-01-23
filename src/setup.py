from cx_Freeze import setup, Executable
import sys

buildOptions = {
	"packages":[
    	'sys','random','time','datetime','PyQt5.QtWidgets', 'PyQt5.QtGui', 'PyQt5.QtCore', 'requests', 'json'
    ],
    "excludes":[

    ]
}
 
exe = [Executable('Main.py', base='Win32GUI')]
 
setup(
    name='Mining Manager',
    version='1.0.0b1',
    author='Donggyun_7759',
    options = dict(build_exe = buildOptions),
    executables = exe
)