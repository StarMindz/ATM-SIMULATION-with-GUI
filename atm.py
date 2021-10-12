# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 23:19:28 2021

@author: STARMINDS
"""

# THIS IS AN ATM MACHINE. YOU CAN WITHDRAW, DEPOSIT, CHANGE PIN, CHECK ACCOUNT DETAILS,CREATE A NEW ACCOUNT, CAN TRANSFER FROM
# ONE ACCOUNT TO ANOTHER, YOU CAN ALSO CHANGE PHONE NUMBER,



#FRONTEND LIBRARIES USING PYQT DESIGNER

#import libraries
import sys
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QSize, QTimer
#from PyQt5.QtGUI import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

#GLOBAL VARIABLES
accountno_list = [] 
global account
global data

#SUB FUNCTIONS

def strings():
    global account
    return str(account.account_name) + str(account.phone_number)  + str(account.pin) + "\n" + str(account.balance) + "\n" + str(account.account_number) + str(account.account_type)

def Account_list():  # opens list of all the account numbers in the database
    global accountno_list
    with open("ATM DATABASE\\ACCOUNT NO'S.txt", 'a+') as accountno:
        accountno.seek(0)
        accountno_list = [string for string in accountno]
Account_list()

def authenticate(pin, pin1):
    if int(pin)==int(pin1):
        return 1
    else:
        return 0
    
    
    
    
    
#BACKEND CODES
#CLASS
class Messages(QDialog):
    def __init__(self, sentence):
        self.sentence=sentence
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\dialog.ui", self)
        self.label.setText(self.sentence)
        self.label.adjustSize()
        self.pushButton.clicked.connect(self.ends)
        self.exec()
    
    def ends(self):
        self.close()

       
def message(sentence):
    new=Messages("  "+sentence)
    






class Account:
    pin = ""
    balance = 0
    phone_number = ""
    account_name = ""
    account_number = ""
    account_type=""
    email_address=""
    


    def __init__(self, name, phone, pin, no, balance):
        self.account_name = name
        self.phone_number = phone
        self.pin = pin
        self.balance = balance
        self.account_number = no
        

    def withdraw(self, amount):
        if amount>self.balance:
            insufficient_balance()
        else:
            self.balance -= amount

    def deposit(self, amount):
        self.balance += amount
        
    def transfer(self, account, amount):
        if amount>self.balance:
            insufficient_balance()
        else:
            self.balance -= amount
            account.balance+=amount
            
            
class Savings(Account):
    def __init__(self):
        super().__init__()
        self.account_type="Savings"
        
    
    
    
    
class Current(Account):
    def __init__(self):
        super().__init__()
        self.account_type="Current"
    
    
    
    
        





#MAJOR FUNCTIONS

def insufficient_balance():
    message("Insufficient Fund")


def withdraw(amount):
    amount=int(amount)
    global data
    global account
    if amount <= int(account.balance):
        account.withdraw(amount)
    else:
        message("\nYou do not have sufficient fund to make this withdrawal\nRequest for a lesser amount")
        return 0
    message("\nTake your cash\nYou have sucessfully withdrawn {} from your account\nPrevious balance: {} \nNew balance: {}".format(amount, amount + account.balance , account.balance))
    g = strings()
    data.write(g)
    data.seek(0)


def deposit(amount):
    amount=int(amount)
    global data
    global account
    account.deposit(int(amount))
    message(
        "\nYou have successfully deposited {} to your account.\nPrevious balance: {} \nNew balance: {} ".format(amount,
                                                                                                                account.balance - amount,
                                                                                                                account.balance))
    g = strings()
    data.write(g)
    data.seek(0)


def change_phone(phone):
    global data
    global account
    phone = input("\nType in your new phone number")
    account.phone_number = phone
    g = strings()
    data.write(g)
    data.seek(0)


def change_pin(pin, pin2):
    pin2 =int(pin2)
    global data
    global account
    if authenticate(pin, int(account.pin)) == 1:
        account.pin = pin2
        g = strings()
        data.write(g)
        data.seek(0)
        return True
    else:
        message("Your typed in a wrong old pin")
        return False


def transfer(amount, account_number):
    global data
    global account
    amount = int(amount)
    if amount <= int(account.balance):
        if account_number not in accountno_list:
            message("\nThis account does not exist.\nType in a valid account number")
        else:
            account.withdraw(amount)
            accountno = account_number
            data2 = open("ATM DATABASE\\" + str(accountno) + ".txt", 'r+')
            account_name = data2.readline()
            phone_number = data2.readline()
            pin1 = int(data2.readline())
            balance = int(data2.readline())
            account_number2 = data2.readline()
            account_type = data2.readline()
            data2.seek(0)
            account2 = Account(account_name, phone_number, pin1, account_number2, balance)
            account2.account_type=account_type
            account2.deposit(amount)
            string=str(account2.account_name) + str(account2.phone_number)  + str(account2.pin) + "\n" + str(account2.balance) + "\n" + str(account2.account_number) + str(account2.account_type)
            data2.write(string)
            data2.seek(0)
            g = strings()
            data.write(g)
            data.seek(0)
            return True
    else:
        insufficient_balance()
        return False
            
    
    

def Open_Account(accountno, pin):
    global accountno_list
    global account
    global data
    print("Good to go")
    print(accountno,pin)
    print(accountno_list)
    while True:
        if '\n' + accountno in accountno_list or accountno in accountno_list or accountno + '\n' in accountno_list:
            break
        else:
            print("Wrong Account No")
            return 0
    account_number = accountno
    data = open("ATM DATABASE\\" + str(accountno) + ".txt", 'r+')
    account_name = data.readline()
    phone_number = data.readline()
    pin1 = int(data.readline())
    balance = int(data.readline())
    account_number = data.readline()
    account_type = data.readline()
    data.seek(0)
    
    
    check=authenticate(pin, pin1)
    if check==1:
        account = Account(account_name, phone_number, pin, account_number, balance)
        account.account_type=account_type
        message("Welcome {}".format(account.account_name))
        return True
    else:
        message("Wrong Account or Pin")
        return False
        
        
        
def Create_Account(name, phone, pin, account_type):
    from random import randint
    while True:
        account_number = randint(1000000000, 9999999999)
        if account_number not in accountno_list:
            break
    balances = 0
    if account_type=="Savings":
        account = Account(name, phone, pin, account_number, balances)
        account.account_type=account_type
        message("\n\nCONGRATULATIONS\nYou successfully created a {} \nYour new account number is   \
        {}".format(account.account_type, account_number))
        with open("ATM DATABASE\\" + str(account_number) + ".txt",
                  'a+') as data:
            g = str(account.account_name) + "\n" + str(account.phone_number) + "\n" + str(account.pin) + "\n" + str(account.balance) + "\n" + str(account.account_number) + '\n' + str(account.account_type)
            data.write(g)

        with open("ATM DATABASE\\ACCOUNT NO'S.txt", 'a+') as data2:
            data2.write("\n" + str(account_number))
    else:
        account = Account(name, phone, pin, account_number, balances)
        account.account_type=account_type
        print("\n\nCONGRATULATIONS\nYou successfully created a {} \nYour new account number is   \
        {}".format(account.account_type, account_number))
        with open("ATM DATABASE\\" + str(account_number) + ".txt",
                  'a+') as data:
            g = str(account.account_name) + "\n" + str(account.phone_number) + "\n" + str(account.pin) + "\n" + str(account.balance) + "\n" + str(account.account_number) + '\n' + str(account.account_type)
            data.write(g)

        with open("ATM DATABASE\\ACCOUNT NO'S.txt", 'a+') as data2:
            data2.write("\n" + str(account_number))
    
    message("Congratulations, You successfully created an Account. \nYour account number is :{} \nand your ATM pin is {}".format(account_number, pin))









#FRONEND CODE
    
class Transfer(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\transfer.ui", self)
        self.show()
        self.pushButton_back1.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.transfer)
        
    def transfer(self):
        self.amount = self.lineEdit_amount.displayText()
        self.accountno =self.lineEdit_accountno.displayText()
        self.check=transfer(self.amount,self.accountno)
        if self.check == True:
            message("Transfer Successful")
            self.back()
        else:
            pass
        
    def back(self):
        self.close()
        self.new=Transactions()
        
        
class Balance(QMainWindow):
    def __init__(self):
        global account
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\balance.ui", self)
        self.show()
        self.sentence = "\n"+"Account Name: "+str(account.account_name)+"\nAccount Number: "+str(account.account_number) +"\nAccount Type: "+str(account.account_type)+"\nBalance: "+str(account.balance)
        self.label.setText(str(self.sentence))
        self.pushButton_back1.clicked.connect(self.back)
        
    def back(self):
        self.close()
        self.new=Transactions()
        
        
class Withdraw(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\withdraw.ui", self)
        self.show()
        self.pushButton.clicked.connect(self.withdraw)
        self.pushButton_back1.clicked.connect(self.back)
        
        
    def withdraw(self):
        self.amount=self.lineEdit_amount.displayText()
        withdraw(self.amount)
        self.back()
        
    def back(self):
        self.close()
        self.new=Transactions()

class Deposit(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\deposit.ui", self)
        self.show()
        self.pushButton_back1.clicked.connect(self.back)
        self.pushButton.clicked.connect(self.deposit)
        
    def deposit(self):
        self.amount=self.lineEdit_amount.displayText()
        deposit(self.amount)
        self.back()
        
    def back(self):
        self.close()
        self.new=Transactions()
        
class Pin(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\change pin.ui", self)
        self.show()
        self.pushButton.clicked.connect(self.change)
        self.pushButton_back1.clicked.connect(self.back)
        
    def change(self):
        self.old=self.lineEdit_pin1.displayText()
        self.new=self.lineEdit_pin2.displayText()
        self.check=change_pin(self.old,self.new)
        if self.check==True:
            message("You've successfully changed your pin")
            self.close()
            self.back()
        else:
            pass
        
    def back(self):
        self.close()
        self.new=Transactions()
        

class Transactions(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\transactions.ui", self)
        self.show()
        self.pushButton_pin.clicked.connect(self.pin)
        self.pushButton_transfer.clicked.connect(self.transfer)
        self.pushButton_balance.clicked.connect(self.balance)
        self.pushButton_withdraw.clicked.connect(self.withdraw)
        self.pushButton_deposit.clicked.connect(self.deposit)
        self.pushButton_back1.clicked.connect(self.back)
        
    def back(self):
        self.close()
        self.new=MainWindow()
    
    def pin(self):
        self.close()
        self.new=Pin()
    
    def transfer(self):
        self.close()
        self.new=Transfer()
        
    def balance(self):
        self.close()
        self.new=Balance()
        
    def withdraw(self):
        self.close()
        self.new=Withdraw()
        
    def deposit(self):
        self.close()
        self.new=Deposit()
    
        
        
    
        

class New_Account(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\creat_new.ui", self)
        self.pushButton_back1.clicked.connect(self.back)
        self.pushButton_join.clicked.connect(self.save)
        self.show()
        
    def save(self):
        self.account_type=self.comboBox_type.currentText()
        self.email=self.lineEdit_email.displayText()
        self.name=self.lineEdit_name.displayText()
        self.phone=self.lineEdit_phone.displayText()
        self.pin=self.lineEdit_pin.displayText()
        Create_Account(self.name, self.phone, self.pin,self.account_type)
        Account_list()
        print(self.account_type)
        self.close()
        self.new = MainWindow()
        
    def back(self):
        self.close()
        self.new = MainWindow()





        
        
        
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\main_window.ui", self)
        self.pushButton_new.clicked.connect(self.new_account)
        self.pushButton_enter.clicked.connect(self.authenticate)
        self.show()
        
    def new_account(self):
        self.close()
        self.new=New_Account()
        self.close()
        
    def authenticate(self):
        self.auth_accountno= self.lineEdit_accountno.displayText()
        self.auth_pin= self.lineEdit_2_pin.displayText()
        self.check=Open_Account(self.auth_accountno, self.auth_pin)
        if self.check==True:
            self.close()
            self.transact=Transactions()
        else:
            self.close()
            self.show()
            message("Wrong Account No or Pin")
        
    



class First_Window(QMainWindow):
    counter = 0
    def __init__(self):
        super().__init__()
        uic.loadUi("ATM GRAPHICS\\spleen_screen.ui", self)
        
        #remove title bar
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        
        #QTimer Start
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        
        #Timer in milliseconds
        self.timer.start(35)
    
        
        self.show()
        
        
    def progress(self):
        
        
        #set value to progress bar
        self.progressBar.setValue(self.counter)
        
        #close spleen screen and open main window
        if self.counter>100:
            self.timer.stop() #stop timer
            self.close()
            self.next = MainWindow()
            
        self.counter+=1


app= QApplication(sys.argv)
window = First_Window()
sys.exit(app.exec_())
        
        

























