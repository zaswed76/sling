


def _fsum(d1, d2, name):
    if not d1: d1 = (0, 0)
    if not d2: d2 = (0, 0)
    for _d1, _d2 in zip(d1.values(), d2.values()):
        return {name: [p1 + p2 for p1, p2 in zip(_d1, _d2)]}

a = dict(aaa=[4, 4])
b = dict()

print(_fsum(a, b, "aaa"))
