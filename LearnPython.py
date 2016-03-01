# coding=utf-8
import os
import chardet
import re
import time

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
    print u'***  拖入需要查找的文件的目录:'
    userPath = raw_input(PROMPT).replace('/', '\\')
    if os.path.isdir(userPath):
        with open(CFG_PATH, 'w') as cfgFile:
            cfgFile.write(userPath)
            print u'***  设置成功'
            return True
    else:
        print u'***  路径输入错误'
        return False


# D:\Projects\Python\testDir
userPath = get_path()
if userPath is None or userPath is '':
    while not set_path():
        pass
print u'''***  输入需要查找的关键词, 使用空格分隔
***  输入 -c 修改需要查找的路径
***  展示最多 10 条搜索结果
***  当前路径:''', userPath
while True:
    userInput = raw_input(PROMPT)
    # tmpTime = time.time()
    while userInput == '-c':
        while not set_path():
            pass
        userInput = raw_input(PROMPT)
    if userInput == 'exit' or userInput == 'quit':
        break
    pattern = '(.*)' + userInput.lower().replace(' ', '(.*)') + '(.*)'
    for filePath, dirNames, fileNames in os.walk(userPath):
        count = 10
        for filename in fileNames:
            if not count:
                break
            path = os.path.join(filePath, filename)
            if os.path.getsize(path) > 1 * 1024 * 1024:
                continue
            with open(path) as userFile:
                for lineNumber, rawLine in enumerate(userFile):
                    if not count:
                        break
                    # det = chardet.detect(rawLine)
                    # if det['encoding'] is None:
                    #     continue
                    detLine = rawLine.decode('UTF-8', 'ignore').encode('GBK', 'ignore')
                    # detLine = rawLine.decode(det['encoding'], 'ignore').encode('gbk', 'ignore')
                    if re.match(pattern, detLine.lower()):
                        count -= 1
                        print u'==============================================================================='
                        print u'文件:', path
                        print u'行号:', lineNumber + 1
                        print u'内容:', detLine.strip('\n')
    print u'==============================================================================='
    # print time.time() - tmpTime


