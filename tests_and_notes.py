



#No matter if the time is out and the bell has rang or user interrupted it, 
# it doesn't make any log until user clocks out in both cases the question "do you want to clock out" will be prompted. 
# If possible in some bright red color (not sure if this is possible)




# backup:

# #sprint and slow mode kept separately for different features
# def sprint_mode():
#     while True:
#         print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>SPRINT MODE<<<{Style.RESET_ALL}")
#         print(last_three_logs())
#         decision = input("""
#         i:          Clocking in
#         o:          Clocking out
#         back:       Back to the previous menu
# Type the shortcut for the event: """).lower()
#         if decision == 'i':
#             comment = input("Comment: ")
#             save_log('in', comment)
#         elif decision == 'o':
#             comment = input("Comment: ")
#             save_log('out', comment)
#         elif decision == 'back':
#             print('\nReturning to main menu')
#             break
#         else:
#             print('Invalid option\n')


# def slow_mode():
#     while True:
#         print(f"\n{Style.BRIGHT}{Fore.YELLOW}>>>SLOW MODE<<<{Style.RESET_ALL}")
#         print(last_three_logs())
#         decision = input("""
#         i:          Clocking in
#         o:          Clocking out
#         back:       Back to the previous menu
# Type the shortcut for the event: """).lower()
#         if decision == 'i':
#             comment = input("Comment: ")
#             save_log('in', comment)
#         elif decision == 'o':
#             comment = input("Comment: ")
#             save_log('out', comment)
#         elif decision == 'back':
#             print('\nReturning to main menu')
#             break
#         else:
#             print('Invalid option\n')