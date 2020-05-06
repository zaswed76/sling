from collections import UserDict


class DCT(UserDict):
    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.__data = {}
        # self.__data.update(*kwargs)


    def update(self, __m):
        self.__data.update(__m)
        print(self.__data)


    def __getitem__(self, key):
        __line = " ".join(key.split(" ")[:4])
        for k in self.__data:
            print(k, "777")
            if k.find(__line) > -1:
                return self.__data.__getitem__(k)
        else:
            return None



    def __repr__(self):
        return str(self.__data)

key = "Seems strange, because I use same closeEvent"
ds = {"Seems strange, because I use": "res"}
d = DCT()
d.update(ds)
print(d.get(key), "res")

# s = "Seems strange, because I use"
# line = "Seems strange, because I"
# print(s.find(line))
