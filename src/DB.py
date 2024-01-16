DBPATH = './Mining Manager/DataBase/'
WEBHOOK_DB_NAME = 'WEBHOOK'
CHECKINGTIME_DB_NAME = 'CheckingTime'

CheckingTime_list = [1, 3, 5, 10, 15, 20]

## getPath ./Mining Manager/DataBase/ + name + .text
def getPath(name):
    return f'{DBPATH}{name}.txt'

## load WebHook url
def loadWEBHOOK():
    url = getPath(WEBHOOK_DB_NAME)
    file = open(url, 'r')
    WEBHOOK = file.readline()
    file.close()
    print(f'DB.loadWEBHOOK():: load \"{WEBHOOK}\" in {url}')
    return WEBHOOK

# text = WebHook url
## save or update WebHook
def saveWEBHOOK(text):
    url = getPath(WEBHOOK_DB_NAME)
    print(f'DB.saveWEBHOOK():: save(update) {url}')
    file = open(url, 'w')
    file.write(text)
    print(f' -> \"{text}\"')
    file.close()

## load checking time index
def loadCheckingTime():
    url = getPath(CHECKINGTIME_DB_NAME)
    file = open(url, 'r')
    checkingTime = file.readline()
    file.close()
    print(f'DB.loadCheckingTimeIdx():: load \"{checkingTime}\" in {url}')
    return int(checkingTime)

# checkingTime = Checking time index
## save or update checkingTime
def saveCheckingTime(checkingTime):
    url = getPath(CHECKINGTIME_DB_NAME)
    print(f'DB.saveCheckingTimeIdx():: save(update) {url}')
    file = open(url, 'w')
    file.write(str(checkingTime))
    print(f' -> \"{checkingTime}\"')
    file.close()

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

