DBPATH = './Mining Manager/DataBase/'
WEBHOOK_DB_NAME = 'WEBHOOK'
CHECKINGTIME_DB_NAME = 'Option_time'
INFO_DB_NAME = 'Option_info'
WHEN_DB_NAME = 'Option_when'

CheckingTime_list = [1, 3, 5, 10, 15, 20]

def getPath(name):
    return f'{DBPATH}{name}.txt'

def loadWEBHOOK():
    url = getPath(WEBHOOK_DB_NAME)
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
    saveInfo('00000')
    saveWhen('000')

# name = File name without '.txt'
# workers = worker List
## save or update the DataBase 
def saveDB(name, workers):
    print(f'Start save DB \"{name}.txt\" ... ')
    url = getPath(name)
    file = open(url, 'w')
    for worker in workers:
        file.write(f'{worker}\n')
    file.close()
    print(f'Successfully saved')

# name = file Name without '.txt'
## load the DataBase 
def loadDB(name):
    print(f'Start load DB \"{name}.txt\" ... ')
    url = getPath(name)
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

