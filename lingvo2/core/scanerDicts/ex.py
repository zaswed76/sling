a = ['', '', '', '', '']
b = ['', '', '', '', ' ']

print(any(b))

def myfilter(lst_line):
    res = []
    loc_res = []
    for s in lst_line:
        if s and not s.isspace():
            loc_res.append(s)
