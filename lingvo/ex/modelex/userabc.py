from collections.abc import MutableMapping as __MutableMapping
from collections.abc import MutableSequence as __MutableSequence
from collections import UserList

# class UserDict(__MutableMapping):
#     def __init__(self, _dict=None):
#         self.__data = {}
#         if isinstance(_dict, dict):
#             self.__data.update(_dict)
#
#     def __setitem__(self, key, value):
#         self.__data[key] = value
#
#     def __getitem__(self, key):
#         return self.__data[key]
#
#     def __len__(self):
#         return len(self.__data)
#
#     def __delitem__(self, key):
#         del self.__data[key]
#
#     def __iter__(self):
#         return iter(self.__data)
#
#     def __repr__(self):
#         return "{}:{}".format(self.__class__.__name__, self.__data)
#
# class UserList(__MutableSequence):
#     def __init__(self, _list=None):
#         self.__data = []
#         if isinstance(_list, list):
#             self.__data.extend(_list)
#
#     def __setitem__(self, i, value):
#         self.__data[i] = value
#
#     def __getitem__(self, i):
#         return self.__data[i]
#
#     def __len__(self):
#         return len(self.__data)
#
#     def __delitem__(self, key):
#         del self.__data[key]
#
#     def __iter__(self):
#         return iter(self.__data)
#
#     def __repr__(self):
#         return "{}:{}".format(self.__class__.__name__, self.__data)
#
#     def insert(self, index, object):
#         self.__data.insert(index, object)


class Side(UserList):
    def __init__(self):
        super().__init__()

    @property
    def sections(self):
        return self







if __name__ == '__main__':
    ud = Side()
    ud.append(1)

    print(ud.sections)