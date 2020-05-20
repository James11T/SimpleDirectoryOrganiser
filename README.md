# Simple Directory Organiser
## Usage
The directory organiser can be used in 2 ways, directly from the python file where the user will be prompted to enter the directory they wish to organise based on the current organization model saved. And the second method being with a bat file to automate the input of the directory, like shown below
```bat
@echo off
cls
python main.py <DIRECTORY>
```
## Building a model
Upon organizing a directory, if the program encounters a file type is has not yet seen it will prompt the user to enter a directory of a directory that already exists or one that doesn't exist and needs to be created.
The program will remember the user’s choices and wont prompt the user based on that file type again. If the user is prompted to enter a directory for a file type, they do not want sorted they can choose this by not entering any directory name and just hitting enter.
