import Web

DBPATH = './Mining Manager/DataBase/'
WEBHOOK_DB_NAME = 'WEBHOOK'
CHECKINGTIME_DB_NAME = 'Option_time'
INFO_DB_NAME = 'Option_info'
WHEN_DB_NAME = 'Option_when'

CheckingTime_list = [1, 3, 5, 10, 15, 20]

def getPath(name):
    return f'{DBPATH}{name}.txt'

def mktxt(name):
    url = getPath(name)
    file = open(url, 'w')
    file.write('')
    file.close()


def DBinit():
    for key in Web.Url_dictionary:
        url = getPath(key)
        try:
            file = open(url, 'r')
        except FileNotFoundError:
            file = open(url, 'w')
            file.write('')
        file.close()

def loadWEBHOOK():
    url = getPath(WEBHOOK_DB_NAME)

    try:
        file = open(url, 'r')
    except FileNotFoundError:
        print(f'File Not found, Create one{url} ')
        mktxt(WEBHOOK_DB_NAME)
    
    file = open(url, 'r')
    WEBHOOK = file.readline()
    file.close()
    print(f'DB.loadWEBHOOK():: load \"{WEBHOOK}\" in {url}')
    return WEBHOOK

def saveWEBHOOK(text):
    url = getPath(WEBHOOK_DB_NAME)
    print(f'DB.saveWEBHOOK():: save(update) {url}')
    file = open(url, 'w')
    file.write(text)
    print(f' -> \"{text}\"')
    file.close()

def loadCheckingTime():
    url = getPath(CHECKINGTIME_DB_NAME)

    try:
        file = open(url, 'r')
    except FileNotFoundError:
        print(f'File Not found, Create one{url} ')
        mktxt(CHECKINGTIME_DB_NAME)

    file = open(url, 'r')
    checkingTime = file.readline()
    file.close()
    print(f'DB.loadCheckingTime():: load \"{checkingTime}\" in {url}')
    return checkingTime

def saveCheckingTime(checkingTime):
    url = getPath(CHECKINGTIME_DB_NAME)
    print(f'DB.saveCheckingTime():: save(update) {url}')
    file = open(url, 'w')
    file.write(str(checkingTime))
    print(f' -> \"{checkingTime}\"')
    file.close()

def loadInfo():
    url = getPath(INFO_DB_NAME)

    try:
        file = open(url, 'r')
    except FileNotFoundError:
        print(f'File Not found, Create one{url} ')
        mktxt(INFO_DB_NAME)

    file = open(url, 'r')
    seq = file.readline()
    file.close()
    print(f'DB.loadInfo():: load \"{seq}\" in {url}')
    return seq

def saveInfo(seq):
    url = getPath(INFO_DB_NAME)
    print(f'DB.saveInfo():: save(update) {url}')
    file = open(url, 'w')
    file.write(seq)
    print(f' -> \"{seq}\"')
    file.close()

def loadWhen():
    url = getPath(WHEN_DB_NAME)
    
    try:
        file = open(url, 'r')
    except FileNotFoundError:
        print(f'File Not found, Create one{url} ')
        mktxt(WHEN_DB_NAME)

    file = open(url, 'r')
    seq = file.readline()
    file.close()
    print(f'DB.loadWhen():: load \"{seq}\" in {url}')
    return seq

def saveWhen(seq):
    url = getPath(WHEN_DB_NAME)
    print(f'DB.saveWhen():: save(update) {url}')
    file = open(url, 'w')
    file.write(seq)
    print(f' -> \"{seq}\"')
    file.close()

def Reset_default_values():
    print('DB::Reset_default_values():: Reset default values')
    saveCheckingTime(CheckingTime_list[2])
    saveInfo('11000')
    saveWhen('101')

# name = File name without '.txt'
# workers = worker List
## save or update the DataBase 
def saveDB(key, workers):
    print(f'Start save DB \"{key}.txt\" ... ')
    url = getPath(key)
    file = open(url, 'w')
    for worker in workers:
        file.write(f'{worker}\n')
    file.close()
    print(f'Successfully saved')

# name = file Name without '.txt'
## load the DataBase 
def loadDB(key):
    print(f'Start load DB \"{key}.txt\" ... ')
    url = getPath(key)
    file = open(url, 'r')
    resultList = []
    while True:
        line = file.readline()
        if not line:
            break
        resultList.append(line[0:len(line) - 1])

    file.close()
    print(f'Successfully loaded')

    return resultList


