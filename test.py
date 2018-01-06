from collections import defaultdict


def numberOfArithmeticSlices(A):
    result = 0
    dp = [{} for i in xrange(len(A))]
    for i in xrange(1, len(A)):
        for j in range(i):
            diff = A[i] - A[j]
            s = dp[j].get(diff, 0) + 1
            dp[i][diff] = dp[i].get(diff, 0) + s
            result += (s - 1)
    return result