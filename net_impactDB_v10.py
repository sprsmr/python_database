#Version 10
#This program is a pilot of a front end interface for a DB.
#The DB will be used to coordinate info for Net Impact's business of supplying loupes.
#Started April 17, 2017

#Programmatic info

#sqlite info
#sqlite3.connect(filename) connects to the DB file
#con = sqlite3.connect(filename) ties it to an easy to use variable
#con.close; close the DB file
#cur = con.cursor()  creates an easy to use cursor;  a pointer in the DB
#Knowing the schema is essential;  display it with this
#Example of clinic follows
#cur.execute('SELECT sql FROM sqlite_master WHERE type = "table" AND name = "Clinic"')
#Other sqlite commands
#SELECT * FROM Dentist; select all columns from table Dentist; add WHERE and other operators to choose specific info
#
#Schema
#Clinic table
#('CREATE TABLE Clinic(cnam TEXT, pbox TEXT, add_unum TEXT, add_snum TEXT, add_stre TEXT, add_styp TEXT, add_quad TEXT, add_city TEXT, add_prov TEXT,
# add_pcod TEXT, add_coun TEXT, phon TEXT, faxx TEXT, toll TEXT, onam TEXT, emal TEXT, webb TEXT)')
#[cnam = clinic name; pbox = post office box info; add_unum = address unit number; add_snum = street number; add_stre = street name or number; add_styp = street type (for 
#example Street or Road or Trail; add_quad = SE or SW or NW or NE; add_city = city; add_prov = province; add_pcod = postal code; add_coun = country; phon = phone number; faxx
#= fax number; toll = toll free number; onam = office manager name; emal = email address; webb = web site]
#add_quad should only ever be SE or SW or NE or NW
#
#Dentist table
#[('CREATE TABLE Dentist (fnam TEXT, mnam TEXT, lnam TEXT, titl TEXT, cred TEXT , cell TEXT, home TEXT, mail TEXT, comm TEXT)')
#[fnam = first name; mnam = middle name of initial; lnam = last name; titl = title; cred = credential like DDS; cell = cell number;
#home = home phone number; mail = personal email; comm = comment]
#
#Cross Connect table
#Table - cross connect between dentist and clinic; this table enables a many to many relationship
#('CREATE TABLE Dent_Clin_Cross (clie_id INT, clin_id INT )')
#[clie_id = Dentist table row id for client; clin_id = Clinic table row id for clinic]
#
#Important operational info on SQLITE: rowid is used as primary key in tables in this DB
#The next rowid number is chosen automatically by adding 1 to the highest rowid in use
#Therefore if a record is deleted and it is the last record in the table the next record will get
#the same rowid that the deleted one just had.
#However if record is deleted that is somewhere else in the table, that rowid will not be used again
#This behaviour creates a corner case where a new record could be linked to another table record
#inadvertantly if the link between the table records has not also been deleted.
#
#Importing regular expressions in order to recognize a phone number and process it
#
#
#


#Imports
import sqlite3
import time
import re


#Version and change information follows; stored in a variable
version_info = '''
Version and change info follows:
June 30, 2017 - Vers 7
(Done)Changed some of the wording in user messages.  eg. 'Enter data here', etc.
(Done)Need to change edit client when name fragment doesnt exist in DB and therefore no number comes up.
(Done)Need to change add client user messageing to be more clear that if you choose 'n', the data isn't saved.
(Done)Added this version info and command to display; for now its hidden; the command is version.
(Done)Need to add toll column to clinic table for toll-free numbers
(Done)Need to add home column to dentist table for home phone number
Need to add delete clinic
(Done)Need to add comment column to dentist table
(Done)Need to add column to clinic for post office mailbox info
(Done)Need to handle no client found in show client/clinic (same as name fragment doesn't exist above)
Need to add search on number; enter a number and find the client or clinic
(Done)Need to change how add client searches for duplicates; if last name field is blank it stops the command altogether.
(Done)Need to add stop function to add client
---------------------------------------------------
July 19, 2017 - Vers 8
July 30, 2017; into production
(Done)Need search on number; find client using phone number (use re to recognize phone number)
Need find client to give all contact numbers back
(Done)Need trim down output while adding clients and clinics; with over 100 entries this has no value
      Also changed how user is prompted in adding client to avoid quick repitition of hitting enter 

---------------------------------------------------
August 6, 2017 - Vers 9
Feedback from users
Show clinic and showing of clinic after an add now has little value; too many to see easily.
Find clinic doesn't work yet (known issue)
Missing credentials in edit client
Development
(Done)Need to change show clinic and add clinic to limit number of clinics shown (currently 7)
(Done)Need to add find clinic feature
Need to check that find client on phone number gives back multiple clients when they exist


End version info.
'''


#Create functions

def add_clin_info():
    """
    This function adds clinic info to the Clinic table in the db.  This table has the following column headings:
    cnam - clinic name; pbox - post office box info; add_unum - unit number; add_snum - street address number; add_stre - street name/number; add_styp - street type; add_quad - city quadrant (SE, SW, NE, NW);
    add_city - city; add_prov - province; add_pcod - postal code; add_coun - country; phon - clinic phone number; faxx - fax number; toll - toll-free number; onam - office manager/contact name;
    emal - email address; webb - web site
    The user is prompted for each of these entries; at the end the user is prompted for accuracy check of the data.
    Currently, pressing enter loads the data into the db; any other entry aborts the process and the function ends.
    Changed this (Currently, after this, the full table is printed out)
    """
    
    print("Enter clinic information as prompted.  If the info is not required press enter to produce an empty field.")
    cnam = input("Enter name of the clinic.  ")
    pbox = input("Enter post office box info (if any).  ")
    add_unum = input("Enter unit number.  ")
    add_snum = input("Enter street address number.  ")
    add_stre = input("Enter street name or number .  ")
    add_styp = input("Enter street type.  For example 'Street' or 'Road' or 'Trail'.  ")
    add_quad = input("Enter city quadrant if applicable.  Can only be SE, SW, NE, or NW.  ")
    add_city = input("Enter city.  ")
    add_prov = input("Enter province.  ")
    add_pcod = input("Enter postal code.  ")
    add_coun = input("Enter country.  ")
    phon = input("Enter phone number.  ")
    faxx = input("Enter fax number.  ")
    toll = input("Enter toll-free number.  ")
    onam = input("Enter name of office manager or contact.  ")
    emal = input("Enter email address.  ")
    webb = input("Enter web site.  ")

    #printing input info to check
    print('\n\n' + cnam)
    print(pbox)
    print(add_unum + ', ' + add_snum + ' ' + add_stre, add_styp, add_quad + '\n' + add_city + ', ' + add_prov + '\n' + add_pcod + '\n' + add_coun)
    print(phon + '  ' + faxx + '  ' + toll)
    print(onam)
    print(emal + '  ' + webb + '\n')

    print('\n(If the above info is almost correct, answer y to the next question; then go back and edit it.)\n')

    confirm = input("Is the above info correct. \nIf yes this data will be written to the database.  If no this data will be discarded. \n(y or n)  -->   ")
    
    cond_valid = False
    while cond_valid == False:
        if confirm == 'y':
            break
        elif confirm == 'n':
            print('\nData has been discarded.\n')
            return('Halted')
        else:
            confirm = input('You must enter either "y" or "n".  --> ')

    cur.execute('INSERT INTO Clinic VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (cnam, pbox, add_unum, add_snum, add_stre, add_styp, add_quad, add_city, add_prov, add_pcod, add_coun, phon, faxx, toll ,onam, emal, webb))

    cur.execute('SELECT * FROM Clinic')
    clin_out = cur.fetchall()
    print('\nThe following clinic record will be stored in the database once you save or exit.\n')
    print('You can still edit the clinic record by doing "edit clinic" right away (even before its saved).\n')
    print(clin_out[-1])


    return('Success')


def add_dent_info():
    '''
    This function adds dentist info to the Dentist table in the db. This table has the following column headings:
    fnam - first name; mnam - middle name or initial; lnam - last name; titl - title(s) or credentials (DDS, etc.); cell - cell phone number;
    home - home phone number; mail - personal email; comm - comment.
    '''
    print("Enter client information as prompted.  If the info is not required press enter to produce an empty field.")
    fnam = input("Enter first name of client.  ")
    mnam = input("Enter middle name or initial of client.  ")
    lnam = input("Enter last name of client. (**OR stop**) ")
    
    if lnam == "stop":
        return "Halted"
    elif lnam == '':
        return "Blank"
    
    #duplicate check
    cur.execute('SELECT fnam, mnam, lnam FROM Dentist WHERE lnam LIKE ?', ('%'+lnam+'%',))
    clie_info = cur.fetchall()
    for clie in clie_info:
    

        if lnam in clie[2]:
            print(clie)
            print(fnam + ' ' + lnam + ' looks like a duplicate!')
            dup_ans = input("Is it? (y or n)")
            if dup_ans == "y":
                print("Duplicate being ignored")
                return
    #
    #
    titl = input("Enter title.  ")
    cred = input("Enter credential.  ")
    cell = input("Enter cell phone number.  ")
    home = input("Enter home phone number.  ")
    mail = input("Enter personal email if there is one.  ")
    comm = input("Enter comments (if any).  ")
    

    print("The client info is: \n")
    print(lnam + ', ' + fnam + ' ' + mnam + '  ' + titl + ' ' + cred + ' ' + cell + ' ' +  home + ' ' + mail + ' ' + comm)

    clie_ans = input("Is the above info correct. \nIf yes this data will be written to the database.  If no this data will be discarded. \n(y or n)  ")
    
    if clie_ans == 'y':
        cur.execute('INSERT INTO Dentist VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', (fnam, mnam, lnam, titl, cred, cell, home, mail, comm))

    return "Success"

def match_clie_clin():
    '''This function matches clients to clinics.  It asks for a client, then a clinic and enters both
       IDs into a table used to hold the relationship.  Using a separate table allows a many to many
       match. 
    '''
    cond_multi_clinic = True
    
    while cond_multi_clinic == True:
        clie = input('Enter a last name of a client you want to match? (You can type in a partial last name.)  ')

        cur.execute('SELECT rowid,fnam,lnam FROM Dentist WHERE lnam LIKE ?', ('%'+clie+'%',))
        poss_clie = cur.fetchall()
        print (poss_clie)
        if poss_clie == []:
            print("No match.")
            break
        while True:
            try:
                clie_ans = int(input("Choose the number of the correct name.  "))
                break
            except ValueError:
                print("Oops, not a number. ")


        clin = input('What clinic(s) does the client work in? (You can type in a partial word.)  ')
        cur.execute('SELECT rowid,cnam FROM Clinic WHERE cnam LIKE ?', ('%'+clin+'%',))
        poss_clin = cur.fetchall()
        print (poss_clin)
        if poss_clin == []:
            print("No match")
            break

        while True:
            try:
                clin_ans = int(input("Choose the number of the correct clinic.  "))
                break
            except ValueError:
                print("Oops, not a number. ")

        print("You chose "+str(clie_ans)+" and "+str(clin_ans))

        enter_ans = input("Enter the match? (y or n) --> ")
        if enter_ans != "y":
            print("You did not enter 'y'. No match entered.\n")
            break
        
        cur.execute('INSERT INTO Dent_Clin_Cross VALUES(?, ?)', (clie_ans, clin_ans))
        print("Entering the match.")

        chng_cond = input("Are you finished matching clients and clinics? (y or n)  ")
        if chng_cond == "y":
            cond_multi_clinic = False
        
    return 


def show_clie():
    '''This function simply shows all clients int the Dentist table.
    '''
    cur.execute('SELECT rowid,* FROM Dentist')
    return cur.fetchall()

def show_clin():
    '''This function simply shows all the clinics in the Clinic table.
    '''
    cur.execute('SELECT * FROM Clinic')
    clin_outp = cur.fetchall()
    count = -7
    while count < 0:
        clin = clin_outp[count]
        print (clin)
        '''
        print(clin[0])
        print(clin[1])
        print(clin[2], ', ', clin[3], ' ', clin[4], ' ', clin[5], ' ', clin[6], sep='')
        print(clin[7]+',', clin[8], ' ', clin[9])
        print(clin[10])
        print(clin[11], clin[12], clin[13], sep='  ')
        print('Contact:', clin[14], sep=' ')
        print(clin[15], clin[16], sep=' ')
        #print('')
        '''
        count = count + 1
        
    return


def show_clie_clin():
    '''This function shows which clinics a client is linked to. Their can be multiple clinics linked to clients
       and multiple clients linked to a clinic.
    '''
    
    clie_ans = input("Which client do you want to show? (Can use partial name.) --> ")
    cur.execute('SELECT rowid,lnam FROM Dentist WHERE lnam LIKE ?', ('%'+clie_ans+'%',))
    clie_info = cur.fetchall()
    print(clie_info)
    if clie_info == []:
        print("No client found! Returning to main menu.")
        return
    clie_ans = input('Choose the number of correct client. --> ')
    #remove the * below and specify which columns you want
    cur.execute('SELECT * FROM Dentist LEFT JOIN Dent_Clin_Cross ON Dentist.rowid = Dent_Clin_Cross.clie_id LEFT JOIN Clinic ON Dent_Clin_Cross.clin_id = Clinic.rowid WHERE Dentist.rowid = ?', (clie_ans,))
    clie_info = cur.fetchall()
    for link in clie_info:
        print(link)
    return


def del_clie():
    '''
    This function deletes a client; it must against leaving orphan records in other tables
    To protect against orphan records it must first check to see if the rowid of this table exists
    in another table record;  if it doesn't then it can be deleted.
    This requirement is because sqlite does not ensure that a new rowid has not existed before
    A new rowid is chosed based on the current max rowid + 1; it is feasable that this could
    result in mismatched cross table entries
    '''
    clie_ans = input("Enter last name of client to be deleted? --> ")
    cur.execute('SELECT rowid,* from Dentist WHERE lnam LIKE ?', ('%'+clie_ans+'%',))
    clie_info = cur.fetchall()
    for clie in clie_info:
        print(clie)
    if clie_info == []:
        print("**No client found.**")
        return
    
    clie_ans = input("Choose the client number. --> ")
    print("Checking to see if this client is linked to a clinic.")
    cur.execute('SELECT * from Dent_Clin_Cross WHERE clie_id = ?', (clie_ans,))
    chek_clie = (cur.fetchall())
    if chek_clie == []:
        print("Client is not linked to a clinic.\nProceeding with client deletion!")
        del_ans = input("Are you sure you want to delete this client? This cannot be undone! (y or n) --> ")
        if del_ans == 'y':
            #clie_ans = int(clie_ans)
            print (clie_ans)
            cur.execute('DELETE from Dentist WHERE rowid = ?', (clie_ans,))
            print("Client deleted.\n")
        else:
            print("You chose not to delete this client.")
        return
    print("Client is linked to a clinic.\nClient NOT deleted.")
    return

def del_clin():
    print("**Working on it**")


def find_clie():
    '''This function finds a specific client and the associated clinic.  You can
       look up by partial name or any phone number
    '''
    phon_num = re.compile(r'\d\d\d.\d\d\d.\d\d\d\d')

    clie_ans = input("Enter last name or phone number of client you want. --> ")

    mo = phon_num.search(clie_ans)
    
    if mo == None:
        print("\nYou're searching on a client name.\n")
        srch_type = 'name'
    else:
        print('\nYour searching on a phone number.\n')
        srch_type = 'phone'

    #searching on partial last name
    if srch_type == 'name':        
        cur.execute('SELECT rowid,* from Dentist Where lnam LIKE ?', ('%'+clie_ans+'%',))
        clie_data = cur.fetchall()
        if clie_data == []:
            print('\nNo client found.\n')
            return
        for clie in clie_data:
            
##

            cur.execute('SELECT *,rowid FROM Dent_Clin_Cross WHERE clie_id = ?', (clie[0],))
            find_data_cross = (cur.fetchall())
            #index is a client so print it first
            print(clie)
            for i in find_data_cross:
                cur.execute('SELECT * FROM Clinic WHERE rowid = ?', (i[1],))
                print(cur.fetchall())

##          
        return

    #searching on a phone number


    ######################################
    #using regex

    var = mo.group(0)

    #a phone number search should always produce only a single row because there should be no duplicates

    cond = True
    while cond == True:
        cur.execute('SELECT *,rowid FROM Dentist WHERE cell = ?', (var,))
        index = cur.fetchall()
        if index != []:
            cond = 'Client'
            break
        cur.execute('SELECT *,rowid FROM Dentist WHERE home = ?', (var,))
        index = cur.fetchall()
        if index != []:
            cond = 'Client'
            break
        cur.execute('SELECT *,rowid FROM Clinic WHERE phon = ?', (var,))
        index = cur.fetchall()
        if index != []:
            cond = 'Clinic'
            break
        cur.execute('SELECT *,rowid FROM Clinic WHERE faxx = ?', (var,))
        index = cur.fetchall()
        if index != []:
            cond = 'Clinic'
            break
        cur.execute('SELECT *,rowid FROM Clinic WHERE toll = ?', (var,))
        index = cur.fetchall()
        if index != []:
            cond = 'Clinic'
            break
        print('\nThe phone number was not in the database.\n')
        cond = False

    if index != []:
        #if index is a clinic, then find the linked client or clients
        #if index is a client, then find the clinic or clinics
        #there could be valid duplicates in the cross link table because a client could work at 2 clinics
        #and a clinic may have more than one client
    
        if cond == 'Clinic':
            #
            cur.execute('SELECT *,rowid FROM Dent_Clin_Cross WHERE clin_id = ?', (index[0][-1],))
            find_data_cross = (cur.fetchall())
            #this will allow for duplicates
            for i in find_data_cross:
                cur.execute('SELECT * FROM Dentist WHERE rowid = ?', (i[0],))
                print(cur.fetchall())
            #index is a clinic so print it last
            print(index)

        if cond == 'Client':
            cur.execute('SELECT *,rowid FROM Dent_Clin_Cross WHERE clie_id = ?', (index[0][-1],))
            find_data_cross = (cur.fetchall())
            #index is a client so print it first
            print(index)
            for i in find_data_cross:
                cur.execute('SELECT * FROM Clinic WHERE rowid = ?', (i[1],))
                print(cur.fetchall())

    #######################################
    return

def find_clin():
    #print("Working on this new feature.")
    clin_ans = input("Enter the clinic you want to find.  (Can use partial name.) --> ")
    cur.execute('SELECT rowid,* from Clinic Where cnam LIKE ?', ('%'+clin_ans+'%',))
    clin_list = cur.fetchall()
    if clin_list == []:
        print("\nClinic was not found.\n")
    else:
        for clin in clin_list:
            print(clin)
    return


def edit_clin():
    '''This function edits a field in a record in the Clinic table.  Only one field at a time can be edited and then saved.
    '''
    clin_ans = input("Enter the clinic you want to edit. (Can use a partial name.)--> ")

    cur.execute('SELECT rowid,* from Clinic Where cnam LIKE ?', ('%'+clin_ans+'%',))
    for clin in cur.fetchall():
        print(clin)

    clin_id = input("Enter the number of the clinic to edit.  --> ")

    cur.execute('SELECT * from Clinic Where rowid = ?', (int(clin_id),))
    print(cur.fetchall())
    
    clin_conf = input("Is this the clinic to edit?  (y or n) --> ")

    if clin_conf == "y":
        print("test**ready to update**")
        clin_field = input('''Choose a field to edit:

clinic name
po box
unit number
street address number
street name or number
street type
city quadrant
city
province
postal code
country
phone
fax
toll-free
contact
email
web

Enter field name here -->  ''')
        if clin_field == 'clinic name':
            col_name = 'cnam'
        elif clin_field == 'po box':
            col_name = 'pbox'
        elif clin_field == 'unit number':
            col_name = 'add_unum'
        elif clin_field == 'street address number':
            col_name = 'add_snum'
        elif clin_field == 'street name or number':
            col_name = 'add_stre'
        elif clin_field == 'street type':
            col_name = 'add_styp'
        elif clin_field == 'city quadrant':
            col_name = 'add_quad'
        elif clin_field == 'city':
            col_name = 'add_city'
        elif clin_field == 'province':
            col_name = 'add_prov'
        elif clin_field == 'postal code':
            col_name = 'add_pcod'
        elif clin_field == 'country':
            col_name = 'add_coun'
        elif clin_field == 'phone':
            col_name = 'phon'
        elif clin_field == 'fax':
            col_name = 'faxx'
        elif clin_field == 'toll-free':
            col_name = 'toll'
        elif clin_field == 'contact':
            col_name = 'onam'
        elif clin_field == 'email':
            col_name = 'emal'
        elif clin_field == 'web':
            col_name = 'webb'
        else:
            print("No field chosen!")
            return

    field_info = input("Enter the new info you're adding. (The old field entry will be erased.) --> ")

    
    sql_comm = 'UPDATE Clinic set '+col_name+' = ? WHERE rowid = ?'

    cur.execute(sql_comm, (field_info, clin_id))
    cur.execute('SELECT * from Clinic WHERE rowid = ?', (clin_id,))
    print("Updated clinic:")
    print(cur.fetchall())

        
    return



def edit_clie():
    '''This function edits a field in a record in the Dentist table. Only one field at a time can be edited and then saved.
    '''
    clie_ans = input("Enter the client last name you want to edit. (Can use a partial name.)--> ")

    cur.execute('SELECT rowid,* from Dentist Where lnam LIKE ?', ('%'+clie_ans+'%',))
#
#    print(cur.fetchall())

    fetch = cur.fetchall()
    
    if fetch == []:
        print()
        print("*"*57 + "\nNo clients found in the database matching that criteria.\n" + "*"*57)
        print()
        return
#
    for clie in fetch:
        print(clie)

    clie_id = input("Enter the number of the client to edit.  --> ")

    cur.execute('SELECT * from Dentist Where rowid = ?', (int(clie_id),))
    print(cur.fetchall())
    
    clie_conf = input("Is this the client to edit?  (y or n) --> ")

    if clie_conf == "y":
        clie_field = input('''Choose a field to edit:

first name
middle name
last name
title
cred
cell
home
email
comment

Enter field name here  --> ''')
        if clie_field == 'first name':
            col_name = 'fnam'
        elif clie_field == 'middle name':
            col_name = 'mnam'
        elif clie_field == 'last name':
            col_name = 'lnam'
        elif clie_field == 'title':
            col_name = 'titl'
        elif clie_field == 'cred':
            col_name = 'cred'
        elif clie_field == 'cell':
            col_name = 'cell'
        elif clie_field == 'home':
            col_name = 'home'
        elif clie_field == 'email':
            col_name = 'mail'
        elif clie_field == 'comment':
            col_name = 'comm'
        else:
            print("No field chosen!")
            return


        field_info = input("Enter the new info you're adding.  --> ")
        
        sql_comm = 'UPDATE Dentist set '+col_name+' = ? WHERE rowid = ?'

        cur.execute(sql_comm, (field_info, clie_id))
        cur.execute('SELECT * from Dentist WHERE rowid = ?', (clie_id,))
        print("Updated client:")
        print(cur.fetchall())
    
        
    else:
        print("No client chosen")
        return

def save():
    '''This function saves the data to the database. If a glitch occurs after, the data is there.
    '''
    con.commit()
    print("\n***********\nData saved.\n************\n")
    return

def version():
    print('*'*80)
    print (version_info)
    print('*'*80)
    return

#####################################################################

#Main program starts.

#Current DB File version is net_impactDB_v9.db
#Connect to DB
con = sqlite3.connect('net_impactDB_v9.db')
cur = con.cursor()

cond_clin = 'go'
cond_dent = 'go'
cond_func = 'go'

#Create a loop to ask for a function


while cond_func == 'go':
    #functions to add
    #show commands; like show clients or show client clinic matches
    show_com = ['SHOW', '-'*18, 'show client', 'show clinic', 'show client/clinic', '']
    find_com = ['FIND', '-'*18, 'find client', 'find clinic', '', '']
    add_com = ['ADD', '-'*18, 'add client', 'add clinic', '', '']
    match_com = ['MATCH', '-'*18, 'match client', '', '', '']
    delete_com = ['DELETE', '-'*18, 'delete client', 'delete clinic', '', '']


    #new command to create
    edit_com = ['EDIT', '-'*18, 'edit client', 'edit clinic', '', '']
    save_com = ['SAVE', '-'*18, 'save', '', '', ''] 
        
    print('\nThis is the production version.  Version 9\n')

    print('COMMANDS:\n')

    count = range(6)

    for c in count:
        print('{:<20}'.format(show_com[c]), end='')
        print('{:<20}'.format(find_com[c]), end='')
        print('{:<20}'.format(add_com[c]), end = '')
        print('{:<20}'.format(match_com[c]), end = '')
        print('{:<20}'.format(edit_com[c]))

    print('\n')
    count = range(6)

    for c in count:
        print('{:<20}'.format(delete_com[c]), end='')
        print('{:<20}'.format(save_com[c]))


    func_ans = input('''Enter a command or enter 'exit'.  (**exit also writes the data to the database**)
-->  ''')

    if func_ans == 'add clinic':
        #clinic
        while cond_clin == 'Success' or 'go':
            cond_clin = add_clin_info()
            if cond_clin == 'Halted':
                break
            cond_anoth = input('Enter another? (y or n)')
            if cond_anoth != 'y':
                break

        #cur.execute('SELECT * FROM Clinic')
        #turning this off
        #for clin in (cur.fetchall()):
        #    print(clin)

    elif func_ans == "add client":
        #clients
        while cond_dent == 'Success' or 'go':
            cond_dent = add_dent_info()
            if cond_dent == 'Halted':
                print('\nStopping the command "add client"!\n')
                break
            elif cond_dent == 'Blank':
                print('\nBlank field entered as last name; no client entered.\n')
                break
            cond_anoth = input('Enter another?  (y or n)')
            if cond_anoth != 'y':
                cur.execute('SELECT rowid,* FROM Dentist')
                for dent in (cur.fetchall()):
                    print(dent)
                break

    elif func_ans == "delete client":
        result_del_clie = del_clie()

    elif func_ans == "delete clinic":
        del_clin()

    elif func_ans == "find client":
        result_find_clie = find_clie()

    elif func_ans == "find clinic":
        find_clin()

    elif func_ans == "match client":
        #matches
        #could change to link client???
        match_clie_clin()

    elif func_ans == "show client":
        result_clie = show_clie()
        for c in result_clie:
            print (c)
        print("\n")
        
    elif func_ans == "show clinic":
        show_clin()
        
    elif func_ans == "show client/clinic":
        show_clie_clin()

    elif func_ans == "edit clinic":
        edit_clin()

    elif func_ans == "edit client":
        edit_clie()
    
    elif func_ans == "save":
        save()

    elif func_ans == "exit":
        print("Good Bye")
        time.sleep(1)
        break

    elif func_ans == "version":
        version()

    else:
        print("\n\t*No command entered.*\n")
        time.sleep(1)

#Commit the changes to make them permanent
con.commit()

#Close the DB file
con.close()
