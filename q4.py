import time

start_time = time.time()

def split_dig(num):
    s = str(num)
    d0 = int(s[0])
    d1 = int(s[1])
    d2 = int(s[2])
    d3 = int(s[3])
    d4 = int(s[4])
    d5 = int(s[5])
    return (d0, d1, d2, d3, d4, d5)


def atleast2match(x):
    d0 = x[0]
    d1 = x[1]
    d2 = x[2]
    d3 = x[3]
    d4 = x[4]
    d5 = x[5]
    if (d0==d1 or d1==d2 or d2==d3 or d3==d4 or d4==d5):
        return True
    else:
        return False

def exactly2match(x):
    d0 = x[0]
    d1 = x[1]
    d2 = x[2]
    d3 = x[3]
    d4 = x[4]
    d5 = x[5]
    if (d0==d1 and d1!=d2):
        return True
    elif d0!=d1 and d1==d2 and d2!=d3:
        return True
    elif d1!=d2 and d2==d3 and d3!=d4:
        return True
    elif d2!=d3 and d3==d4 and d4!=d5:
        return True
    elif d3!=d4 and d4==d5:
        return True
    else:
        return False



def isascending(x): 
    d0 = x[0]
    d1 = x[1]
    d2 = x[2]
    d3 = x[3]
    d4 = x[4]
    d5 = x[5]
    if (d5 >= d4 >= d3 >= d2 >= d1 >= d0):
        return True
    else:
        return False


fit_criteria = []

# 235741
# 706948
# range(235741, 706948)

testcases = [987654, 112233, 123444, 111122, 555678, 555677]

for num in range(235741, 706948):
    split_num = split_dig(num)
    if isascending(split_num) == True:
        if atleast2match(split_num) == True:
            if exactly2match(split_num) == True:
                fit_criteria.append(num)
                #print(num, " fits criteria")
            else:
                pass
                #print(num, " doesn't fit criteria")
        else:
            pass
            #print(num, " doesn't fit criteria")
    else:
        pass
        #print(num, " doesn't fit criteria")

print(len(fit_criteria))


print((time.time() - start_time), " sec")
