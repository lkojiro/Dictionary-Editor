import csv
import string
import os
from pathlib import Path

def main():

    tokens = {"add","rem","new","del","quit",
              "help","peek","size","get",
              "addmul","list","rename"}


    while (True):

        token = ''
        in_line = []

        #Get a valid token
        while (token not in tokens or not areValidArgs(token,in_line)):  
            in_line = input("DICT EDITOR >>>> ").split()
            if len(in_line) == 0:
                continue
            token = in_line[0]

            if token not in tokens:
                print("invalid token: ",token)
                print("use 'help' for list of tokens")

            if not areValidArgs(token,in_line):
                print("invalid arguments, use 'help' for token useage")

        
        #in_line is a valid token with correct number of arguments


        if token == 'quit':
            break

        elif token == 'peek': 
            printDictFromFile(in_line[1] + '.csv')

        elif token == 'list':
            listDicts()

        elif token == 'help':
            print("\n --Separate tokens and arguments with spaces--\n")
            print("exit the editor:         quit")
            print("list dicts available     list")
            print("add a key/arg to dict:   add <filename> <key> <val>")
            print("remove a key from dict:  rem <filename> <key>")
            print("create new dict:         new <filename>")
            print("delete dict:             del <filename>")
            print("print contents of dict:  peek <filename>")
            print("get # of keys/vals:      size <filename>")
            print("rename dict:             rename <filename> <new name>")
            print("get val from key         get <filename> <key>")
            print("add n tuples (key,val)   addmul <filename> <(key,val)>....<(key,val)>\n")
            

        elif token =='add':
            filename = in_line[1] + '.csv'
            key = in_line[2]
            val = in_line[3]
            addToDict(filename,key,val)

        elif token == 'rem':
            filename = in_line[1] + '.csv'
            key = in_line[2]
            remFromDict(filename,key)

        elif token == 'new':
            filename = in_line[1] + '.csv'
            newDictToFile(filename)

        elif token == 'del':
            filename = in_line[1] + '.csv'
            deleteDict(filename)

        elif token == 'get':
            filename = in_line[1] + '.csv'
            key = in_line[2]
            printValAtKey(filename,key)

        elif token == 'size':
            filename = in_line[1] + '.csv'
            printSize(filename)
            
        elif token == 'addmul':
            filename = in_line[1] + '.csv'
            addmul(filename,in_line)

        elif token == 'rename':
            filename = in_line[1] + '.csv'
            newName = in_line[2] + '.csv'
            rename(filename,newName)

    return 0



def rename(filename,newName):
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return

    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}




    w = csv.writer(open(newName,"w"))

    for key_,val_ in new_dict.items():
        w.writerow([key_,val_])

    deleteDict(filename)



def listDicts():
    dicts = []

    for pth in Path.cwd().iterdir(): #from stackoverflow
        if pth.suffix == '.csv':
            dicts.append(pth)


    if dicts == []:
        print("No Dictionaries")
        return

    print('')
    for d in dicts:
        s = path2str(d)
        print(" ---- %s ---- "%s)    

    print('\n')



def path2str(path): #grabs filename + extension from path
    last = str(path).split("/")[-1]
    return last


def printSize(filename): #print num keys in dict
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return

    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}
    print("%s is of size %d"%(filename,len(new_dict)))



def addmul(filename,in_line): #adds tuples of args to dict as key:val
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return
        
    args = in_line[2:len(in_line)]
    tuples = []
    try:
        for t in args:
            key_ = t[1:t.index(',')]
            val_ = t[t.index(',')+1:len(t)-1]
            tuples.append((key_,val_))

        for tup in tuples:
            addToDict(filename,tup[0],tup[1])

    except:
        print("invalid arguments: keys not added")
        

    


def printValAtKey(filename,key): #displays dict[key]
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return
        
    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}

    if key not in new_dict:
        print("%s is not in %s" %(key,filename))

    else:
        print("%s[%s] --> %s" %(filename,key,new_dict[key]))



def remFromDict(filename,key): #removes key from dict
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return
        
    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}

    new_dict.pop(key)

    w = csv.writer(open(filename,"w"))

    for key_,val_ in new_dict.items():
        w.writerow([key_,val_])

    print("Removed %s from dict"%(key))




def deleteDict(filename): #removes dict
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return
        
    os.remove((os.getcwd() + "/" + (filename)))




def addToDict(filename,key,val): #adds elem key:val to dict
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return

    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}

    new_dict[key] = val

    w = csv.writer(open(filename,"w"))

    for key_,val_ in new_dict.items():
        w.writerow([key_,val_])

    print("Added [%s:%s] to %s" %(key,val,filename))
    




def newDictToFile(filename): #found online
    if isFileInDir(filename):
        print("Dict %s already exists" %filename)
        return

    dict = {}
    w = csv.writer(open(filename,"w"))
    for key,val in dict.items():
        w.writerow([key,val])

    print("New dict at",filename,'\n')




def printDictFromFile(filename):
    if not isFileInDir(filename):
        print("File not found: %s" %filename)
        return
        
    with open(filename,mode='r') as infile:
        reader = csv.reader(infile)
        new_dict = {rows[0]:rows[1] for rows in reader}

    print("\n     ----- %s -----\n" %(filename))
    print("   --keys--        --vals--\n")

    for key,val in new_dict.items():
        print("  ",key, " "*(14-len(key)), val)

    print('')



def areValidArgs(token,in_line): #ensures correct num arguments in input

    args = len(in_line) - 1

    if token == 'add':
        return args == 3

    elif token in {'rem','get','rename'}:
        return args == 2

    elif token in {'new','del','peek','size'}:
        return args == 1

    elif token in {'help','quit','list'}:
        return args == 0

    elif token == 'addmul':
        return args >= 2

    return False



def isFileInDir(filename):
    curr_path = os.getcwd()
    for file in os.listdir(os.fsencode(curr_path)):
        fl = os.fsencode(file)

        if fl == os.fsencode(filename):
            return True
    return False




if __name__ == '__main__':
    main()
    print("\n\nexiting...")