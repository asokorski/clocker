def count_one():
    print(1)
def count_two():
    print(2)

dict_count = {1: count_one, 2: count_two}

dict_count[2]()

def displayapple():
    return 'apple'

def displaypotat():
    return 'potat'


dict = {'apel': displayapple(), 'pota':displaypotat()}

print(dict['pota'])



    # if mode == 'sprint':
    #     sprint_mode()
    #     continue
    # elif mode == 'slow':
    #     slow_mode()
    #     continue
    # elif mode == 'display':
    #     #display logic here
    #     pass
    # elif mode == 'showlast':
    #     #logic for showing last entry
    #     pass
    # elif mode == 'removelast':
    #     #logic for removing last entry
    #     pass
    # elif mode == 'today':
    #     total_today()
    #     pass
    # else:
    #     print("Incorrect choice...")
    #     continue

# import datetime

# def get_current_time(): #function to get the current date&time stamp without microseconds
#      return datetime.datetime.now().replace(microsecond=0)

# # print(get_current_time())
# # print(type(get_current_time()))



# current_date = get_current_time().date()
# print(current_date)

# current_time = get_current_time().time()
# print(current_time)

# print(type(current_time))


# print(type(current_date))

# day_of_week = get_current_time().strftime('%A')

# print(day_of_week)
# print(type(day_of_week))