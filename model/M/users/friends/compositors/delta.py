import random


def delta(admin, m, n, supercycle = False):
    xQ        = admin.orm.api.users.count("unfriendQ")
    load      = 400
    efficency = load / xQ
    rate      = (m + n) / 2
    if not supercycle:
        rate /= efficency
    else:
        efficency =  1 - efficency
        rate     *= (1 + efficency)
    distance  = abs(m - rate)
    m, n      = int(max(5, rate - distance)), int(rate + distance)
    n         = random.randint(m, n)
    return n
