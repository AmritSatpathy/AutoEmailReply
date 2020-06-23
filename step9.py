import pandas as pd

def decode(x,y):
    if x == "Surely, noted.Feel free to connect with us in the future if you would like toexplore our offerings.,Rekha JainFounder+91 9930459453" and y == 0:
        return True
    elif x == "Surely, noted.Feel free to connect with us in the future if you would like toexplore our offerings.,Rekha JainFounder+91 9930459453" and y == 1:
        return False
    elif x != "Surely, noted.Feel free to connect with us in the future if you would like toexplore our offerings.,Rekha JainFounder+91 9930459453" and y == 1:
        return True
    elif x != "Surely, noted.Feel free to connect with us in the future if you would like toexplore our offerings.,Rekha JainFounder+91 9930459453" and y == 0:
        return False
def load():
    loaded = pd.read_csv("finedresult.csv", engine='python')
    check = pd.read_csv("cleanedsent.csv")
    mergedStuff = pd.merge(loaded, check, on=['Subject'], how='inner')
    for i in mergedStuff.index:
         if not (decode(mergedStuff['text/plain_y'][i], mergedStuff['Label'][i])):
             var = mergedStuff['Label'][i]
             sub = mergedStuff['Subject'][i]
             for j in loaded.index:
                 if loaded["Subject"][j] == sub:
                     if var == 0:
                         loaded['Label'][j] = 1
                     else:
                         loaded['Label'][j] = 0
    loaded.to_csv("finedresult.csv")

