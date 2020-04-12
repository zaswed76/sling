import csv

path=r"D:\user\projects\sling\lingvo\data\slovar1\testDict - Лист1.csv"
path2=r"D:\user\projects\sling\lingvo\data\slovar1\testDictEx.txt"



def changeSep(path, path2=None, sourcedelimiter=',', targetdelimiter=';'):
    path2 = path if path2 is None else path2
    with open(path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=sourcedelimiter)
        data = list(spamreader)
    with open(path2, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=targetdelimiter)
        for line in data:
            writer.writerow(line)

if __name__ == '__main__':
    changeSep(path, path2)