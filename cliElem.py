# Simple CLI Elements
cols = " "*40

# Colour Codes
class colors:
    reset = '\033[00m'
    bold = '\033[01m'
    disable = '\033[02m'
    underline = '\033[04m'
    reverse = '\033[07m'
    strikethrough = '\033[09m'
    invisible = '\033[08m'
    blink = '\033[05m'
    clear = '\033[2J\033[H'

    class fg:
        black = '\033[30m'
        red = '\033[31m'
        green = '\033[32m'
        orange = '\033[33m'
        blue = '\033[34m'
        purple = '\033[35m'
        cyan = '\033[36m'
        lightgrey = '\033[37m'
        darkgrey = '\033[90m'
        lightred = '\033[91m'
        lightgreen = '\033[92m'
        yellow = '\033[93m'
        lightblue = '\033[94m'
        pink = '\033[95m'
        lightcyan = '\033[96m'

    class bg:
        black = '\033[40m'
        red = '\033[41m'
        green = '\033[42m'
        orange = '\033[43m'
        blue = '\033[44m'
        purple = '\033[45m'
        cyan = '\033[46m'
        lightgrey = '\033[47m'


def printBanner(*args, sep=' '):
    pStr = sep.join(args)
    print(cols, f"+-{'-'*len(pStr)}-+")
    print(cols, f"| {colors.blink}{colors.bold}{pStr}{colors.reset} |")
    print(cols, f"+-{'-'*len(pStr)}-+")

def log(kind='I', *args):
    kinds = {
            'I': ('INFO', colors.bold),
            'E': ('ERROR', colors.fg.red),
            'S': ('SUCCESS', colors.fg.green),
            'W': ('WARNING', colors.fg.yellow)

    }
    k, c = kinds[kind]
    print(cols, f"{c}{k}:", *args, colors.reset)

def inputLOV(prompt, options):
    print("\n", prompt)
    print(genTable([((i+1), options[i]) for i in range(len(options))], False))
    while True:
        try:
            optId = int(input("Enter an option: "))
            return options[optId-1]
        except ValueError:
            log('W', "Invalid input typed. Please try again!")
        except IndexError:
            log('W', "Invalid option selected. Please try again!")


def genTable(data, header=True, colp=True):
    col_widths = [max(len(str(item)) for item in col) for col in zip(*data)]
    
    def format_row(row):
        return "| " + " | ".join(f"{str(item).ljust(width)}" for item, width in zip(row, col_widths)) + " |"
    
    border = "+-" + "-+-".join("-" * width for width in col_widths) + "-+"
    
    table = [border]
    table.append(format_row(data[0]))
    if header:
        table.append(border.replace("-", "="))
    for row in data[1:]:
        table.append(format_row(row))
    table.append(border)
    
    return "\n".join([cols+row if colp else row for row in table])

