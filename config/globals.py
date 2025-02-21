
# hold runtime args
global_dict = {}

def set(key, value):
    global_dict[key] = value

def get(key):
    return global_dict.get(key)

#Used for argument ID
argument_id = []