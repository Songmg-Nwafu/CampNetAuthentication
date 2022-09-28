import CampNet

username = '' #学号
password = ''

a = CampNet.IfLogin(username, password)
if a.getStatus():
    msg = a.doLogin()
    if msg[1]:
        print('Successful!')
    else:
        print('Failed!')
    print(msg[0])