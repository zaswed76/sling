
lst = ['a', 'b']
d = dict(a=1, b=2, c=3)

td = {k:v for k, v in d.items() if k in lst}
print(td)


