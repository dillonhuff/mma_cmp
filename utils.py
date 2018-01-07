from sets import Set

def represents_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def is_month(s):
    months = Set(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])

    return s in months

def month_to_num(s):
    month_nums = {'Jan' : 0,
                  'Feb' : 1,
                  'Mar' : 2,
                  'Apr' : 3,
                  'May' : 4,
                  'Jun' : 5,
                  'Jul' : 6,
                  'Aug' : 7,
                  'Sep' : 8,
                  'Oct' : 9,
                  'Nov' : 10,
                  'Dec' : 11}

    return month_nums[s]
    
def num_to_month(n):
    nums_month = {1 : 'Jan',
                  2 : 'Feb',
                  3 : 'Mar',
                  4 : 'Apr',
                  5 : 'May',
                  6 : 'Jun',
                  7 : 'Jul',
                  8 : 'Aug',
                  9 : 'Sep',
                  10 : 'Oct',
                  11 : 'Nov',
                  12 : 'Dec'}

    return nums_month[n]
