from bs4 import BeautifulSoup
import requests, os
from supp import *
from pathlib import Path

pmList = [''] # [title, link, status] and start from 1

print('Welcome to use DCFever message checker.\n')
s = requests.Session()
url = 'https://www.dcfever.com/users/login.php'

cookiesExist = Path('cookies')
if cookiesExist.exists():
    temp = input('Do you want to use the existing cookies to login?(Y/n) ')
    if str.lower(temp) == 'y':
        loginPage = login(s, url, True)
    else:
        loginPage = login(s, url, False)
else:
    loginPage = login(s, url, False)

option = ''
while True:
    displayUserInfo(loginPage)

    # load the first page of pm page
    temp = s.get('https://www.dcfever.com/pm/index.php')
    pm = BeautifulSoup(temp.text, 'lxml')

    showNumberOfNewPm(pm)
    retrieveAllPm(s, pm, pmList)  
    print('[1]\tCheck pm')
    print('[0]\tLeave\n')
    resp = input('Option: ')
    if resp == '0':
        break
    elif resp == '1':
       displayPmList(s, pmList)