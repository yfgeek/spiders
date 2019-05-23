import sys

def convert_arr(value):
    return list(map(int, str(value)))


def verify(num):
    arr = convert_arr(num)
    test = [0] * 10
    for i in arr:
        if test[int(i)] > 0:
            return False
        test[int(i)] += 1
    return True


def search(start, end):
    num = 0
    for i in range(start, end+1):
        if verify(i):
            num += 1
    return num


for line in sys.stdin:
    a = line.split()
    print(search(int(a[0]), int(a[1])))
