import sys

def verify(num):
    arr = num.split()
    test = [0,1,2,3,4,5,6,7,8,9]
    for i in arr:
        if test[int(i)]>0:
            return False
        test[int(i)] += 1
    return True

def search(start, end):
    num = 0
    for i in range(start, end):
        if verify(i):
            num += 1
    return num

for line in sys.stdin:
    a = line.split()
    print(search(int(a[0]), int(a[1])))
