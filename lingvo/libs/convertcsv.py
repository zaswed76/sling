import csv

path=r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\data\seasons\seasons.csv"
path2=r"E:\1_SYNS_ORIGINAL\0SYNC\python_projects\sling\lingvo2\data\seasons\seasons.txt"



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