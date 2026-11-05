import math, mpmath

def f_bad(x):
    return math.sqrt(x+1) - math.sqrt(x)

def f_good(x):
    return 1/(math.sqrt(x+1) + math.sqrt(x))

def f_exact(x):
    x = mpmath.mpf(x)
    return 1/(mpmath.sqrt(x+1) + mpmath.sqrt(x))

def experiment(f_bad, f_good, xs, f_exact):
    print(f"{'x':>10} | {'bad':>14} | {'good':>14} | "
          f"{'err_bad':>10} | {'err_good':>10}")
    print("-" * 78)
    for x in xs:
        b  = f_bad(x)
        g  = f_good(x)
        ex = f_exact(x)                    # независимый эталон
        eb = abs(b - ex) / abs(ex) if ex else float('inf')
        eg = abs(g - ex) / abs(ex) if ex else float('inf')

        eb = mpmath.nstr(eb, 5)
        eg = mpmath.nstr(eg, 5)
        print(f"{x:>10.0e} | {b:>14.8e} | {g:>14.8e} | "
              f"{eb:>10} | {eg:>10}")

mpmath.mp.dps = 100
xs = [1e-14, 1e-12, 1e-10, 1e-6, 5, 100, 1000, 1e6, 1e10, 1e12, 1e14]
experiment(f_bad, f_good, xs, f_exact)

"""
вывод
При небольших значениях x оба способа работают практически одинаково,
однако с увеличением x погрешность первого способа начинает быстро расти.

"""