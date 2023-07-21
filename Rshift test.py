import tkinter as tk
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import csv

def isNan(value):
    return value != value

def btnLoadClick():
    folderR0=entry_folderR0.get()
    folderR1=entry_folderR1.get()
    fileR0=entry_fileR0.get()
    fileR1=entry_fileR1.get()

    df0=[]
    df1=[]
    del df0[0:]
    del df1[0:]

    for i in range(1,5):
        for j in range(1,9):
            try:
                df0.append(pd.read_csv(folderR0+'/'+fileR0+str(i)+str(j)+'1.csv'))
            except:
                messagebox.showwarning(title="error (input : R0)", message="failed to open "+folderR0+'/'+fileR0+str(i)+str(j)+'1.csv')
                return
            try:
                df1.append(pd.read_csv(folderR1+'/'+fileR1+str(i)+str(j)+'1.csv'))
            except:
                messagebox.showwarning(title="error (input : R1)", message="failed to open "+folderR1+'/'+fileR1+str(i)+str(j)+'1.csv')
                return
    
    now=datetime.now()
    time=now.strftime("%Y%m%d_%H%M%S")

    try:
        f=open(time+'_output.csv','w',newline='')
    except:
        messagebox.showwarning(title="error (output)", message="failed to open output file")
        return
    
    try:
        fmo=open(time+'_missout.csv','w',newline='')
    except:
        messagebox.showwarning(title="error (MISS/OUT)", message="failed to open MISS/OUT file")
        return
    
    writer=csv.writer(f)
    writer2=csv.writer(fmo)
    
    temp=[]
    del temp[0:]
    for i in range(3):
        temp.append('')
    for i in range(1,10):
        temp.append(str(i))
        temp.append('')
        temp.append('')
        temp.append('')
    writer.writerow(temp)
    
    del temp[0:]
    temp.append('file명')
    temp.append('step')
    temp.append('Design')
    for i in range(9):
        temp.append('R0')
        temp.append('R1')
        if i<2: temp.append('R1-R0')
        elif i==6: temp.append('R1-R0')
        elif i==8: temp.append('R1-R0')
        else: temp.append('R1-R0 [%]')
        temp.append('Spec IN/OUT')
    writer.writerow(temp)

    writer2.writerow(['file명','step','Design','No.','R0','R1','R1-R0','Spec IN/OUT'])


    for i in range(1,5):
        for j in range(1,9):
            
            if i==1:
                for n in range(7):
                    for m in range(16):
                        del temp[0:]
                        temp.append(str(i)+str(j)+'1') #file명
                        temp.append((n+1)*16+m+1) #step
                        if n==0: temp.append(5)  #design
                        elif n==6: temp.append(1)
                        else: temp.append(n)
                        for k in range(9):
                            temp.append(df0[j-1].iloc[n*16+m+1].values[k]) #R0
                            temp.append(df1[j-1].iloc[n*16+m+1].values[k]) #R1
                            if (k<2)|(k==6)|(k==8):
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append(float(temp[-1])-float(temp[-2])) #R1-R0

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<5: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                            else:
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append((float(temp[-1])/float(temp[-2])-1)*100) #(R1/R0-1)*100 [%]

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<10: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:-2]+[str(temp[-2])+'%']+[temp[-1]])
                        writer.writerow(temp)
            elif i==2:
                for n in range(8):
                    for m in range(16):
                        del temp[0:]
                        temp.append(str(i)+str(j)+'1') #file명
                        temp.append(n*16+m+1) #step
                        if n==0: temp.append(4)  #design
                        elif n>=6: temp.append(n-5)
                        else: temp.append(n)
                        for k in range(9):
                            temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                            temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            if (k<2)|(k==6)|(k==8):
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append(float(temp[-1])-float(temp[-2])) #R1-R0

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<5: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                            else:
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append((float(temp[-1])/float(temp[-2])-1)*100) #(R1/R0-1)*100 [%]

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<10: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:-2]+[str(temp[-2])+'%']+[temp[-1]])
                        writer.writerow(temp)
            elif i==3:
                for n in range(8):
                    for m in range(16):
                        del temp[0:]
                        temp.append(str(i)+str(j)+'1') #file명
                        temp.append(n*16+m+1) #step
                        if n==0: temp.append(5)  #design
                        elif n>=5: temp.append(n-4)
                        else: temp.append(n+1)
                        for k in range(9):
                            temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                            temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            if (k<2)|(k==6)|(k==8):
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append(float(temp[-1])-float(temp[-2])) #R1-R0

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<5: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                            else:
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append((float(temp[-1])/float(temp[-2])-1)*100) #(R1/R0-1)*100 [%]

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<10: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:-2]+[str(temp[-2])+'%']+[temp[-1]])
                        writer.writerow(temp)
            elif i==4:
                for n in range(8):
                    for m in range(16):
                        del temp[0:]
                        temp.append(str(i)+str(j)+'1') #file명
                        temp.append(n*16+m+1) #step
                        if n==0: temp.append(1)  #design
                        elif n>=4: temp.append(n-3)
                        else: temp.append(n+2)
                        for k in range(9):
                            temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                            temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            if (k<2)|(k==6)|(k==8):
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append(float(temp[-1])-float(temp[-2])) #R1-R0

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<5: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                            else:
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append((float(temp[-1])/float(temp[-2])-1)*100) #(R1/R0-1)*100 [%]

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<10: temp.append('IN')
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:-2]+[str(temp[-2])+'%']+[temp[-1]])
                        writer.writerow(temp)
    
    
    f.close()
    fmo.close()
    return


win=tk.Tk()
win.geometry('700x200+150+350')
win.title("Rshift test")

label_fnR0=tk.Label(win,text="R0 폴더명 / 파일명 :")
label_fnR1=tk.Label(win,text="R1 폴더명 / 파일명 :")
entry_folderR0=tk.Entry(win)
entry_folderR1=tk.Entry(win)
label_slash0=tk.Label(win,text="/")
label_slash1=tk.Label(win,text="/")
entry_fileR0=tk.Entry(win)
entry_fileR1=tk.Entry(win)
label_csv0=tk.Label(win,text='111.csv')
label_csv1=tk.Label(win,text='111.csv')

label_fnR0.place(x=10,y=50,width=150,height=25)
label_fnR1.place(x=10,y=80,width=150,height=25)

entry_folderR0.place(x=160,y=50,width=120,height=25)
entry_folderR1.place(x=160,y=80,width=120,height=25)

label_slash0.place(x=280,y=50,width=20,height=25)
label_slash1.place(x=280,y=80,width=20,height=25)

entry_fileR0.place(x=300,y=50,width=200,height=25)
entry_fileR1.place(x=300,y=80,width=200,height=25)

label_csv0.place(x=500,y=50,width=50,height=25)
label_csv1.place(x=500,y=80,width=50,height=25)

button_load=tk.Button(win,text="load",command=btnLoadClick)
button_load.place(x=560,y=60,width=80,height=30)


win.mainloop()