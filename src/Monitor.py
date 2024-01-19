import DB
import Web

for key in Web.Url_dictionary:
    data = Web.getList(key)
    print(key)
    print(data)