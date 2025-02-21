from common.logger import logger
import threading
import sys
import datetime
import json
import random
import jwt
import operator
import _thread


def dict_pretty_format(value):
    try:
        return json.dumps(value, indent=4, default=str)
    except Exception as e:
        logger.debug(f"dict pretty format error:{e}")
        return value


def get_date(date_offset=0, date_format='%Y-%m-%d %H:%M:%S'):
    return (datetime.datetime.today() + datetime.timedelta(days=date_offset)).strftime(date_format)


def random_char(length):
    list_temp = []
    for i in range(length):
        x = random.randint(1, 2)
        if x == 1:
            y = str(random.randint(0, 9))
        else:
            y = chr(random.randint(97, 122))
        list_temp.append(y)
    return ''.join(list_temp)


def decode_jwt_token(token, algorithms):
    contnt = jwt.decode(token, algorithms=algorithms, options={"verify_signature": False})
    return contnt


def quit_function(fn_name):
    # print to stderr, unbuffered in Python 2.
    print('{0} took too long'.format(fn_name), file=sys.stderr)
    sys.stderr.flush()  # Python 3 stderr is likely buffered.
    _thread.interrupt_main()


def get_operator(operator_string):
    cond_info = {'>': operator.gt, '<': operator.lt, '==': operator.eq, '>=': operator.ge,
                 '<=': operator.le, '!=': operator.ne, '=': operator.eq}
    return cond_info[operator_string]


def time_out_decorator(fn):
    def decorator(self, *args, **kwargs):
        timer = threading.Timer(self.state, quit_function, args=[fn.__name__])
        timer.start()
        try:
            result = fn(self, *args, **kwargs)
        finally:
            timer.cancel()
        return result
    return decorator
