# ios-base-project
Base iOS project creator script which initializes common components such as cocoapods and fastlane

# Config

Modify create.py variables:

```python
SRC_FOLDER = 'ios-base-project'
FOLDER_NAME = 'project-ios'
PROJECT_NAME = 'Sample App'
ORGANIZATION_NAME = 'My Company'
ORGANIZATION_IDENTIFIER = 'com.mycompany'
```

# Description
Performs the following tasks in the python script create.py:
* Copies SRC_FOLDER to FOLDER_NAME
* Renames files and directories based on the settings
* Renames contents of files to use the config settings
* Initializes the cocoapods