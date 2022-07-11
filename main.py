from os import system
import time

from colors import C,P
c = C()
p = P()

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
exitflag = False
# char width constants 
type_w = 4
amount_w = 10
reason_w = 23
colon_w = 3
side_w = amount_w+reason_w+type_w+colon_w
multiline_w = amount_w+reason_w+colon_w


def write_db(data):
    storef = open('db','a')
    storef.write(data)
    storef.close()


def get_db():
    dataf = open('db','r')
    data = dataf.read().splitlines()
    arr = []
    for line in data :
        arr.append(eval(line))
    dataf.close()
    return arr


def get_details(is_expense: bool):
    """ 
        Gets Finance details from the user,
        returns a 3 tuple of is_expense,amount,reason
    """
    # Defining strings based on condition
    sr = 'spent' if is_expense else  'recieved'
    rs = 'spending' if is_expense else  'recieving'
    # Fetching the amount 
    amount = input(f'{c.red if is_expense else c.green}{c.bold}Enter amount {sr}{c.o}: \n')
    # validating null
    if not amount:
        p.o(c.yellow,'Empty amounts not allowed!')
        time.sleep(1)
        return False
    # validating numeric
    if not amount.isnumeric():
        p.o(c.yellow,'Amount must be a number!')
        time.sleep(1)
        return False
    # Fetching the reason 
    reason = input(f'{c.red if is_expense else c.green}{c.bold}Enter reason for {rs}{c.o}: \n')
    # validating null
    if not reason:
        p.o(c.yellow,'Empty reasons not allowed!')
        time.sleep(1)
        return False
    # Validating that reason is not more than 10 chars
    if len(amount) > amount_w:
        p.o(c.yellow,'Max amount : 10 chars.')
        time.sleep(1)
        return False
    # Returning the values
    return (is_expense,amount,reason)


def check_multiline(reason): return len(reason) > reason_w


def print_income(line):
    # unpack the line tuple 
    is_expense = line[0]
    amount = line[1]
    reason = line[2]
    # check if it's a multiline record 
    is_multiline = check_multiline(reason)
    if not is_multiline :
        print_sline(amount,type,reason)
    else :
        first_line = reason[:reason_w-1]
        the_rest = reason[reason_w:]
        print(f'The rest : {the_rest}')
        print(f'First line : {first_line}')
        print_sline(amount,type,first_line)
        for chunk in range(0, len(the_rest), multiline_w):
            print(f'\nChunk indx : {chunk}')
            print(f'Chunk : {the_rest[chunk:chunk+multiline_w]}')


def padd_str(text,to_chars,push_r:bool = False,push_l:bool = False):
    if len(text) < to_chars:
        excess = to_chars - len(text)
        if push_r :  # we pad to the left of text 
            text = ' ' * excess + text
        elif push_l :  # we pad to the right of text
            text = text + ' ' * excess
        else :  # we dont pad if no direction
            print('No direction specified , returning normal')
        assert len(text) == to_chars
        return text 
    elif len(text) == to_chars:
        return text
    else:
        print('Text larger than max chars.')
        return False


def print_sline(is_expense,amount,reason):
    """Prints a Single line record ( Income/Expense ) to the console."""
    cline = '┃'
    if not is_expense:  # if it is an income [+]
        output = ''
        #  Adding padding to reason and amount
        reason = padd_str(reason,reason_w,push_r=True)  
        amount = padd_str(amount,amount_w,push_r=True)  
        # Splicing the data back together to an outputtable string 
        output += reason  #
        output += ' : '
        output +=  amount 
        output += " [+]"
        p.o(c.green,output+cline,compact=True)
    else :  # if it is an expense [-]
        output = ''
        #  Adding padding to reason and amount
        reason = padd_str(reason,reason_w,push_l=True)  
        amount = padd_str(amount,amount_w,push_l=True)  
        # Splicing the data back together to an outputtable string 
        output += "[-] "
        output +=  amount 
        output += ' : '
        output += reason 
        p.o(c.red," "*side_w+cline+output,compact=True)


def print_mline(is_expense,amount,reason):
    """Prints a multiline record ( Income/Expense ) to the console."""
    cline = '┃'
    reason_i= reason[:reason_w]
    reason_e = reason[reason_w:]
    print_sline(is_expense,amount,reason_i)
    if not is_expense:  # if it is an income [+]
        output = ''
        # loop for each chunk 
        for chunk in range(0, len(reason_e), multiline_w):
            #  Adding padding to reason 
            reason_t = reason_e[chunk:chunk+multiline_w]
            reason = padd_str(reason_t,multiline_w,push_l=True)
            # Splicing the data back together to an outputtable string 
            output += reason #
            output += "    "
            p.o(c.green,output+cline,compact=True)
    else :  # if it is an expense [-]
        output = ''
        # loop for each chunk 
        for chunk in range(0, len(reason_e), multiline_w):
            reason_t = reason_e[chunk:chunk+multiline_w]
            #  Adding padding to reason 
            reason = padd_str(reason_t,multiline_w,push_r=True)
            # Splicing the data back together to an outputtable string 
            output += "    "
            output += reason #
            p.o(c.red," "*side_w+cline+output,compact=True)


def print_records():
    """ Prints the details stored in the list """
    system('clear')
    p.o(c.b_black,
        f'━━━━━━━━━━━━━━━━━━━━━━━━━━[ Income-Expense Timeline ]━━━━━━━━━━━━━━━━━━━━━━━━')
    money = 0
    store = get_db()
    for item in store:
        if item[0]:
            money -= int(item[1])
        elif not item[0]:
            money += int(item[1])
        if not check_multiline(item[2]):
            print_sline(item[0],item[1],item[2])
        elif check_multiline(item[2]):
            print_mline(item[0],item[1],item[2])
    p.o(c.b_black,
        f'━━━━━━━━━━━━━━━━━━━━━━━━━━━[ Money left : {money} ]━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


while not exitflag :
    # Prompt the main menu
    system('clear')
    p.o(c.blue,'\nIncome - Expense cli tool',bold=True)
    p.o(c.b_purple,' [V] View spending habbits ',True,bold=True)
    p.o(c.green,' [I] New Income ',True,bold=True)
    p.o(c.red,' [E] New Expense ',True,bold=True)
    # p.o(c.b_black,' [D] Debug view ',True,bold=True)
    p.o(c.black,' [0] Exit program ',True,bold=True)
    # wait for input
    resp = input(f'\n{c.b_black}{c.bold}Choose : {c.o}')
    
    # Create a new income if response I
    if resp in ['I','i']:
        system('clear')
        p.o(c.green,'\nNew Income flow',bold=True)
        store_str = get_details(False)
        if not store_str is False:
            write_db(str(store_str) + '\n')
        time.sleep(0.2)
    # Create a new expense if response E
    elif resp in ['E','e']:
        system('clear')
        p.o(c.red,'\nNew Expense flow',bold=True)
        store_str = get_details(True)
        if not store_str is False:
            write_db(str(store_str) + '\n')
        time.sleep(0.2)
    # View debug values if response D
    elif resp in ['D','d']:
        store = get_db()
        p.o(c.b_black,f'Store length : {len(store)} item(s).')
        for item in store:
            print(item)
            time.sleep(0.2)
        time.sleep(4)
    # View timeline if response V
    elif resp in ['V','v']:
        print_records()
        input()
    # Kill program if choice zero
    elif resp == '0':
        exitflag = True
