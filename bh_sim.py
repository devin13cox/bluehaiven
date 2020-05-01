
import tkinter as tk
import numpy as np
import random

num = 20
root = tk.Tk()
root.title('Blue Haiven Stream')


def key_r(event, cell):
    # return/enter has been pressed
    data = dict[cell].get()  # get text/data in given cell
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
            entry1.grid(row=row, column=col)  # , padx = 2, pady=2)
            # create a dictionary of cell:object pair
            cell = "%s%s" % (alpha[col], row)
            dict[cell] = entry1


# Create timestamp entry box at bottom
tick_entry = tk.Entry(root, width=w + 1)
tick_entry.grid(row=num + 1, column=5)
tick_entry.delete(0, 'end')
# update cell with equation result
tick_entry.insert(0, 'Timestamp: ' + str(0) + 'hours')
tick_entry.configure(bg='lightblue')

# Create Cases entry box
cases_entry = tk.Entry(root, width=w + 16)
cases_entry.grid(row=num + 1, column=6)
cases_entry.delete(0, 'end')
# update cell with equation result
cases_entry.insert(0, 'Cases: ' + str(0) + ', which is ' + str(0) + '% of your company')
cases_entry.configure(bg='lightblue')


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
        persons.append(Person(i, firstnames[rand], lastnames[rand1], r))
        r += 1
    return persons


class Person:
    def __init__(self, master, firstname, lastname, rank):
        self.name = firstname + ' ' + lastname
        start = random.randint(60, 81)
        self.bpm = start
        self.location = [37.8715 + ((random.randint(0, 150) - 50) / 1000),
                         122.2730 + ((random.randint(0, 150) - 50) / 1000)]
        self.contact = firstname + lastname + '@bluehaiven.com'
        self.status = 'GOOD'
        self.timer = 0
        self.timer_on = False
        self.timer_average = 0
        self.fever = False
        self.interaction_check = list()
        self.interactions = []
        self.deviation = 0
        self.rank = rank + 1
        self.average = start


persons = create_data(num)
tick = 1
cases = []  # track people who have been sick.


def simulate():
    global tick
    tick += 1
    for p in persons:
        p.bpm = update_bpm(p)
        p.location = update_location(p)
        p.deviation = update_differences(p)
        analyze_bpm(p)
        print(p)
    analyze_location(persons)
    tick_entry.delete(0, 'end')
    tick_entry.insert(0, 'Timestamp: ' + str(tick) + ' hours')
    cases_entry.delete(0, 'end')
    cases_entry.insert(0, 'Cases: ' + str(len(cases)) + ', which is ' + str(len(cases) * 100 / num) +
                       '% of your company')
    root.after(1000, simulate)


def update_bpm(p):
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
        rate += (3 / multiplier)
    if not p.timer_on:
        p.average = round(((p.average * tick) + rate) / (tick + 1), 3)
    if rate > p.average + 8 and not p.timer_on:
        p.timer_on = True
        p.timer_average = rate
    if rate < p.average + 8 and p.timer_on:
        p.timer_on = False
        p.timer = 0
    if p.timer_on:
        p.timer += 1
    p.timer_average = round(((p.timer_average * p.timer) + rate) / (p.timer + 1), 3)
    return round(rate, 3)


def update_location(p):
    coin_toss = random.randint(0, 4)
    if coin_toss == 0:
        return [round(p.location[0] + 0.0015, 4), round(p.location[1], 4)]
    if coin_toss == 1:
        return [round(p.location[0] - 0.0015, 4), round(p.location[1], 4)]
    if coin_toss == 2:
        return [round(p.location[0], 4), round(p.location[1] + 0.0001, 4)]
    if coin_toss == 3:
        return [round(p.location[0], 4), round(p.location[1] - 0.0001, 4)]
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
        if p.status != 'WARNING' and p.status != 'I AM GOOD' and p.status != 'SEND HELP' and \
                p.status != 'ANALYZE':
            if p.status != 'HELP ON THE WAY' and p.status != 'HELP IS HERE':
                status = 'WARNING'
                trigger_response(p, status)
        if p not in cases:
            cases.append(p)
    else:
        status = 'GOOD'
    if p.status == 'HELP ON THE WAY' or p.status == 'HELP IS HERE':
        status = p.status
    update_person(p, status)


def trigger_response(p, txt):
    if txt == 'ALERT':
        trigger = tk.Tk()
        Alert(trigger, 'ALERT: ' + p.name + ' has reached bpm of: ' + str(p.bpm) + '. Help Requested',
              'ALERT', 'STATUS', p.rank, p)
        return 'ALERT'
    elif txt == 'WARNING':
        trigger = tk.Tk()
        Alert(trigger, 'WARNING: ' + p.name + ' has had a 24 hour increase in average heart rate. '
              + 'Their average heart rate is: ' + str(p.average) + '. Average over last 24 hours is: '
              + str(p.timer_average) + '. This is an average increase of '
              + str(round(p.timer_average - p.average, 3)) + '. They have had ' + str(len(p.interaction_check) - 1)
              + ' interaction(s) within a potentially contagious period. Please Monitor',
              'WARN', 'STATUS', p.rank, p)
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

    return


def analyze_location(people):
    for p in people:
        for i in people:
            if np.abs(np.sqrt(((p.location[0] - i.location[0]) ** 2) +
                              ((p.location[0] - i.location[0]) ** 2))) < 0.001:
                if i in p.interaction_check:
                    for inter in p.interactions:
                        if inter[0] == i.name:
                            inter[3] = 'Last Interaction: ' + str(tick)
                            inter[4] += 1
                else:
                    p.interactions.append([i.name, p.location, 'First Interaction: ' + str(tick),
                                           'Last Interaction:' + str(tick), 1])
                    p.interaction_check.append(i)


def set_text(text, row, column):
    cell = row + column
    obj = dict[cell]
    obj.delete(0, 'end')
    # update cell with equation result
    obj.insert(0, text)
    return


def inject():
    select = random.randint(0, len(persons) - 1)
    persons[select].bpm = 168


def scare():
    select = random.randint(0, len(persons) - 1)
    persons[select].bpm = persons[select].average + 12
    persons[select].fever = True


class Alert:
    def __init__(self, master, txt, severity, row, column, person):
        self.label=tk.Label(master)
        self.label.grid(row=0,column=0)
        self.label.configure(text=txt, wraplength=1000, highlightcolor='red')
        self.count = 0
        self.severity = severity
        self.row = row
        self.person = person
        self.column = column
        if severity == 'ALERT':
            txt1 = 'HELP ON THE WAY'
            txt2 = 'HELP IS HERE'
        else:
            txt1 = 'ANALYZE'
            txt2 = 'SEND HELP'

        def first():
            stat_txt = txt1
            stat_row = self.row
            stat_column = self.column
            status_update(stat_txt, stat_row, stat_column, self.person)

        def second():
            stat_txt = txt2
            stat_row = self.row
            stat_column = self.column
            status_update(stat_txt, stat_row, stat_column, self.person)

        self.btn = tk.Button(master, text = txt1, bd = '5', command = first)
        self.btn.grid(row=1, column=1, columnspan=1)
        self.btn2 = tk.Button(master, text = txt2, bd = '5', command = second)
        self.btn2.grid(row=1, column=2, columnspan=1)


def status_update(txt, row, column, p):
    set_text(txt, str(row), str(column))
    if txt == 'SEND HELP':
        trigger = tk.Tk()
        Alert(trigger, 'ALERT: Help Requested', 'ALERT', 'STATUS', column, p)
    elif txt == 'ANALYZE':
        trigger = tk.Tk()
        Alert(trigger, 'Analyzing: ' + p.name + ' has had the following interactions to consider, in'
              + ' the form of [Name, Location, First Timestamp, Last Timestamp, Number Interactions]: '
              + '\n'
              + str(p.interactions[1:]), 'WARN', 'STATUS', p.rank, p) + '\n' + ''
        return 'ANALYZE'


dict['NAME1'].focus()
btn = tk.Button(root, text='ALERT!', bd='5', command=inject)
btn.grid(row=num + 1, column=3, columnspan=1)
btn2 = tk.Button(root, text='FEVER!', bd='5', command=scare)
btn2.grid(row=num + 1, column=2, columnspan=1)
root.after(1000, simulate)
root.mainloop()
