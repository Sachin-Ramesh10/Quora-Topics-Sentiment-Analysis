import csv
from VaderSentimentAnalysis import *



def write_data(a, b, c,d,f,e):
    with open('SentimentQuora.csv', 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['Question', 'User', 'Answer','Negative Emotion Quotient','Neutral Emotion Qoutient','Positive Emotion Qoutient']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Question': a, 'User': b, 'Answer': c,'Negative Emotion Quotient':d,'Neutral Emotion Qoutient':f,'Positive Emotion Qoutient':e})

def write_q(a, b):
    with open('Questions-Quora.csv', 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['Question', 'QuestionId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Question': a, 'QuestionId': b})

def write_u(a, b):
    with open('Profiles-Quora.csv', 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['User', 'UserId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'User': a, 'UserId': b})

def write_a(a, b):
    with open('Answers-Quora.csv', 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['Answer', 'AnswerId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'Answer': a, 'AnswerId': b})

def write_map1(a,b):
    with open("Questions-Answers-Map.csv", 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['QuestionId', 'AnswerId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'QuestionId': a, 'AnswerId': b})

def write_map2(a,b):
    with open("Questions-Profiles-Map.csv", 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['QuestionId', 'ProfileId']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'QuestionId': a, 'ProfileId': b})

def write_map3(a,b,c,d):
    with open("Users-Sentiment.csv", 'a', newline='', encoding= 'utf-8') as csvfile:
        fieldnames = ['UserId', 'Negative Emotion Quotient','Neutral Emotion Qoutient','Positive Emotion Qoutient']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({'UserId':a, 'Negative Emotion Quotient':b,'Neutral Emotion Qoutient':c,'Positive Emotion Qoutient':d})

def QuoraFiles():

    qcount=1
    ucount=1
    acount=1
    users={}
    questions={}
    answers={}
    with open('Quora.csv', 'r', encoding= 'UTF-8') as f:
        reader = csv.reader(f, delimiter= ',')

        for row in reader:
            if (row[0] == 'Question'):
                continue
            if row[0] not in questions:
                print(row[0])
                questions[row[0]] = qcount
                write_q(row[0], qcount)
                qcount += 1
            if row[1] not in users:
                users[row[1]] = ucount
                write_u(row[1], ucount)
                ucount += 1
            if row[2] not in answers:
                answers[row[2]] = acount
                write_a(row[2], acount)
                acount += 1
            print(row[2])
            print(row[1])
            print(row[0])
            val,val1,val2,val3=analyse(row[2])
            write_data(questions[row[0]], users[row[1]], answers[row[2]], val,val1,val2)
            write_map1(questions[row[0]],answers[row[2]])
            write_map2(questions[row[0]],users[row[1]])
            write_map3(users[row[1]],val,val1,val2)


def usersAverage():
    userNeg={}
    userNeu={}
    userPos={}
    with open("Users-Sentiment.csv","r") as f:
        reader = csv.reader(f, delimiter=',')
        for row in reader:
            c=0
            if row[0] not in userNeg:
                userNeg.setdefault(row[0], [])
                userNeg[row[0]].append(float(row[1]))
                c=1
            if row[0] not in userNeu:
                userNeu.setdefault(row[0], [])
                userNeu[row[0]].append(float(row[2]))
                c=1
            if row[0] not in userPos:
                userPos.setdefault(row[0], [])
                userPos[row[0]].append(float(row[3]))
                c=1
            if c==0:
                userNeg[row[0]].append(float(row[1]))
                userNeu[row[0]].append(float(row[2]))
                userPos[row[0]].append(float(row[3]))
    print(userNeg)
    print(userNeu)
    print(userPos)

    userIds = userNeg.keys()

    for user in userIds:
        averageN = float(sum(userNeg[user])/len(userNeg[user]))
        averageNeu = float(sum(userNeu[user])/len(userNeu[user]))
        averageP = float(sum(userPos[user])/len(userPos[user]))
        with open('AverageValues.csv', 'a', newline= '') as f:
            fieldnames = ['userId', 'Average Negative', 'Average Neutral', 'Average Postive']
            writer = csv.DictWriter(f, fieldnames= fieldnames)
            writer.writerow({'userId':user,'Average Negative': averageN,'Average Neutral': averageNeu,'Average Postive':averageP})



QuoraFiles()
usersAverage()