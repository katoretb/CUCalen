# def time_range(start, end):
#     temp = []
#     sl = start.split(":")
#     el = end.split(":")
#     for i in range(int(sl[0]), int(el[0])+1):
#         for j in range(2):
#             temp.append(f'{i}-{j*30}')
#             temp.append(f'{i}-{j*30}')

#     temp = temp[3:] if sl[1] != "00" else temp[1:]
#     temp = temp[:-3] if el[1] == "00" else temp[:-1]
#     return temp

# temp = []
# for j in range(9, 16+1):
#     for k in range(2):
#         temp.append(f'{j}-{ k*30}')
#         temp.append(f'{j}-{k*30}')
# print(temp)
# print(time_range("12:00:00", "13:00:00"), "\n")
# print(time_range("13:00:00", "16:00:00"), "\n")


# print(time_range("9:00:00", "10:00:00"), "\n")
# print(time_range("9:00:00", "10:30:00"), "\n")
# print(time_range("9:30:00", "10:00:00"), "\n")
# print(time_range("9:30:00", "10:30:00"), "\n")


for i in []:
    print(i)