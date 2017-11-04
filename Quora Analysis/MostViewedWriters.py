import CLusteringKmeans
writers={"Balaji Viswanathan":1511,"Naman Chakraborty":450,"Krishna Singh":382,"Mohan Dudha":206,"Deekhit Bhattacharya":1642,"Nishank Mishra":1240,"Aadam Ibn Farooq":2290,"Vijay Simha":659,"Aditya Dogra":1166,"Sahil Chatta":657}

def find_clusters():
    c={}
    with open("Cluster_Mapping(5).csv","r") as f:
        for row in f:
            row=row.split(",")
            for j in writers:
                if writers[j]==int(row[1]):
                    if row[0] not in c:
                        c.setdefault(row[0],[])
                    c[row[0]].append(writers[j])
                else:
                    print("!")
    print(c)

find_clusters()