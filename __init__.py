#ECHO
#Ddeveloped by William Scargil
import os

cwd = os.getcwd()
path = (cwd + "\\echo")
os.chdir(path)


from .client import load
from .client import help



