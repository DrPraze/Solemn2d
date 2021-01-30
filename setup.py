import sys
from cx_Freeze import setup, Executable

exe = Executable(
    script=r"Skeleton.py",
    base="Win32GUI",
    )

setup(
    name = "Skeleton2D",
    version = "0.0",
    description = "Beta version",
    executables = [exe]
    )


