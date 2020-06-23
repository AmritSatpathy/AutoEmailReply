import os


def rem():
    os.remove("all_emailrecieved.json")
    os.remove("all_emailsent.json")
    os.remove("cleaned.csv")
    os.remove("cleanedsent.csv")
    os.remove("fromjson.csv")
    os.remove("fromsentjson.csv")
    os.remove("predictedresult.csv")
    os.remove("result.csv")
    print("File Removed!")
