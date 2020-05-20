import os
import json
import sys

def loadDirectory(directory):
    files, subdirs = [], []
    
    for subdir in next(os.walk(directory))[1]:
        subdirs.append(subdir)

    for file in next(os.walk(directory))[2]:
        files.append(file)

    return files, subdirs

def directoryExists(directory):
    return os.path.exists(directory)

def isWorkableFile(fileName):
    return len(fileName.split(".")) > 1

def getFileExtention(fileName):
    nameSplit = fileName.split(".")
    return nameSplit[len(nameSplit) - 1]

def loadJson(fileName):
    with open(fileName, "r") as f:
        return json.loads(f.read())
        
def loadFileTypes(subdirs):
    extentionDict = {}
    newSubdirs = []
    
    subdirData = loadJson("filetypes.json")
    for extention, subdir in subdirData.items():
        if not (subdir in subdirs or subdir in newSubdirs):
            newSubdirs.append(subdir)
        if not extention in extentionDict:
            extentionDict[extention] = subdir

    return extentionDict, newSubdirs

def checkNewExtentions(files, extentionDict):
    processed = []
    for file in files:
        if not isWorkableFile(file):
            continue
        extention = getFileExtention(file)
        if not extention in extentionDict:
            if not extention in processed:
                subdirectory = input(f"What subdirectory should the extention {extention} be placed into: ")
                if len(subdirectory) > 0:
                    extentionDict[extention] = subdirectory
                processed.append(extention)
    return extentionDict

def checkNewSubdirectories(subdirs, newSubdirs, extentionDict):
    for extention, subdir in extentionDict.items():
        if not (subdir in subdirs or subdir in newSubdirs):
            newSubdirs.append(subdir)
    return newSubdirs

def createDirectory(dirName):
    print(f"Creating directory {dirName}")
    if not directoryExists(dirName):
        os.makedirs(dirName)

def createDirectories(rootDir, dirs, subdirs):
    for subdir in dirs:
        createDirectory(rootDir + "\\" + subdir)
        subdirs.append(subdir)
    return subdirs

def moveFile(rootDir, filename, destination):
    print(f"Moving {filename} to {destination}")
    try:
        os.rename(rootDir + "\\" + filename, rootDir + "\\" + destination + "\\" + filename)
    except FileExistsError:
        print(f"Failed to move file {filename} as the target directory already has a file under that name")
    except PermissionError:
        print(f"Failed to move file {filename} as another program is using it")
    except:
        print(f"Failed to move file {filename}")

def main():
    SKIP_INPUT = False
    directory = ""
    arglen = len(sys.argv)
    if arglen > 1:
        directory = sys.argv[1]
    else:
        directory = input("Enter directory: ")
    
    if arglen > 2:
        SKIP_INPUT = sys.argv[2].lower() == "true"
    
    if not directoryExists(directory):
        return input("Directory not found")
        
    files, subdirs = loadDirectory(directory)
    extentionDict, newSubdirs = loadFileTypes(subdirs)
    if not SKIP_INPUT:
        extentionDict = checkNewExtentions(files, extentionDict)
    newSubdirs = checkNewSubdirectories(subdirs, newSubdirs, extentionDict)

    subdirs = createDirectories(directory, newSubdirs, subdirs)
    
    for file in files:
        if not isWorkableFile(file):
            continue
        extention = getFileExtention(file)
        if extention in extentionDict:
            destination = extentionDict[extention]
            moveFile(directory, file, destination)

    with open("filetypes.json", "w") as f:
        f.write(json.dumps(extentionDict))

main()
