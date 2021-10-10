
def is_number(user_input):
    is_number = user_input.isnumeric()
    if is_number == False:
        return False
    else:
        return True


def is_in_range(user_input, list):
    index = int(user_input) - 1
    upper_range = len(list)
    if (0 <= index < upper_range):
        return True
    else: 
        return False


def is_not_empty_list(list):
    if (len(list) == 0):
        return False
    else:
        return True