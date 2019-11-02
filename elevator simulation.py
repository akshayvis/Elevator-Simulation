# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 16:07:42 2019

@author: Akshay Viswanathan
"""


#Packages
from tkinter import *
from tkinter.ttk import *
import random
from xlwt import Workbook 
import string
# Importing the libraries
import numpy as np
import pandas as pd

#Elevator Class
class Elevator:
    def __init__(self, elenum, elecurpos, eledir, clnf, clbf, elesf, elesflst, eleisactive, clspeed):
        self.elenum = elenum                    #Elevator's identifier
        self.elecurpos = elecurpos              #Elevator's current position
        self.eledir = eledir                    #Elevator's direction
        self.clnf = clnf                        #total no. of floors
        self.clbf = clbf                        #total no. of basements
        self.elesf = elesf                      #Elevator's next destination
        self.elesflst = elesflst                #Elevator's destination list
        self.eleisactive = eleisactive          #Elevator's status
        self.clspeed = clspeed                  #Elevator's speed
        if(self.elecurpos == clnf and self.eledir == 'U'): #Go down after reaching top floor
            self.eledir = 'D'
        elif(self.elecurpos == clbf and self.eledir == 'D'): #Go up after reaching bottom
            self.eledir == 'U'        
        

#Function to find the distance/speed aka time between the elevator's current position and the user's position           
def disfunc(funcf, funelecurpos, funeledir, funnf, funsf, funisactive, funheightdict, funcspeed):
    if (funisactive == 'N'):
        return (funnf*3000)
    else:
        dist = 0   
        #User in same floor as Elevator
        if(funelecurpos == funcf):
            return 0.0
        
        #User below elevator and elevator is static or coming down
        elif((funelecurpos > funcf) and ((funeledir == 'S') or (funeledir == 'D'))):
            for i in range(funelecurpos, funcf, -1):
                dist+=funheightdict[str(i)]
            return (dist / funcspeed)   
                
        #User above elevator and elevator is static or coming up
        elif((funelecurpos < funcf) and ((funeledir == 'S') or (funeledir == 'U'))):
            for i in range(funelecurpos,funcf):
                dist+=funheightdict[str(i)]
            return (dist / funcspeed)   
        
        #User below elevator but the elevator is going up
        elif((funelecurpos > funcf) and (funeledir == 'U')):
            for i in range(funelecurpos,funsf):
                dist+=funheightdict[str(i)]
            for i in range(funsf,funcf,-1):
                dist+=funheightdict[str(i)]
            return (dist / funcspeed)
        
        #User above elevator but the elevator is going Down
        elif((funelecurpos < funcf) and (funeledir == 'D')):
            for i in range(funelecurpos,funsf):
                dist+=funheightdict[str(i)]
            for i in range(funsf,funcf):
                dist+=funheightdict[str(i)]
            return (dist / funcspeed)
        
#Function to input destination floors for elevator
def flstopfunc(stnum,enum, flstnf, flstbf):
    ctr = 0
    while(ctr < stnum):
        val = []
        for j in range(stnum):
            try:
                t = int(input(f'Enter the stop {j+1} for elevator {enum + 1}: '))
                if ((t > flstnf) or (t < flstbf)):
                    raise ValueError()
                else:
                    val.append(t)
                    ctr+=1                   
            except:
                print(f'Error! Please enter a valid number between {flstbf} and {flstnf} ')
                ctr = 0
                break
    return val
    

#Function to return elevator list for dropbox   
def appvalues(appfntot):
    rval = []
    for i in range(1,appfntot+1):
        rval.append(i)
    return rval

#Function to schedule maintenance
def schmfunc(schmelenum):
    elevator[schmelenum].eleisactive = 'N'
    print(f'Elevator {schmelenum+1} is now suspended for Maintenance!')

#Function to complete maintenance    
def compmfunc(compmnum):
    if (elevator[compmnum].eleisactive == 'N'):
        elevator[compmnum].eleisactive = 'Y'
        print(f'Maintenance work for Elevator {compmnum+1} is now complete and ready for use !')
    else:
        print(f'Elevator {compmnum + 1} is currently not under maintenance!')
        
#Function to implement emergency feature        
def emergfunc(emergnum,emernf):
    if(elevator[emergnum].eledir == 'U' and elevator[emergnum].elecurpos != emernf):
        elevator[emergnum].elecurpos += 1
        print(f'Elevator {emergnum + 1} has stopped at floor {elevator[emergnum].elecurpos}. Inspection Required! ')
        elevator[emergnum].eleisactive = 'N'
    elif(elevator[emergnum].eledir == 'U' and elevator[emergnum].elecurpos == emernf):
        elevator[emergnum].elecurpos -=1
        print(f'Elevator {emergnum + 1} has stopped at floor {elevator[emergnum].elecurpos}. Inspection Required!')
        elevator[emergnum].eleisactive = 'N'
    elif(elevator[emergnum].eledir == 'D' and elevator[emergnum].elecurpos != 0):
        elevator[emergnum].elecurpos -= 1
        print(f'Elevator {emergnum + 1} has stopped at floor {elevator[emergnum].elecurpos}. Inspection Required!')
        elevator[emergnum].eleisactive = 'N'
    elif(elevator[emergnum].eledir == 'D' and elevator[emergnum].elecurpos == 0):
        elevator[emergnum].elecurpos += 1
        print(f'Elevator {emergnum + 1} has stopped at floor {elevator[emergnum].elecurpos}. Inspection Required!')
        elevator[emergnum].eleisactive = 'N'
    else:
        print(f'Elevator {emergnum + 1} at floor {elevator[emergnum].elecurpos} has stopped. Inspection Required!')
        elevator[emergnum].eleisactive = 'N'
        
#Function to implement Power failure situation
def pffunc(pffunne):
    print('Power Failure!')
    for k in range(pffunne):
        emergfunc(k,pffunne)

#Function to implement Power Supply fix        
def pffixfunc(pffixne):
    print('Power Problem Solved! Elevators are ready to use!')
    for k in range(pffixne):
        elevator[k].eleisactive = 'Y'

#Function to implement show pos button        
def showpos(spfuncne):
    for k in range(spfuncne):
        if(elevator[k].eleisactive == 'Y'):
            if(elevator[k].eledir != 'S'):
                print(f'Elevator{k+1} is in floor {elevator[k].elecurpos} and is going to floor {elevator[k].elesf}')
            else:
                print(f'Elevator{k+1} is static at floor {elevator[k].elecurpos}')
        else:
            print(f'Elevator{k+1} is currently under maintenance')
#Imput Error Handling Function
def getinput(s):
    temp = 0
    while(temp == 0):
        try:
            res = int(input(s))
            temp = 1
        except:
            print('Please enter a valid number')
    return res    

#Simulation function
def simcompfunc():
    simfunc()
    print('Simulation Completed!')
   
#Customer Simulation    
def simfunc(dummypara1, dummypara2, dummypara3, dummypara4):
    simcf = dummypara1
    simdf = dummypara2
    simdistlst = []
    for i in range(ne):
        elevator[i].elecurpos = random.choice(elevator[i].elesflst)
        if(elevator[i].elecurpos == max(elevator[i].elesflst)):
            elevator[i].eledir = random.choice(['D','S'])
        elif(elevator[i].elecurpos == min(elevator[i].elesflst)):
            elevator[i].eledir = random.choice(['U','S'])
        else:
            elevator[i].eledir = random.choice(['U','D','S'])
        if(elevator[i].eledir == 'S'):
            elevator[i].elesf = elevator[i].elecurpos
        elif(elevator[i].eledir == 'U'):
            elevator[i].elesf = random.randint((elevator[i].elecurpos)+1,max(elevator[i].elesflst))
            while (elevator[i].elesf not in elevator[i].elesflst):
                elevator[i].elesf = random.randint((elevator[i].elecurpos)+1,max(elevator[i].elesflst))
        else:
            elevator[i].elesf = random.randint(min(elevator[i].elesflst),(elevator[i].elecurpos)-1)
            while (elevator[i].elesf not in elevator[i].elesflst):
                elevator[i].elesf = random.randint(min(elevator[i].elesflst),(elevator[i].elecurpos)-1)
                
        
        if((simcf in elevator[i].elesflst) and (simdf in elevator[i].elesflst)):
            simdistlst.append(disfunc(simcf, elevator[i].elecurpos, elevator[i].eledir, nf, 
                                       elevator[i].elesf, elevator[i].eleisactive, heightdict, elevator[i].clspeed))
        else:
            simdistlst.append(nf*3000)
                
        
    simmini = min(simdistlst)
    if (simmini < (nf*3000)):
        simfinalele = simdistlst.index(simmini)
        #print(f'Please use elevator #{finalele} to save time!')
        return (simcf, simdf, simfinalele, elevator[simfinalele].clspeed)
    else:
        simfinalele = ne*2
        #print('No elevators are availabe at the moment')
        return (simcf, simdf, simfinalele, 99999)

def sheetwr(swsheet1, swq, swscf,swsdf,swsfele,swsspeed):
    swsheet1.write(swq+1, 0, f'{swscf}')
    swsheet1.write(swq+1, 1, f'{swsdf}')
    swsheet1.write(swq+1, 2, f'{swsfele}')
    swsheet1.write(swq+1, 3, f'{swsspeed}')


#Data Generation Function    
def gendata(wb):
    if(wb == ""):
        print("Please enter a file name")
    else:
        elewb = randomString()
        elewb = Workbook() 
        # add_sheet is used to create sheet. 
        sheet1 = elewb.add_sheet('Sheet 1') 
        sheet1.write(0, 0, 'User position')
        sheet1.write(0, 1, 'User Destination')
        sheet1.write(0, 2, 'Elevator Used')
        sheet1.write(0, 3, 'Elevator speed')
    
        for q in range(1880):
            dummysfele = 0
            dummysspeed = 0
            if q<750:
                scf,sdf,sfele,sspeed = simfunc(0, 4, dummysfele, dummysspeed) 
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q>750 and q<1500:
                scf,sdf,sfele,sspeed = simfunc(4, 0, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q>1500 and q<1540:
                scf,sdf,sfele,sspeed = simfunc(0, 1, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q>1540 and q<1580:
                scf,sdf,sfele,sspeed = simfunc(1, 0, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q>1580 and q<1600:
                scf,sdf,sfele,sspeed = simfunc(3, 5, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q>1600 and q<1620:
                scf,sdf,sfele,sspeed = simfunc(5, 3, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1620 and q < 1700:
                scf,sdf,sfele,sspeed = simfunc(0, 2, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1700 and q < 1780:
                scf,sdf,sfele,sspeed = simfunc(2, 0, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1780 and q < 1800:
                scf,sdf,sfele,sspeed = simfunc(2, 5, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1800 and q < 1820:
                scf,sdf,sfele,sspeed = simfunc(5, 2, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1820 and q < 1850:
                scf,sdf,sfele,sspeed = simfunc(0, 5, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
            elif q >1850 and q < 1880:
                scf,sdf,sfele,sspeed = simfunc(5, 0, dummysfele, dummysspeed)
                sheetwr(sheet1,q,scf,sdf,sfele,sspeed)
        # Workbook save 
        elewb.save(f'{wb}.xls') 
        print("Data successfully generated!")
        if(wb in fnamelst):
            print("File name already exist! The data is overwritten.")
        else:
            fnamelst.append(wb)
        
def randomString():
    letters = string.ascii_lowercase
    return (''.join(random.choice(letters) for i in range(15)))


#Driver Function
nf = getinput('Enter the number of floors(excluding basements): ')
bf = getinput('Enter the number of basements (Enter 0 if none): ')
fnamelst = []
if(bf>0):        
    bf = 0-bf
heightdict = {}
    
for i in range(bf,0):
    bsheight = getinput(f'Enter the height of basement floor {i} (in ft): ')
    heightdict.update({f'{i}': bsheight})
    
for i in range(0,nf+1):
    tfheight = getinput(f'Enter the height of floor {i} (in ft): ')
    heightdict.update({f'{i}': tfheight})
                
ne = getinput('Enter the number of elevators: ')
elevator = []
for i in range(ne):     
    sfloorlst = []
    elevator.append('')  
    n = int(input(f'Enter the number of stops for Elevator {i+1}: '))
    g=0
    while(g == 0):
        if(n<=0):
            print('Invalid input!')
            n = int(input(f'Enter the number of stops for Elevator {i+1}: '))
        else:
            g=1
            sfloorlst = flstopfunc(n,i,nf,bf)
            
    curposele = getinput(f'Enter the current position of elevator {i+1}: ')
    while (curposele > nf or curposele < bf):
        curposele = int(input('Invalid floor! Please enter a valid position: '))           
    curdirele = input(f'Enter the direction of the elevator {i+1} (U for Up / D for Down / S for Static) :')
    while (curdirele.upper() != 'U' and curdirele.upper() != 'D' and curdirele.upper() != 'S'):
        curdirele = input('Invalid Direction! Please enter a valid direction: ')    
    while (curposele == nf and curdirele.upper() == 'U'):
        curdirele = input('Invalid Direction! Already in top floor! Please enter a valid direction: ')
    while (curposele == bf and curdirele.upper() == 'D'):
        curdirele = input('Invalid Direction! Already in bottom floor! Please enter a valid direction: ')
    curdirele = curdirele.upper()
    if(curdirele != 'S'):
        sf = int(input(f"Enter the elevator {i+1}'s destination floor(0 for Ground Floor): "))
        while ((sf > nf) or (sf < bf) or (sf not in sfloorlst)):
            sf = int(input('Invalid floor! Please enter a valid position: '))
        while ((curdirele.upper() == 'U') and (sf < curposele)):
            sf = int(input('Invalid destination! Please enter a floor higher than current floor: '))
        while ((curdirele.upper() == 'D') and (sf > curposele)):
            sf = int(input('Invalid destination! Please enter a floor lower than current floor: '))
    else:
        sf = curposele
    temp = 0
    while(temp == 0):
        try:
            speed = float(input(f'Enter the speed of Elevator {i+1} (in ft/sec): '))
            if(speed < 0):
                print('Speed cannot be negative!')
                continue
            temp = 1
        except:
                print('Please enter a valid number')
    elevator[i] = Elevator(i, curposele, curdirele, nf, bf, sf, sfloorlst, 'Y', speed)

def findele():    
    cf = int(input("Enter the user's position(0 for Ground Floor): "))
    while (cf > nf or cf < bf):
        cf = int(input('Invalid floor! Please enter a valid position: '))
    df = int(input("Enter the user's destination floor(0 for Ground Floor): "))
    while (df > nf or df < bf):
        df = int(input('Invalid floor! Please enter a valid Destination: '))
    distlst = []
    for i in range(ne):
        if((cf in elevator[i].elesflst) and (df in elevator[i].elesflst)):
            distlst.append(disfunc(cf, elevator[i].elecurpos, elevator[i].eledir, nf, 
                                       elevator[i].elesf, elevator[i].eleisactive, heightdict, elevator[i].clspeed))

        else:
            distlst.append(nf*3000)
    mini = min(distlst)
    if (mini < (nf*3000)):
        finalele = [i+1 for i,x in enumerate(distlst) if x == mini]
        print(f'Please use elevator #{finalele} to save time!')
    else:
        print('No elevators are availabe at the moment')            

findele()    



# Decision Tree Classification

def applyml(ipfilename):
    
    if(ipfilename == ''):
        print('Please enter a valid source file name')
    else:
        # Importing the dataset
        dataset = pd.read_csv(f'{ipfilename}')
        X = dataset.iloc[:, [0, 1]].values
        y = dataset.iloc[:, 2].values
        
        
        pdxdataset =pd.DataFrame({'0' : X[:,0], '1' : X[:,1]})
        
        pdxdataset.groupby(["0", "1"]).size()
        pdxdatasetfrequency = pdxdataset.groupby(["0", "1"]).size().reset_index(name="Time")
        maxtimes = pdxdatasetfrequency['Time'].max()
        maxtimessrc = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == maxtimes, '0'].iloc[0]
        maxtimesdest = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == maxtimes, '1'].iloc[0]
        
        
        print(f'Demand is predicted to be high at floor {maxtimessrc} to go to floor {maxtimesdest}')
        
            
        
        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)
        
        '''# Feature Scaling
        from sklearn.preprocessing import StandardScaler
        sc = StandardScaler()
        X_train = sc.fit_transform(X_train)
        X_test = sc.transform(X_test)'''
        
        # Fitting Decision Tree Classification to the Training set
        from sklearn.tree import DecisionTreeClassifier
        classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0)
        classifier.fit(X_train, y_train)
        
        # Predicting the Test set results
        y_pred = classifier.predict(X_test)
        
        y_predcustom = classifier.predict([[maxtimessrc,maxtimesdest]])
        
        y_predprint = y_predcustom[0]
        
        print(f'The speed of elevator {y_predprint + 1} which covers floor {maxtimessrc} and {maxtimesdest} is {elevator[y_predprint].clspeed}')
        
        mlspeedmin = elevator[y_predprint].clspeed
        higherspeedelelst = []
        for i in range(ne):
            if(i == y_predprint):
                pass
            else:
                if(elevator[i].clspeed > mlspeedmin):
                    higherspeedelelst.append(i)
                    
        for j in higherspeedelelst:
            print(f'Elevator {j+1} is operating at a rate of {elevator[j].clspeed}')
            
        mintimessrclst = []
        mintimesdestlst = []
        mintimes = pdxdatasetfrequency['Time'].min()
        mintimessrc = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == mintimes, '0']
        for j in range(len(mintimessrc)):
            temp = mintimessrc = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == mintimes, '0'].iloc[j]
            mintimessrclst.append(temp)
        mintimesdest = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == mintimes, '1']
        for j in range(len(mintimesdest)):
            temp = mintimesdest = pdxdatasetfrequency.loc[pdxdatasetfrequency['Time'] == mintimes, '1'].iloc[j]
            mintimesdestlst.append(temp)
            
        
        y_predcustomslowlst = []
    
        for k in range(len(mintimessrclst)):
            y_predcustomslow = classifier.predict([[mintimessrclst[k],mintimesdestlst[k]]])
            temp = y_predcustomslow[0]
            y_predcustomslowlst.append(temp)
            
        y_predcustomslowset =  set(y_predcustomslowlst)
        for ele in y_predcustomslowset:
            print(f'Elevator {ele+1} which covers floor "{elevator[ele].elesflst}" has low demand ')
            
        
        
        '''# Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix
        cm = confusion_matrix(y_test, y_pred)'''

    

#Application
window = Tk() 
window.title("Welcome to Elevator Simulator") 
window.geometry('900x900')

combo = Combobox(window)
combo['values']= appvalues(ne) 
combo.grid(column=1, row=0)

schmbtn = Button(window, text="Schedule Maintenance", command = lambda: schmfunc(int(combo.get())-1))
schmbtn.grid(column=0, row=1)

compmbtn = Button(window, text="Complete Maintenance", command = lambda: compmfunc(int(combo.get())-1)) 
compmbtn.grid(column=2, row=1)

emergencybtn = Button(window, text="Emergency", command = lambda: emergfunc(int(combo.get())-1,nf)) 
emergencybtn.grid(column=0, row=2)

pfbtn = Button(window, text="Power Failure", command = lambda: pffunc(ne)) 
pfbtn.grid(column=2, row=2)

pffixbtn = Button(window, text="Power Problem Solved!", command = lambda: pffixfunc(ne))
pffixbtn.grid(column=0, row=3)

showeleposbtn = Button(window, text="Show Elevator Positions", command = lambda: showpos(ne))
showeleposbtn.grid(column=2, row=3)

simulatebtn = Button(window, text ="Simulate!", command = lambda: simcompfunc())
simulatebtn.grid(column=1, row=4)

useappbtn = Button(window, text="Find Nearest Elevator", command = lambda: findele())
useappbtn.grid(column=1, row=5)

Label(window, text='Enter File Name').grid(column=0,row=7)
e1 = Entry(window)
e1.grid(column=2, row=7) 

gendatabtn = Button(window,text="Generate Data", command = lambda: gendata(e1.get()))
gendatabtn.grid(column=1, row=8)

Label(window, text='Enter the source file name for ML followed by .csv').grid(column=0,row=9)
e2 = Entry(window)
e2.grid(column=2, row=9)

applymlbtn = Button(window, text="Apply ML", command = lambda: applyml(e2.get()))
applymlbtn.grid(column=1, row =10)

 
window.mainloop()
    

