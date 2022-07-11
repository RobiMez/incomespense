# pylint: disable=fixme
"""Main execution script"""

from os import system, path
import time
import ast

from colors import C, P
c = C()
p = P()

# create file if not exists
if not path.exists('db'):
    with open('db', 'w', encoding='utf-8') as file:
        file.close()

    # ----------[ income side ]     [ Printing Function ]    [Expense side]------------
    # <--------------23-----><3><-----10-><4->|<4-><---10---><3><-----------26-------->
    #             dlfkjalskdj : 0000000000 [+]|
    # flskdjfalksjdlfkjalskdj : 0000000000 [+]|
    #                                         |[-] 0000000000 : ajflsdkjkflajd
    #                                         |[-] 0000000000 : sldfkjalsdjflskajdlfkjs
    # flskdjfalksjdlfkjalskdjf : kjasldkfj [+]|
    #                                         |[-] slkdjf : sldfkjalsdjflskajdlfkjslkdj
    # rem ipsum sir dolor ame :    0000000 [+]|
    # alksdjflkasjdlfkjsldkfalfxsdfasdfasd    |
    # alksdjflkasjdlfkjsldkfalfxsdfasdfasd    |
    #                                         |[-] 10,000,000 : sfalksjldfkjaslkdjflkas
    #                                         |    daflksjdlfkajfssfalksjldfkjaslkdjflk
    #                                         |    daflksjdlfkajfssfalksjldfkjaslkdjflk
    # ----------[ income side ]     [ Printing Function ]    [Expense side]------------

# TODO: handle comma separated numbers.
# TODO: add a counter for cash and bank
# TODO: add new field for loans
# TODO: add denominations


# exit loop flag
EXIT_FLAG = False
# char width constants
TYPE_W = 4
AMOUNT_W = 10
REASON_W = 23
COLON_W = 3
SIDE_W = AMOUNT_W+REASON_W+TYPE_W+COLON_W
MULTILINE_W = AMOUNT_W+REASON_W+COLON_W


def write_db(data):
    """Writes data to file"""
    with open('db', 'a', encoding='utf-8') as dbf:
        dbf.write(data)
        dbf.close()


def get_db():
    """Gets data from file"""
    with open('db', 'r', encoding='utf-8') as dbf:
        data = dbf.read().splitlines()
        arr = []
        for line in data:
            arr.append(ast.literal_eval(line))
        dbf.close()
        return arr


def get_details(is_expense: bool):
    """
        Gets Finance details from the user,
        returns a 3 tuple of is_expense,amount,reason
    """
    # Defining strings based on condition
    spent_recieved = 'spent' if is_expense else 'recieved'
    spending_recieving = 'spending' if is_expense else 'recieving'
    # Fetching the amount
    amount = input(
        f'{c.red if is_expense else c.green}{c.bold}Enter amount {spent_recieved}{c.o}: \n')
    # validating null
    if not amount:
        p.o(c.yellow, 'Empty amounts not allowed!')
        time.sleep(1)
        return False
    # validating numeric
    if not amount.isnumeric():
        p.o(c.yellow, 'Amount must be a number!')
        time.sleep(1)
        return False
    # Fetching the reason
    reason = input(
        f'{c.red if is_expense else c.green}{c.bold}Enter reason for {spending_recieving}{c.o}: \n')
    # validating null
    if not reason:
        p.o(c.yellow, 'Empty reasons not allowed!')
        time.sleep(1)
        return False
    # Validating that reason is not more than 10 chars
    if len(amount) > AMOUNT_W:
        p.o(c.yellow, 'Max amount : 10 chars.')
        time.sleep(1)
        return False
    # Returning the values
    return (is_expense, amount, reason)


def check_multiline(string):
    """Checks if the string given should be multiline or not"""
    return len(string) > REASON_W


def print_income(line):
    """Prints data for the income side"""
    # unpack the line tuple
    amount = line[1]
    reason = line[2]
    # check if it's a multiline record
    is_multiline = check_multiline(reason)
    if not is_multiline:
        print_sline(amount, type, reason)
    else:
        first_line = reason[:REASON_W-1]
        the_rest = reason[REASON_W:]
        print(f'The rest : {the_rest}')
        print(f'First line : {first_line}')
        print_sline(amount, type, first_line)
        for chunk in range(0, len(the_rest), MULTILINE_W):
            print(f'\nChunk indx : {chunk}')
            print(f'Chunk : {the_rest[chunk:chunk+MULTILINE_W]}')


def padd_str(text, to_chars, push_r: bool = False, push_l: bool = False):
    """Padds the string given with spaces to a certain char count ( like setw() in cpp )"""
    if len(text) <= to_chars:
        excess = to_chars - len(text)
        if push_r:  # we pad to the left of text
            text = ' ' * excess + text
        elif push_l:  # we pad to the right of text
            text = text + ' ' * excess
        else:  # we dont pad if no direction
            print('No direction specified , returning normal')
        assert len(text) == to_chars
        return text
    if len(text) > to_chars:
        print('Text larger than max chars.')
        return False
    return False


def print_sline(is_expense, amount, reason):
    """Prints a Single line record ( Income/Expense ) to the console."""
    cline = '┃'
    if not is_expense:  # if it is an income [+]
        output = ''
        #  Adding padding to reason and amount
        reason = padd_str(reason, REASON_W, push_r=True)
        amount = padd_str(amount, AMOUNT_W, push_r=True)
        # Splicing the data back together to an outputtable string
        output += reason  #
        output += ' : '
        output += amount
        output += " [+]"
        p.o(c.green, output+cline, compact=True)
    else:  # if it is an expense [-]
        output = ''
        #  Adding padding to reason and amount
        reason = padd_str(reason, REASON_W, push_l=True)
        amount = padd_str(amount, AMOUNT_W, push_l=True)
        # Splicing the data back together to an outputtable string
        output += "[-] "
        output += amount
        output += ' : '
        output += reason
        p.o(c.red, " "*SIDE_W+cline+output, compact=True)


def print_mline(is_expense, amount, reason):
    """Prints a multiline record ( Income/Expense ) to the console."""
    cline = '┃'
    reason_i = reason[:REASON_W]
    reason_e = reason[REASON_W:]
    print_sline(is_expense, amount, reason_i)
    if not is_expense:  # if it is an income [+]
        output = ''
        # loop for each chunk
        for chunk in range(0, len(reason_e), MULTILINE_W):
            #  Adding padding to reason
            reason_t = reason_e[chunk:chunk+MULTILINE_W]
            reason = padd_str(reason_t, MULTILINE_W, push_l=True)
            # Splicing the data back together to an outputtable string
            output += reason
            output += "    "
            p.o(c.green, output+cline, compact=True)
    else:  # if it is an expense [-]
        output = ''
        # loop for each chunk
        for chunk in range(0, len(reason_e), MULTILINE_W):
            reason_t = reason_e[chunk:chunk+MULTILINE_W]
            #  Adding padding to reason
            reason = padd_str(reason_t, MULTILINE_W, push_r=True)
            # Splicing the data back together to an outputtable string
            output += "    "
            output += reason
            p.o(c.red, " "*SIDE_W+cline+output, compact=True)


def print_records():
    """ Prints the details stored in the list """
    system('clear')
    p.o(c.b_black,
        '━━━━━━━━━━━━━━━━━━━━━━━━━━[ Income-Expense Timeline ]━━━━━━━━━━━━━━━━━━━━━━━━')
    money = 0
    data = get_db()
    for record in data:
        if record[0]:
            money -= int(record[1])
        elif not record[0]:
            money += int(record[1])
        if not check_multiline(record[2]):
            print_sline(record[0], record[1], record[2])
        elif check_multiline(record[2]):
            print_mline(record[0], record[1], record[2])
    p.o(c.b_black,
        f'━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Money left : {money} ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


while not EXIT_FLAG:
    # Prompt the main menu
    system('clear')
    p.o(c.blue, '\nIncome - Expense cli tool', bold=True)
    p.o(c.b_purple, ' [V] View spending habbits ', True, bold=True)
    p.o(c.green, ' [I] New Income ', True, bold=True)
    p.o(c.red, ' [E] New Expense ', True, bold=True)
    # p.o(c.b_black,' [D] Debug view ',True,bold=True)
    p.o(c.black, ' [0] Exit program ', True, bold=True)
    # wait for input
    resp = input(f'\n{c.b_black}{c.bold}Choose : {c.o}')

    # Create a new income if response I
    if resp in ['I', 'i']:
        system('clear')
        p.o(c.green, '\nNew Income flow', bold=True)
        store_str = get_details(False)
        if not store_str is False:
            write_db(str(store_str) + '\n')
        time.sleep(0.2)
    # Create a new expense if response E
    elif resp in ['E', 'e']:
        system('clear')
        p.o(c.red, '\nNew Expense flow', bold=True)
        store_str = get_details(True)
        if not store_str is False:
            write_db(str(store_str) + '\n')
        time.sleep(0.2)
    # View debug values if response D
    elif resp in ['D', 'd']:
        store = get_db()
        p.o(c.b_black, f'Store length : {len(store)} item(s).')
        for item in store:
            print(item)
            time.sleep(0.2)
        time.sleep(4)
    # View timeline if response V
    elif resp in ['V', 'v']:
        print_records()
        input()
    # Kill program if choice zero
    elif resp == '0':
        EXIT_FLAG = True
