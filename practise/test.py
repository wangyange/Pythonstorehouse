list_1 =[1,2,3,4]

def double_func(list):
    return list*2

# list_2 = map(lambda list:list*2,list_1)
# print list_2

list_3 =reduce(lambda x,y:x+y,list_1)
print list_3


