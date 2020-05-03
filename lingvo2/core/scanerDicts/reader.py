import csv
import pprint


def csvRead(path,  sourcedelimiter=';'):
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=sourcedelimiter)
        return list(spamreader)

def formatter(data):
    cutData = [line[:5] for line in data]
    # pprint.pprint(cutData)
    # print("----------------")
    fdata = list(filter(emptyFilter, cutData))
    # pprint.pprint(fdata)

def emptyFilter(line):
    f1 = any(line)
    return all((f1,))


if __name__ == '__main__':
    import pprint
    csv1251Test2 = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\1251Test2.csv"
    csvutfTest = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\utfTest.csv"
    xlsxTest = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\datatest\1251Test.xlsx"

    # csv1 = r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\libs\season.csv"
    csvread = csvRead(csv1251Test2)
    formatter(csvread)