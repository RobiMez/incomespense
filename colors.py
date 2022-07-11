
class C:
    black = '\033[30m'
    red = '\033[31m'
    green = '\033[32m'
    yellow = '\033[33m'
    orange = '\033[34m'
    purple = '\033[35m'
    blue = '\033[36m'
    white = '\033[37m'
    b_black = '\033[90m'
    b_red = '\033[91m'
    b_green = '\033[92m'
    b_yellow = '\033[93m'
    b_orange = '\033[94m'
    b_purple = '\033[95m'
    b_blue = '\033[96m'
    b_white = '\033[97m'
    bold = '\033[1m'
    faint = '\033[2m'
    italic = '\033[3m'
    underline = '\033[4m'
    o = '\033[0m'


class P:
    @staticmethod
    def o(color=C.b_black, data=' O~O - Default print',
          compact=False, bold=False, faint=False):
        data = str(data)
        if bold:
            data = C.bold+color+data+C.o
        elif faint:
            data = C.faint+color+data+C.o
        else:
            data = color+data+C.o
        if not compact:
            data = '\n'+data+'\n'
        print(f'{data}')


