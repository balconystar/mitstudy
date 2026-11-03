


def fastfib(n,memo):
    
    if not n in memo:
        memo[n] = fastfib(n-1,memo) + fastfib(n-2,memo)
    return memo[n]           



def fib(n):
    memo = { 0:0 , 1:1 , 2:1}
    return fastfib(n,memo)


for i in range(1,31):
    print(fib(i))


