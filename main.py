from bs4 import BeautifulSoup
import requests
import getpass
import os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

print('Welcome to use DCFever message checker.')
print('E-mail: ', end = '')
username_login = input()
password_login = getpass.getpass(prompt='Password: ')

payload = {
    'username' : username_login,
    'password' : password_login,
    'autologin' : '1'
}

s = requests.Session()
url = 'https://www.dcfever.com/users/login.php'

r = s.get(url, headers = headers)
soup = BeautifulSoup(r.content, 'lxml')
payload['action'] = soup.find('input', attrs={'name' : 'action'})['value']

# receive main webpage after posting    
login = s.post(url, data=payload, headers = headers)

# parse the login webpage
login = BeautifulSoup(login.text, 'lxml')
temp = login.find(class_='info_div').find('p').text.strip()

username = login.find(class_='info_div').find('h3').text
regDate = temp[:temp.find('\t')]
email = temp[temp.find('\t'):].strip()

# print user info
os.system('cls' if os.name == 'nt' else 'clear')
print('Welcome back! ' + username + '.')
print('Registration Date: ' + regDate)
print('E-mail: ' + email)
print()

# receive pm webpage after posting
temp = s.get('https://www.dcfever.com/pm/index.php')

pm = BeautifulSoup(temp.text, 'lxml')
numberOfNewPm = pm.find(class_='user_functions visible-md visible-lg').find_all('span')[2].text[1:-1].strip()

if pm.find(class_='user_functions visible-md visible-lg').find('img').get('src') == '/images/new_pm.gif':
    print('There are ' + str(numberOfNewPm) + ' new private message(s).')
