from bs4 import BeautifulSoup
import requests, getpass, os, math, pickle

def login(currentSession, url, useCookies):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
    }
    allowCookies = 'n'

    while True:
        if not useCookies:
            username_login = input('E-mail: ')
            password_login = getpass.getpass(prompt='Password: ')
            allowCookies = input('Allow cookies?(Y/n) ')

            payload = {
            'username' : username_login,
            'password' : password_login,
            }
        
            if str.lower(allowCookies) == 'y':
                payload['autologin'] = '1'

            r = currentSession.get(url, headers = headers)
            soup = BeautifulSoup(r.content, 'lxml')
            payload['action'] = soup.find('input', attrs={'name' : 'action'})['value']
            loginPage = currentSession.post(url, data=payload, headers = headers)
        
        else:
            f = open('cookies', 'rb')
            currentSession.cookies.update(pickle.load(f))
            f.close()
            loginPage = currentSession.get('https://www.dcfever.com/users/index.php')

        tempLoginPage = BeautifulSoup(loginPage.text, 'lxml')

        if tempLoginPage.find(class_='info_div') == None:
            os.system('cls' if os.name == 'nt' else clear)
            print('Incorrect username or password.')
            print('Please try again.\n')
        else:
            break
    
    # store cookies
    if str.lower(allowCookies) == 'y':
        f = open('cookies', 'wb')
        pickle.dump(currentSession.cookies, f)
        f.close()

    # return main webpage after login process
    return loginPage

def displayUserInfo(loginPage):
    # parse the login webpage
    loginPage = BeautifulSoup(loginPage.text, 'lxml')
    temp = loginPage.find(class_='info_div').find('p').text.strip()

    username = loginPage.find(class_='info_div').find('h3').text
    regDate = temp[:temp.find('\t')]
    email = temp[temp.find('\t'):].strip()

    # print user info
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Welcome back! ' + username + '.')
    print('Registration Date: ' + regDate)
    print('E-mail: ' + email + '')

def showNumberOfNewPm(soupedPm):
    # show the numbers of new pm
    numberOfNewPm = soupedPm.find(class_='user_functions visible-md visible-lg').find_all('span')[2].text[1:-1].strip()

    if soupedPm.find(class_='user_functions visible-md visible-lg').find('img').get('src') == '/images/new_pm.gif':
        print('There are ' + str(numberOfNewPm) + ' new private message(s).\n')
    
    else:
        print('There are no new private message\n.')

def importAllPm(currentSession, soupedPm, pmList):
    numberOfTotalPm = soupedPm.find(class_='section_header').text.strip()[5:-5].strip()
    maxPage = math.ceil(int(numberOfTotalPm) / 25) # round it up
    
    counter = 1
    for singlePage in range(maxPage):
        pmUrl = 'https://www.dcfever.com/pm/index.php?page=' + str(singlePage + 1)
        soupedPm = BeautifulSoup(currentSession.get(pmUrl).text,'lxml')

        for i in soupedPm.find(class_='pm_list').find_all(True, {'class' : ['title', 'unread']}):
            pmList.append([i.text])
            pmList[counter].append('https://www.dcfever.com/pm/' + i.find('a').get('href'))
            
            if len(i.get('class')) == 1:
                pmList[counter].append('read')
            else:
                pmList[counter].append('unread')

            counter += 1

def displayPmList(currentSession, pmList):

    usrInput = None
    page = 1
    max_page = math.ceil((len(pmList) - 1) / 10) # first item will not be counted

    while True:
        # display page 1 by default
        os.system('cls' if os.name == 'nt' else 'clear')
        displayPmList_Displayitem(page, pmList)

        if page != 1:
            print('[,]\tPrevious page')
        if page != max_page:
            print('[.]\tNext page')
        print('[0]\tBack to home\n')
        
        while True:
            valid = True
            usrInput = input('Option:')

            # option list
            numberSet = list(range(len(pmList)))
            for i in range(len(numberSet)):
                numberSet[i] = str(numberSet[i])
            
            # validate usrInput
            if not (usrInput in numberSet) and usrInput != ',' and usrInput != '.':
                valid = False
            
            if page == 1 and usrInput == ',':
                valid = False

            if page == max_page and usrInput == '.':
                valid = False
            
            if not valid:
                print('Input error.')
                print('Please try again.\n')
            else:
                break
        
        if usrInput == ',':
            page -= 1
            continue
        
        elif usrInput == '.':
            page += 1
            continue

        elif usrInput == '0':
            break

        else:
            displayPmDetail(currentSession, int(usrInput), pmList)

def displayPmList_Displayitem(page, pmList):
    delta = (page - 1) * 10
    print('There are total ' + str(len(pmList)-1) + ' private message(s).')

    if 10 + delta > len(pmList) - 1:
        print('Now showing private message(s) from ' + str( 1 + delta) + ' to ' + str(len(pmList) - 1) + '\n')
        for i in range(11 + delta)[ 1 + delta: len(pmList)]:
            print('[' + str(i) + ']\t' + pmList[i][2] + '\t' + pmList[i][0])

    else:
        print('Now showing private message(s) from ' + str( 1 + delta) + ' to ' + str(10 + delta) + '\n')
        for i in range(11 + delta)[ 1 + delta:]:
            print('[' + str(i) + ']\t' + pmList[i][2] + '\t' + pmList[i][0])

def displayPmDetail(currentSession, pmNo, pmList):
    specificPm = currentSession.get(pmList[pmNo][1])
    pmContent = BeautifulSoup(specificPm.text, 'lxml')

    sender = pmContent.find(class_='pm_read_info').find_all(class_='col2')[0].text.strip()
    receiver = pmContent.find(class_='pm_read_info').find_all(class_='col2')[1].text.strip()
    date = pmContent.find(class_='pm_read_info').find_all(class_='col2')[2].text.strip()
    content = pmContent.find(class_='pm_read_content clear').find(class_='md').text.strip()
    os.system('cls' if os.name == 'nt' else 'clear')
    print('Sender: ' + sender)
    print('Receiver: ' + receiver)
    print('Date: ' + date)
    print('Summary:\n' + content + '\n')
    input('Press Enter to go back')