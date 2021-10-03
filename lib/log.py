
# helper class for ASCII color escape codes
class color:
    OK = '\033[92m'
    INFO = '\033[94m'
    WARN = '\033[93m'
    FAIL = '\033[91m'
    EOF = '\033[0m'
    BOLD = '\033[1m'


# log a message to the console with an optional level i.e INFO or ERROR and optional context
def log(log_message: str, context: str = None, log_level=color.INFO):
    msg: str = ""
    # append a log level
    if log_level == color.OK:
        msg += f'{color.OK}[OK]'
    elif log_level == color.INFO:
        msg += f'{color.INFO}[INFO]'
    elif log_level == color.WARN:
        msg += f'{color.WARN}[WARN]'
    elif log_level == color.FAIL:
        msg += f'{color.FAIL}[FAIL]'
    else:
        # set INFO as the default
        msg += f'{color.INFO}[INFO]'
    # set the default context
    if context is None:
        context = "[+]"
    # add BOLD tags to WARN and FAIL log types
    if log_level == color.WARN:
        msg + f' {color.WARN}{color.BOLD}' + context + f'{color.EOF} ' + log_message + f'{color.EOF}{color.EOF}'
    elif log_level == color.FAIL:
        msg + f' {color.FAIL}{color.BOLD}' + context + f'{color.EOF} ' + log_message + f'{color.EOF}{color.EOF}'
    else:
        msg + f' {log_level} ' + context + ' ' + log_message + f'{color.EOF}'
    # output the crafted log
    print(msg)