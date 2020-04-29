import csv
import pprint
csv1251Test = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\1251Test.csv"
csvutfTest = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\utfTest.csv"
xlsxTest = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\1251Test.xlsx"
# path2=r"D:\user\projects\sling\lingvo\data\slovar1\testDictEx.txt"



def changeSep(path, path2=None, sourcedelimiter=';', targetdelimiter=';'):
    path2 = path if path2 is None else path2
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=sourcedelimiter)
        data = list(spamreader)
        pprint.pprint(data)

    # with open(path2, "w", newline='') as csv_file:
    #     writer = csv.writer(csv_file, delimiter=targetdelimiter)
    #     for line in data:
    #         writer.writerow(line)

if __name__ == '__main__':
    # changeSep(csv1251Test)
    changeSep(csvutfTest)