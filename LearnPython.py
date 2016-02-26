# coding=utf-8
import os
import chardet
import re

CFG_PATH = r'C:\Users\Administrator\FindCode.ini'
PROMPT = '>>> '


def get_path():
    """返回用户之前设置的搜索文件的目录, 如果不存在则返回 None"""
    if os.path.exists(CFG_PATH):
        with open(CFG_PATH) as cfgFile:
            return cfgFile.readline()
    return None


def set_path():
    """设置用户需要搜索的路径"""
    global userPath
    print u'拖入需要查找的文件的目录:'
    userPath = raw_input(PROMPT).replace('/', '\\')
    if os.path.isdir(userPath):
        with open(CFG_PATH, 'w') as cfgFile:
            cfgFile.write(userPath)
            print u'设置成功'
            return True
    else:
        print u'路径输入错误'
        return False


# D:\Projects\Python\testDir
userPath = get_path()
if userPath is None or userPath is '':
    while not set_path():
        pass
print u'输入需要查找的关键词, 使用空格分隔, 输入 -c 修改需要查找的路径'
print u'当前路径:', userPath
while True:
    userInput = raw_input(PROMPT)
    while userInput == '-c':
        while not set_path():
            pass
        userInput = raw_input(PROMPT)
    if userInput == 'exit' or userInput == 'quit':
        break
    pattern = '(.*)' + userInput.lower().replace(' ', '(.*)') + '(.*)'
    for filePath, dirNames, fileNames in os.walk(userPath):
        for filename in fileNames:
            path = os.path.join(filePath, filename)
            with open(path) as userFile:
                for lineNumber, rawLine in enumerate(userFile):
                    det = chardet.detect(rawLine)
                    if det['encoding'] == None:
                        continue
                    detLine = rawLine.decode(det['encoding'], 'ignore').encode('gbk', 'ignore')
                    if re.match(pattern, detLine.lower()):
                        print u'==============================================================================='
                        print u'文件:', path
                        print u'行号:', lineNumber + 1
                        print u'内容:', detLine.strip('\n')
    print u'==============================================================================='
