import csv



def create():
    useravg = {}
    with open('user_compound.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
                c = 0
                if row[0] not in useravg.keys():
                    useravg.setdefault(row[0], [])
                    useravg[row[0]].append(float(row[1]))
                    c=1
                if c==0:
                    useravg[row[0]].append(float(row[1]))

    print(useravg)
    for user in useravg:
            averageN = float(sum(useravg[user])/len(useravg[user]))
            with open('user_compound_average.csv', 'a', newline= '', encoding='UTF-8') as f:
                fieldnames = ['userId', 'Average Compound']
                writer = csv.DictWriter(f, fieldnames= fieldnames)
                writer.writerow({'userId':user,'Average Compound': averageN})


def plot():
    pos = 0.0
    neg = 0.0
    with open('user_compound_average.csv', 'r', encoding='UTF-8') as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            if float(row[1]) > 0:
                pos = pos + 1
            else:
                neg = neg + 1
    import matplotlib.pyplot as plt

    plt.bar([-1, +1], [neg, pos])
    plt.show()

create()
plot()