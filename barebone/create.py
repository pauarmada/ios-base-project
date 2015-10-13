import glob, os
import shutil

from tempfile import mkstemp
from shutil import move
from os import remove, close

from subprocess import call

"""
GLOBAL SETTINGS
"""

SRC_FOLDER = 'ios-base-project'
FOLDER_NAME = 'project-ios'
PROJECT_NAME = 'Sample App'
ORGANIZATION_NAME = 'My Company'
ORGANIZATION_IDENTIFIER = 'com.mycompany'

"""
END GLOBAL SETTINGS
"""

def replace(file_path, pattern, subst):
    #Create temp file
    fh, abs_path = mkstemp()
    with open(abs_path,'w') as new_file:
        with open(file_path) as old_file:
            for line in old_file:
                new_file.write(line.replace(pattern, subst))
    close(fh)
    #Remove original file
    remove(file_path)
    #Move new file
    move(abs_path, file_path)


def renameProjectFile(filename):
    idx = filename.rfind("/")
    path = filename[:idx]
    name = filename[idx+1:]

    if "PROJECTNAME" in name:
        os.rename(filename, path + "/" + name.replace("PROJECTNAME", PROJECT_NAME))

def rename(dir, pattern):
    for pathAndFilename in glob.iglob(os.path.join(dir, pattern)):
        if (os.path.isfile(pathAndFilename)):
            replace(pathAndFilename, "PROJECTNAME", PROJECT_NAME)
            replace(pathAndFilename, "ORGANIATIONNAME", ORGANIZATION_NAME)
            replace(pathAndFilename, "ORGANIZATIONIDENTIFIER", ORGANIZATION_IDENTIFIER)
                
            renameProjectFile(pathAndFilename)

def listDirs(dir):
    for root, subFolders, files in os.walk(dir, topdown=False):
        for folder in subFolders:
           yield os.path.join(root,folder)
    return

def copyDirectory(src, dest):
    try:
        shutil.copytree(src, dest)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not copied. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not copied. Error: %s' % e)

def removeDirectory(src):
    try:
        shutil.rmtree(src)
    # Directories are the same
    except shutil.Error as e:
        print('Directory not deleted. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('Directory not deleted. Error: %s' % e)

def removeFile(src):
    try:
        shutil.remove(src)
    # Directories are the same
    except shutil.Error as e:
        print('File not deleted. Error: %s' % e)
    # Any error saying that the directory doesn't exist
    except OSError as e:
        print('File not deleted. Error: %s' % e)


print "Removing " + FOLDER_NAME
removeDirectory(FOLDER_NAME)

print "Making sure other files are removed"
#removeFile(SRC_FOLDER+"/PodFile.lock")
#removeDirectory(SRC_FOLDER+"/Pods"+Pods)
removeDirectory(SRC_FOLDER+"/PROJECTNAME.xcodeproj/project.xcworkspace")
removeDirectory(SRC_FOLDER+"/PROJECTNAME.xcodeproj/xcuserdata")
removeDirectory(SRC_FOLDER+"/PROJECTNAME.xcworkspace/xcuserdata")

print "Copying source directory to " + FOLDER_NAME
copyDirectory('./'+SRC_FOLDER, FOLDER_NAME)


print "Renaming project files:"
print "Project Name: " + PROJECT_NAME
print "Organization Name: " + ORGANIZATION_NAME
print "Organization Identifier: " + ORGANIZATION_IDENTIFIER
listDirs('./'+FOLDER_NAME)

for path in listDirs(FOLDER_NAME):
    rename(path, "*.*")
    renameProjectFile(path)

print "Running cocoapods"
print os.path.abspath(FOLDER_NAME)
os.chdir(FOLDER_NAME)
call(["pod", "install"])