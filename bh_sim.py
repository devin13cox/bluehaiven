
import tkinter as tk
import numpy as np
import random
#import pandas as pd
#import matplotlib as plt
num = 20
root = tk.Tk()
root.title('Blue Haiven Stream')
def click(event, cell):
    # can do different things with right (3) and left (1) mouse button clicks
    root.title("you clicked mouse button %d in cell %s" % (event.num, cell))
    # test right mouse button for equation solving
    # eg. data = '=9-3' would give 6
    if event.num == 3:
        # entry object in use
        obj = dict[cell]
        # get data in obj
        data = obj.get()
        # if it starts with '=' it's an equation
        if data.startswith('='):
            eq = data.lstrip('=')
            print(data, eq)
            try:
                # solve the equation
                result = eval(eq)
                #print result, type(result)  # test
                # remove equation data
                obj.delete(0, 'end')
                # update cell with equation result
                obj.insert(0, str(result))
            except:
                pass
def key_r(event, cell):
    # return/enter has been pressed
    data = dict[cell].get()  # get text/data in given cell
    #print cell, dict[cell], data  # test
    root.title("cell %s contains %s" % (cell, data))
# create a dictionary of key:value pairs
dict = {}
w = 20
h = 1
alpha = ["", 'NAME', 'STATUS', 'BPM', 'AVERAGE', 'DEVIATION', 'TIMER', 'LOCATION', 'CONTACT']
for row in range(num + 1):
    for col in range(9):
        if col == 0:
            # create row labels
            label1 = tk.Label(root, width=3, text=str(row))
            label1.grid(row=row, column=col, padx = 2, pady=2)
        elif row == 0:
            # create column labels
            label1 = tk.Label(root, width=w, text=alpha[col])
            label1.grid(row=row, column=col, padx = 2, pady=2)
        else:
            # create entry object
            entry1 = tk.Entry(root, width=w)
            # place the object
            entry1.grid(row=row, column=col)  #, padx = 2, pady=2)
            # create a dictionary of cell:object pair
            cell = "%s%s" % (alpha[col], row)
            dict[cell] = entry1
            # bind the object to a left mouse click
            entry1.bind('<Button-1>', lambda e, cell=cell: click(e, cell))
            # bind the object to a right mouse click
            entry1.bind('<Button-3>', lambda e, cell=cell: click(e, cell))
            # bind the object to a return/enter press
            entry1.bind('<Return>', lambda e, cell=cell: key_r(e, cell))

def create_data(n):
    persons = []
    firstnames = ['Devin', 'James', 'Hyeyeun', 'Jackson', 'Daniella', 'Conner', 'Everett', 'Michael',
                  'Richard', 'Emily', 'Sachi', 'Lindsay', 'Mickey', 'George', 'Daniel', 'Alexa',
                  'Jim', 'Michele', 'Martin', 'Dustin', 'Dani', 'Aaron', 'Caleb', 'Anthony',
                  'Pam', 'Daphne', 'Stephanie', 'Haley', 'Alleanna', 'Ashley', 'Darien', 'Ronald',
                  'Morgan', 'Amir']
    lastnames = ['Cox', 'Yellow', 'Chu', 'Oliver', 'Johnson', 'Dror', 'Morgan', 'Simpson', 'Helmers',
                 'Scott', 'Taharian', 'Morton', 'Kolus', 'Clark', 'Escajeda', 'Carter', 'George', 'Martin',
                 'Paulos', 'Chen', 'Miller', 'Nordstrom', 'Hunken', 'Freeman', 'Farsi', 'Peterson']
    r = 0
    for i in np.arange(n):
        rand = random.randint(0, len(firstnames) - 1)
        rand1 = random.randint(0, len(lastnames) - 1)
        persons.append(person(i, firstnames[rand], lastnames[rand1], r))
        r += 1
    return persons


class person:
    def __init__(self, master, firstname, lastname, rank):
        self.name = firstname + ' ' + lastname
        start = random.randint(60, 81)
        self.bpm = start
        self.location = [37.8715, 122.2730]
        self.contact = firstname + lastname + '@bluehaiven.com'
        self.status = 'GOOD'
        self.timer = 0
        self.timer_on = False
        self.timer_average = 0
        self.fever = False
        self.deviation = 0
        self.rank = rank + 1
        self.average = start

persons = create_data(num)
def simulate():
    #while True:
    for p in persons:
        p.bpm = update_bpm(p)
        p.location = update_location(p)
        p.deviation = update_differences(p)
        analyze_bpm(p)
        print(p)
    root.after(1000, simulate)

tick = 1
def update_bpm(p):
    global tick
    tick += 1
    coin_toss = random.randint(0,1)
    multiplier = 4
    if coin_toss != 0:
        rate = p.bpm + (random.randint(0, 3) / multiplier)
    else:
        rate = p.bpm - (random.randint(0, 3) / multiplier)
    if p.bpm < p.average - 5:
        rate += (2 / multiplier)
    if p.bpm > p.average + 5:
        rate -= (2 / multiplier)
    if p.fever and p.bpm < p.average + 15:
        rate += (2 / multiplier)
    p.average = round(((p.average * tick) + rate) / (tick + 1), 3)
    if rate > p.average + 8 and p.timer_on == False:
        p.timer_on = True
        p.timer_average = rate
    if rate < p.average + 8 and p.timer_on:
        p.timer_on = False
        p.timer = 0
    if p.timer_on:
        p.timer += 1
    p.timer_average = round(((p.timer_average * p.timer) + rate) / (p.timer + 1), 3)
    return rate

def update_location(p):
    coin_toss = random.randint(0,4)
    if coin_toss == 0:
        return [round(p.location[0] + 0.0015, 4), round(p.location[1], 4)]
    if coin_toss == 1:
        return [round(p.location[0] - 0.0015, 4), round(p.location[1], 4)]
    if coin_toss == 2:
        return [round(p.location[0], 4), round(p.location[1] + 0.0015, 4)]
    if coin_toss == 3:
        return [round(p.location[0], 4), round(p.location[1] - 0.0015, 4)]
    else:
        return p.location

def update_differences(p):
    val = p.bpm
    avg = p.average
    return round(val - avg, 3)

def analyze_bpm(p):
    status = dict['STATUS' + str(p.rank)].get()
    p.status = status
    if np.abs(85 - p.bpm) > 45:
        if p.status != 'ALERT' and p.status != 'HELP ON THE WAY' and p.status != 'HELP IS HERE':
            status = 'ALERT'
            trigger_response(p, status)
    elif p.timer > 24:
        if p.status != 'WARNING' and p.status != 'I AM GOOD' and p.status != 'SEND HELP' and p.status != 'ANALYZE':
            if p.status != 'HELP ON THE WAY' and p.status != 'HELP IS HERE':
                status = 'WARNING'
                trigger_response(p, status)
    else:
        status = 'GOOD'
    if p.status == 'HELP ON THE WAY' or p.status == 'HELP IS HERE':
        status = p.status
    update_person(p, status)

def trigger_response(p, txt):
    if txt == 'ALERT':
        trigger = tk.Tk()
        Alert(trigger, 'ALERT: ' + p.name + ' has reached bpm of: ' + str(p.bpm) + '. Help Requested',
              'ALERT', 'STATUS', p.rank)
        return 'ALERT'
    elif txt == 'WARNING':
        trigger = tk.Tk()
        Alert(trigger, 'WARNING: ' + p.name + ' has had a 24 hour increase in average heart rate. '
              + 'Their average heart rate is: ' + str(p.average) + '. Average over last 24 hours is: '
              + str(p.timer_average) + '. This is an average increase of '
              + str(round(p.timer_average - p.average, 3)) + '. Please Monitor',
              'WARN', 'STATUS', p.rank)
        return 'WARNING'
    else:
        trigger = tk.Tk()
        Alert(trigger, 'MONITORING')
        return 'MONITORING'

def update_person(p, status):
    rank = p.rank
    p.status = status
    set_text(p.name, 'NAME', str(p.rank))
    set_text(p.status, 'STATUS', str(p.rank))
    set_text(p.bpm, 'BPM', str(p.rank))
    set_text(p.deviation, 'DEVIATION', str(p.rank))
    set_text(p.timer, 'TIMER', str(p.rank))
    set_text(p.location, 'LOCATION', str(p.rank))
    set_text(p.contact, 'CONTACT', str(p.rank))
    set_text(p.average, 'AVERAGE', str(p.rank))

    return #set_text('Put me in!', )

def set_text(text, row, column):
    cell = row + column
    obj = dict[cell]
    obj.delete(0, 'end')
    # update cell with equation result
    obj.insert(0, text)

  #  e.delete(0,tk.END)
  #  e.insert(19,text)
    return

def inject():
    select = random.randint(0, len(persons) - 1)
    persons[select].bpm = 168

def scare():
    select = random.randint(0, len(persons) - 1)
    persons[select].bpm = persons[select].average + 12
    persons[select].fever = True

class Alert:
    def __init__(self, master, txt, severity, row, column):
        self.label=tk.Label(master)
        self.label.grid(row=0,column=0)
        self.label.configure(text=txt)
        self.count = 0
        self.severity = severity
        self.row = row
        self.column = column
        if severity == 'ALERT':
            txt1 = 'HELP ON THE WAY'
            txt2 = 'HELP IS HERE'
        else:
            txt1 = 'ANALYZE'
            txt2 = 'SEND HELP'

        def first():
            txt = txt1
            row = self.row
            column = self.column
            status_update(txt, row, column)
        def second():
            txt = txt2
            row = self.row
            column = self.column
            status_update(txt, row, column)



        self.btn = tk.Button(master, text = txt1, bd = '5', command = first)
        self.btn.grid(row=1, column=1, columnspan=1)
        self.btn2 = tk.Button(master, text = txt2, bd = '5', command = second)
        self.btn2.grid(row=1, column=2, columnspan=1)

def status_update(txt, row, column):
    set_text(txt, str(row), str(column))
    if txt == 'SEND HELP':
        trigger = tk.Tk()
        Alert(trigger, 'ALERT: Help Requested', 'ALERT', 'STATUS', column)



#print dict  # test
# set the focus on cell A1
dict['NAME1'].focus()
btn = tk.Button(root, text = 'ALERT!', bd = '5', command = inject)
btn.grid(row=num + 1, column=3, columnspan=1)
btn2 = tk.Button(root, text = 'FEVER!', bd = '5', command = scare)
btn2.grid(row=num + 1, column=2, columnspan=1)
root.after(1000, simulate)
root.mainloop()