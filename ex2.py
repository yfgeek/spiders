# coding = utf-8
import sys

if __name__ == "__main__":
    arr = []
    niu1,niu2 =0,0
    num = int(sys.stdin.readline().strip())
    line = sys.stdin.readline().strip()
    arr = list(map(int, line.split()))
    a = sum(arr) / 2
    temp = 0
    m = [[0 for x in range(a + 1)] for y in range(len(arr))]
    for i in range(len(arr)):
        m[i][0] = 0
    for j in range(a + 1):
        if j >= arr[0]:
            m[0][j] = arr[0]
        else:
            m[0][j] = 0

    for j in range(1, a + 1):
        for i in range(1, len(arr)):
            if j - arr[i] >= 0:
                m[i][j] = max(m[i - 1][j], m[i - 1][j - arr[i]] + arr[i])
            else:
                m[i][j] = m[i - 1][j]
    p1 = len(arr) - 1
    p2 = a

    while p1 >= 0:
        if (m[p1][p2] != m[p1 - 1][p2] and p1 - 1 >= 0) or (p1 == 0 and m[p1][p2] == arr[p1]):
            niu1 +=arr[p1]
            p2 = p2 - arr[p1]
            p1 = p1 - 1
        elif m[p1][p2] == m[p1 - 1][p2]:
            niu2 += arr[p1]
            p1 = p1 - 1
    print str(niu1) + " " + str(niu2)
