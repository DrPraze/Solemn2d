import sys
from cx_Freeze import setup, Executable

exe = Executable(
    script=r"Skeleton.py",
    base="Win32GUI",
    )

setup(
    name = "Solemn2D",
    version = "1.0",
    description = "Simple Animator app",
    executables = [exe]
    )





