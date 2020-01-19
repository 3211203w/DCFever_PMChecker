from bs4 import BeautifulSoup
import requests
import os
import math
from supp import *

pmList = [''] # [title, link, status] and start from 1

print('Welcome to use DCFever message checker.\n')
s = requests.Session()
url = 'https://www.dcfever.com/users/login.php'

loginPage = login(s, url)

option = ''
while True:
    displayUserInfo(loginPage)

    # load the first page of pm page
    temp = s.get('https://www.dcfever.com/pm/index.php')
    pm = BeautifulSoup(temp.text, 'lxml')

    showNumberOfNewPm(pm)
    importAllPm(s, pm, pmList)  
    print('[1]\tCheck pm')
    print('[0]\tLeave\n')
    resp = input('Option: ')
    if resp == '0':
        break
    elif resp == '1':
       displayPmList(s, pmList)