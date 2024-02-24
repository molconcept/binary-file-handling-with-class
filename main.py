#Modules Imported
import pickle

#Global Variable
file = "fix_info.dat"

#Class Definations
class Fix:
    def __init__(self, fix_id, info, status = "pending"):
        self.fix_id = fix_id
        self.info = info
        self.status = status

#Function Definations
def file_check():
    global file
    curr_file = input("Enter the name of the binary file : ")

    #Checking if the file exist or not
    try:
        fh = open(curr_file, 'rb')
        fh.close()
        file = curr_file

    #Creating the file if it doesn't exist
    except FileNotFoundError:
        print("File Doesn't Exist!")
        print()
        print("CREATING! a new file")
        new_file = input("Enter the name of file you want to create : ")
        if '.dat' in new_file:
            file = new_file
        else:
            file = new_file + '.dat'
        fh = open(file, 'wb')
        fh.close()
        print("Created {}".format(file))
        print()

def pickle_data(main_data):
    global file
    with open(file, 'wb') as f:
        pickle.dump(main_data, f)

def unpickle_data():
    global file
    with open(file, 'rb') as f:
        while True:
            #Handling situation when file pointer reaches End Of File
            try:
                main_data = pickle.load(f)
            except EOFError:
                break 
        #Handling situation when main_data is empty
        try:
            return main_data
        except UnboundLocalError:
            return False

def dsp_record():
    global file
    #Unpickling data from Binary File
    temp = unpickle_data()

    #When Binary File is Empty
    if not temp:
        print("The File {} is Empty!".format(file))
        print("Can't Display Anything!")

    else:
        #Displaying data pickled from Binary File
        trace = 0
        for unit in temp:
            print("==================== RECORD NO.{} ====================".format(unit[0]))
            print("# App Name - ", unit[1])
            print("# Current App Version - ", unit[2])
            print("# Fixes to be made for newer upcoming version :-")
            for obj in unit:
                if trace < 3:
                    trace += 1 
                    continue
                else:
                    print(obj.fix_id, '-', obj.info, "[Status] - ", obj.status)
            print("=====================================================")
            print()
            trace = 0

def apd_record():
    global file
    #Unpickling data from Binary File
    temp = unpickle_data()

    #When Binary File is Empty
    if not temp:
        # Writing a new record if the file is empty
        print("ATTENTION! - The file {} is empty".format(file))
        print("WRITING! a new record to the empty file")
        print()
        temp = []
        rec_id = 1

    #Appending record to the unpickled data from Binary File
    else:
        print("APPENDING! a new record to the file {}".format(file))
        print()
        rec_id = temp[-1][0]
        rec_id += 1

    #Creating a new record unit list
    new_rec = []
    app_name = input("Enter the Name of Application : ")
    curr_ver = float(input("Enter the Current Application Version : "))
    n = int(input("Enter the number of fixes you want to make to this batch : "))
    #Append data to the unit list i.e. new_rec
    new_rec.append(rec_id)
    new_rec.append(app_name)
    new_rec.append(curr_ver)
    for i in range(n):
        x = input("Enter Fix {} Info : ".format(i+1))
        new_rec.append(Fix(i+1, x))
        print("Data Entered")
        print()
    print("ATTENTION! - By Default the status of all the fixes will be set to 'pending'")
    print()
    #Appending new record unit list to main data list
    temp.append(new_rec)

    #Pickling Appended data to Binary File
    pickle_data(temp)

def edit_record():
    global file
    #Unpickling data from Binary File
    temp = unpickle_data()

    #When Binary File is Empty
    if not temp:
        print("The File {} is Empty!".format(file))
        print("Can't Edit an empty Record!")

    #Editing unpickled data from Binary File
    else:
        trace = 0
        rec_id = int(input("Enter the number of the record you want to edit : "))
        #Outer loop for record searching
        for unit in temp:
            if rec_id == unit[0]:
                obj_no = int(input("Enter the serial number of the fix you want to edit : "))
                #Inner loop for fix searching and edit
                for obj in unit:
                    if trace < 3:
                        trace += 1
                        continue
                    else:
                        if obj_no == obj.fix_id:
                            print("****************************************************")
                            print("To edit 'info' Enter 'i'")
                            print("To edit 'status' Enter 's'")
                            opt = input("Enter a Choice : ")
                            if opt == 'i' or opt == 'I':
                                x = input("Enter New Fix Info : ")
                                obj.info = x
                            elif opt == 's' or opt == 'S':
                                y = input("Enter New Status Info : ")
                                obj.status = y
                            print("*******************Data Updated*********************")
                            print()
                            #Inner loop will break if fix edited successfully
                            break
                        
                #Will execute only after full iteration of inner loop
                #Full iteration of inner loop will signify no matches found for the entered fix
                else:
                    print("Sorry no fix found at this number!")
                #Outer loop will break if fix edited successfully or record was found but can't find fix 
                break

        #Will execute only after full iteration of outer loop
        #Full iteration of outer loop will signify no matches found for the entered record
        else:
            print("Sorry no record found!")

        #Pickling Updated data to Binary File
        pickle_data(temp)
                
def del_record():
    #Unpickling data from Binary File
    temp = unpickle_data()

    #Searching and Deleting Record
    rec_no = int(input("Enter the number of the record you want to delete : "))
    for unit in temp:
            if rec_no == unit[0]:
                temp.remove(unit)
                print("Record {} Deletion Successful".format(rec_no))
                print()
                break
    else:
        print("Sorry no record found!")
    
    #Pickling Updated data to Binary File
    pickle_data(temp)
    
#Main Program Execution
cmd = 'empty'

print('''############## OPERATOR MENU ##############
= Enter 'R' to display records from file
= Enter 'A' to append new record to file
= Enter 'W' to edit a record from file
= Enter 'D' to delete a record from file
= Enter 'X' to exit the program
###########################################''')
print()

#Taking input and checking the existance of file
file_check()

#Operation Loop
while True:
    print()
    cmd = input("Enter the operator : ")
    print()

    if cmd == 'R' or cmd == 'r':
        dsp_record()

    elif cmd == 'A' or cmd == 'a':
        apd_record()

    elif cmd == 'W' or cmd == 'w':
        edit_record()

    elif cmd == 'D' or cmd == 'd':
        del_record()

    elif cmd == 'X' or cmd == 'x':
        break

    else:
        print("Invalid Operator")
        print("TRY AGAIN")
        print()

#Exit
print("End_Of_Program")
