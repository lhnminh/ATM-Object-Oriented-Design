# The id/password: "aabuomar": "1234"
'''CSC 161 Lab: Computers and Programs

Minh Le
Lab Section TR 2:00-3:15pm
Spring 2020
'''

from graphics import GraphWin, Rectangle, Point, Text, Entry  # This is for extra credit
from time import sleep


def draw_ATM():
    '''
    This function is used for drawing the ATM
    return a GraphWin 
    '''
    win = GraphWin("ATM", 600, 600)
    rect = Rectangle(Point(50, 200), Point(500, 400))
    rect.draw(win)
    return win


def erase_ATM(win):
    '''
    This function is used for erasing the ATM
    '''
    eraser = Rectangle(Point(51, 201), Point(499, 399))
    eraser.setFill("White")
    eraser.draw(win)


def main_win():
    win = draw_ATM()
    u, ok = login_win(win)

    if not ok:
        erase_ATM(win)
        failed_win(win)
    else:
        erase_ATM(win)
        a = Account(u.id)
        m = Menu(a, win)
        m.welcome()
        sleep(0.5)
        erase_ATM(win)
        while m.cont is True:
            m.start()
            m.do_action()
            win.getMouse()
            erase_ATM(win)


class Menu():
    '''
    The class Menu is used for handling any action that the user may want
    It require a class Account to work on
    '''
    def __init__(self, u, win):
        self.action = ''
        self.helped = False
        self.account = u
        self.cont = True
        self.win = win

    def welcome(self):
        welcome = Text(Point(250, 300), f"Welcome user {self.account.id}")
        welcome.draw(self.win)

    def start(self):
        button = Rectangle(Point(250, 350), Point(350, 380))
        press = Text(Point(300, 365), "Continue")
        button.draw(self.win)
        press.draw(self.win)
        if self.helped == False:
            n = Text(Point(260, 250), "What would you like to do today?(Type help for menu) ")
            n.draw(self.win)
        elif self.helped == True:
            n = Text(Point(260, 250), "What else would you like to do today? ")
            n.draw(self.win)

        todo = Entry(Point(260, 300), 10)
        todo.draw(self.win)

        self.win.getMouse()

        todo.undraw()
        n.undraw()
        self.action = todo.getText()

    def do_action(self):
        possible = ["help", "check", "withdraw", "deposit", 'quit']
        if self.action == "help":
            Text(Point(222, 250), "Type check to check your balance").draw(self.win)
            Text(Point(260, 270), "Type withdraw to withdraw from your account").draw(self.win)
            Text(Point(217, 290), "Type deposit to make a deposit").draw(self.win)
            Text(Point(165, 310), "Type quit to quit").draw(self.win)
            self.helped = True

        elif self.action == "check":
            Text(Point(260, 250),
            f"The user {self.account.id} have ${self.account.balance} in your account").draw(self.win)
            self.helped = True

        elif self.action == "withdraw":
            prompt = Text(Point(260, 250), "Enter the amount of withdrawal")
            todo = Entry(Point(260, 300), 10)

            prompt.draw(self.win)
            todo.draw(self.win)

            self.win.getMouse()

            amount = float(todo.getText())
            prompt.undraw()
            todo.undraw()

            if amount <= self.account.balance:
                self.account.withdraw(amount)
                Text(Point(260, 250),
                     f"Successfully withdrawed ${amount} from account {self.account.id}").draw(self.win)
            elif amount > self.account.balance:
                Text(Point(260, 250),
                     f"Error, user tried to withdraw ${amount}\
 with a balance of ${self.account.balance}").draw(self.win)

            self.helped = True

        elif self.action == "deposit":
            prompt = Text(Point(260, 250), "Enter the amount of deposit")
            todo = Entry(Point(260, 300), 10)

            prompt.draw(self.win)
            todo.draw(self.win)

            self.win.getMouse()

            amount = float(todo.getText())
            prompt.undraw()
            todo.undraw()

            self.account.deposit(amount)
            Text(Point(260, 250),
                 f"Successfully deposited ${amount} into account {self.account.id}").draw(self.win)
            self.helped = True

        elif self.action not in possible:
            Text(Point(260, 250), "Unknown command").draw(self.win)
            self.helped = False

        elif self.action == "quit":
            Text(Point(260, 250), "You have successfully logged out").draw(self.win)
            self.cont = False


def login_win(win):
    u = User("", "")
    count = -1
    status = Point(0, 0)
    while count <= 7:
        count += 1
        if count == 0:
            a_ = Text(Point(150, 250), 'Please enter your user ID: ')
            a_.draw(win)
            b_ = Text(Point(150, 300), 'Please enter your PIN: ')
            b_.draw(win)

        _id, pin = get_inputs_win(win, count)
        u = User(_id, pin)

        if u.login() is False:
            status = Text(Point(300, 325), "Wrong input")
            status.setTextColor("red")
            status.draw(win)
            sleep(0.5)

        else:
            a_.undraw()
            b_.undraw()
            return u, True
        status.undraw()
    return u, False


def get_inputs_win(win, count):
    '''
    This function get the input of the user on the GUI
    '''

    a = Entry(Point(300, 250), 10)
    b = Entry(Point(300, 300), 10)
    button = Rectangle(Point(250, 350), Point(350, 380))
    press = Text(Point(300, 365), "Login")

    if count == 0:
        button.draw(win)
        press.draw(win)

    b.draw(win)
    a.draw(win)

    win.getMouse()

    a.undraw()
    b.undraw()

    a = a.getText()
    b = b.getText()
    return a, b


def failed_win(win):
    fail = Text(Point(250, 300), "Too many wrong attempts")
    fail2 = Text(Point(250, 325), "Click anywhere to quit")

    fail.draw(win)
    fail2.draw(win)

    win.getMouse()
    win.close()


class Account:
    '''
    The class Account is used for storing the id and their cash balances
    It's used when performing actions relating to cash balances
    '''
    def __init__(self, _id):
        balances = {"aaboumar": 10000, "mle": 100}
        self.id = _id
        self.balance = balances[_id]

    def withdraw(self, amount):
        self.balance -= amount

    def deposit(self, amount):
        self.balance += amount


class User:
    '''
    The class User is used for storing password and id
    It's used when signing in
    '''
    def __init__(self, _id, pin):
        self.id = _id
        self.pin = pin

    def login(self):
        info = {"aabuomar": "1234", "mle": "9999"}
        if self.id not in info.keys():
            return False
        elif self.id in info.keys() and self.pin not in info.values():
            return False
        elif self.id in info.keys() and self.pin in info.values():
            return True

main_win()
