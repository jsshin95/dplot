import tkinter as tk
import tkinter.ttk
import pandas as pd
from datetime import datetime
from tkinter import messagebox
import csv
import os
from PIL import ImageGrab
import numpy as np
from tkinter import filedialog

def isNan(value):
    return value != value

def btnLoadClick():

    def OnSelect(event):
        widget=event.widget
        index=int(widget.curselection()[0])
        
        canvas.delete(tk.ALL)

        cp=0
        cf=0
        cm=0
        for i in range(31):
            for j in range(128):
                if A[index][i][j]=='P':
                    if CheckLine.get()==1: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='blue', outline='white')
                    else: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='blue')
                    cp+=1
                elif A[index][i][j]=='F':
                    if CheckLine.get()==1: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='red', outline='white')
                    else: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='red')
                    cf+=1
                elif A[index][i][j]=='M':
                    if CheckLine.get()==1: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='gray', outline='white')
                    else: canvas.create_polygon(j*7,i*7, (j+1)*7,i*7, (j+1)*7,(i+1)*7, j*7,(i+1)*7, fill='gray')
                    cm+=1
        
        label_total.place(x=45, y=380, width=200, height=20)
        label_blue.place(x=30, y=410, width=10, height=10)
        label_red.place(x=30, y=435, width=10, height=10)
        label_gray.place(x=30, y=460, width=10, height=10)
        label_pass.config(text='PASS : '+str(cp))
        label_fail.config(text='FAIL : '+str(cf))
        label_miss.config(text='MISS : '+str(cm))
        label_pass.place(x=45, y=405, width=200, height=20)
        label_fail.place(x=45, y=430, width=200, height=20)
        label_miss.place(x=45, y=455, width=200, height=20)


    df0=[]
    df1=[]
    del df0[0:]
    del df1[0:]

    for i in range(1,5):
        for j in range(1,9):
            try:
                df0.append(pd.read_csv(label_filename_R0['text'][:-7]+str(i)+str(j)+'1.csv'))
                len_row=len(df0[-1].index)
                if cb_input_type.get()=='type1':
                    if i==1:
                        if len_row<113:
                            for _ in range(113-len_row):
                                df0[-1].loc[len(df0[-1].index)]=pd.Series([np.nan]*9, index=df0[-1].columns)
                    else:
                        if len_row<129:
                            for _ in range(129-len_row):
                                df0[-1].loc[len(df0[-1].index)]=pd.Series([np.nan]*9, index=df0[-1].columns)
                elif cb_input_type.get()=='type2':
                    if i==1:
                        if len_row<224:
                            for _ in range(224-len_row):
                                df0[-1].loc[len(df0[-1].index)]=pd.Series([np.nan]*13, index=df0[-1].columns)
                    else:
                        if len_row<256:
                            for _ in range(256-len_row):
                                df0[-1].loc[len(df0[-1].index)]=pd.Series([np.nan]*13, index=df0[-1].columns)
            except:
                messagebox.showwarning(title="error (input : R0)", message="failed to open "+label_filename_R0['text'][:-7]+str(i)+str(j)+'1.csv')
                return
            
            try:
                df1.append(pd.read_csv(label_filename_R1['text'][:-7]+str(i)+str(j)+'1.csv'))
                len_row=len(df1[-1].index)
                if cb_input_type.get()=='type1':
                    if i==1:
                        if len_row<113:
                            for _ in range(113-len_row):
                                df1[-1].loc[len(df1[-1].index)]=pd.Series([np.nan]*9, index=df1[-1].columns)
                    else:
                        if len_row<129:
                            for _ in range(129-len_row):
                                df1[-1].loc[len(df1[-1].index)]=pd.Series([np.nan]*9, index=df1[-1].columns)
                elif cb_input_type.get()=='type2':
                    if i==1:
                        if len_row<224:
                            for _ in range(224-len_row):
                                df1[-1].loc[len(df1[-1].index)]=pd.Series([np.nan]*13, index=df1[-1].columns)
                    else:
                        if len_row<256:
                            for _ in range(256-len_row):
                                df1[-1].loc[len(df1[-1].index)]=pd.Series([np.nan]*13, index=df1[-1].columns)
            except:
                messagebox.showwarning(title="error (input : R1)", message="failed to open "+label_filename_R1['text'][:-7]+str(i)+str(j)+'1.csv')
                return

    os.chdir(cwd)
    
    if os.path.exists('Rshift result')==False:
        try:
            os.mkdir('Rshift result')
        except:
            messagebox.showwarning(title="error", message="failed to create the result folder")
            return

    now=datetime.now()
    time=now.strftime("%Y%m%d_%H%M%S")

    if os.path.exists('Rshift result/'+time)==False:
        try:
            os.mkdir('Rshift result/'+time)
        except:
            messagebox.showwarning(title="error", message="failed to create directory")
            return
    
    os.chdir('Rshift result/'+time)

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
        #temp.append('')
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
        #temp.append('Spec IN/OUT')
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
                            if cb_input_type.get()=='type1':
                                temp.append(df0[j-1].iloc[n*16+m+1].values[k]) #R0
                                temp.append(df1[j-1].iloc[n*16+m+1].values[k]) #R1
                            elif cb_input_type.get()=='type2':
                                temp.append(df0[j-1].iloc[2*n*16+2*m+1].values[k+4]) #R0
                                temp.append(df1[j-1].iloc[2*n*16+2*m+1].values[k+4]) #R1
                            else:
                                messagebox.showwarning(title="error", message="type error")
                                return
                            
                            if (k<2)|(k==6)|(k==8): 
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append(float(temp[-1])-float(temp[-2])) #R1-R0

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<5: temp.append('IN') #R0<50 -> Rshift<5 PASS
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                            else:
                                if isNan(temp[-1])|isNan(temp[-2]): temp.append('MISS')
                                else: temp.append((float(temp[-1])/float(temp[-2])-1)*100) #(R1/R0-1)*100 [%]

                                if temp[-1]=='MISS':
                                    temp.append('MISS')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:])
                                elif abs(float(temp[-1]))<10: temp.append('IN') #R0>=50 -> Rshift<10% PASS
                                else:
                                    temp.append('OUT')
                                    writer2.writerow(temp[0:3]+[k+1]+temp[-4:-2]+[str(temp[-2])+'%']+[temp[-1]])
                            
                            if n%2==0: # -->
                                if temp[-1]=='IN': A[k][(6-n)*4 + i - 1][m*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(6-n)*4 + i - 1][m*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(6-n)*4 + i - 1][m*8 + 8-j]='M'
                            elif n%2==1: # <--
                                if temp[-1]=='IN': A[k][(6-n)*4 + i - 1][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(6-n)*4 + i - 1][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(6-n)*4 + i - 1][(15-m)*8 + 8-j]='M'
                            
                            temp.pop()

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
                            if cb_input_type.get()=='type1':
                                temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            elif cb_input_type.get()=='type2':
                                temp.append(df0[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R1
                            else:
                                messagebox.showwarning(title="error", message="type error")
                                return
                            
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
                            if n==0:
                                if temp[-1]=='IN': A[k][28][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][28][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][28][(15-m)*8 + 8-j]='M'
                            elif n%2==0: # <--
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='M'
                            elif n%2==1: # -->
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='M'
                            
                            temp.pop()

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
                            if cb_input_type.get()=='type1':
                                temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            elif cb_input_type.get()=='type2':
                                temp.append(df0[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R1
                            else:
                                messagebox.showwarning(title="error", message="type error")
                                return
                            
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
                            if n==0:
                                if temp[-1]=='IN': A[k][29][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][29][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][29][(15-m)*8 + 8-j]='M'
                            elif n%2==0: # <--
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='M'
                            elif n%2==1: # -->
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='M'
                            
                            temp.pop()

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
                            if cb_input_type.get()=='type1':
                                temp.append(df0[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[n*16+m+1].values[k]) #R1
                            elif cb_input_type.get()=='type2':
                                temp.append(df0[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R0
                                temp.append(df1[(i-1)*8+j-1].iloc[2*n*16+2*m+1].values[k+4]) #R1
                            else:
                                messagebox.showwarning(title="error", message="type error")
                                return
                            
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
                            if n==0:
                                if temp[-1]=='IN': A[k][30][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][30][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][30][(15-m)*8 + 8-j]='M'
                            elif n%2==0: # <--
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][(15-m)*8 + 8-j]='M'
                            elif n%2==1: # -->
                                if temp[-1]=='IN': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='P'
                                elif temp[-1]=='OUT': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='F'
                                elif temp[-1]=='MISS': A[k][(7-n)*4 + i - 1][m*8 + 8-j]='M'
                            
                            temp.pop()

                        writer.writerow(temp)
    
    f.close()
    fmo.close()

    for i in range(31):
        for j in range(128):
            result='P'
            for k in range(9):
                if A[k][i][j]=='M': result='M'
            for k in range(9):
                if A[k][i][j]=='F': result='F'
            A[9][i][j]=result


    lb.delete(0,tk.END)
    for i in range(9):
        lb.insert(i, str(i+1))
    lb.insert(9, 'total')
    
    lb.bind("<<ListboxSelect>>", OnSelect)
    checkbutton.place(x=950, y=120, width=80, height=20)
    button_capture.place(x=860,y=115,width=60,height=25)
      
    return

def capture():
    x1=win.winfo_rootx()*1.25 + 25*1.25
    y1=win.winfo_rooty()*1.25 + 150*1.25
    x2=x1 + 896*1.25
    y2=y1 + 217*1.25
    box=(x1,y1,x2,y2)
    img=ImageGrab.grab(box)
    if lb.curselection()[0]==9: img.save('total.png')
    else: img.save(str(lb.curselection()[0]+1)+'.png')

def btnFnR0Click():
    try:
        fi_temp=filedialog.askopenfilename(title = 'select input file (R0)', filetypes=(('*.csv','*csv'),))
        R0_dir=fi_temp[:-7]
    except:
        messagebox.showwarning(title="error", message="failed to load input file (R0)")
        return
    label_filename_R0.config(text=R0_dir+'xx1.csv')

def btnFnR1Click():
    try:
        fi_temp=filedialog.askopenfilename(title = 'select input file (R1)', filetypes=(('*.csv','*csv'),))
        R1_dir=fi_temp[:-7]
    except:
        messagebox.showwarning(title="error", message="failed to load input file (R1)")
        return
    label_filename_R1.config(text=R1_dir+'xx1.csv')


A=[[['' for _ in range(128)] for _ in range(31)] for _ in range(10)]
cwd=os.getcwd()

win=tk.Tk()
win.geometry('1200x600+100+100')
win.title("Rshift ver.1.1.")

canvas=tk.Canvas(win, relief="solid", bg="white")
canvas.place(x=25,y=150,width=128*7,height=31*7)

lb=tk.Listbox(win)
lb.place(x=950, y=150, width=80, height=400)

label_input_type=tk.Label(win, text="input type : ")
label_input_type.place(x=10,y=10,width=90,height=25)

cb_input_type=tk.ttk.Combobox(win, height=25, values=['type1','type2'], state='readonly')
cb_input_type.place(x=105,y=10,width=80,height=25)


button_fnR0=tk.Button(win,text="R0 파일 선택 ",command=btnFnR0Click)
button_fnR1=tk.Button(win,text="R1 파일 선택 ",command=btnFnR1Click)
label_filename_R0=tk.Label(win, text='')
label_filename_R1=tk.Label(win, text='')
label_csv0=tk.Label(win,text='xx1.csv')
label_csv1=tk.Label(win,text='xx1.csv')

button_fnR0.place(x=10,y=50,width=150,height=25)
button_fnR1.place(x=10,y=80,width=150,height=25)

label_filename_R0.place(x=160,y=50,width=390,height=25)
label_filename_R1.place(x=160,y=80,width=390,height=25)

button_load=tk.Button(win,text="load",command=btnLoadClick)
button_load.place(x=560,y=60,width=80,height=30)

label_total=tk.Label(win, text='TOTAL : 3968', anchor='w') #128*31=3968
label_blue=tk.Label(win, bg='blue')
label_red=tk.Label(win, bg='red')
label_gray=tk.Label(win, bg='gray')
label_pass=tk.Label(win, anchor='w')
label_fail=tk.Label(win, anchor='w')
label_miss=tk.Label(win, anchor='w')

button_capture=tk.Button(win, text='capture', command=capture)

CheckLine=tk.IntVar()
checkbutton=tk.Checkbutton(win, text='outline', variable=CheckLine)

win.mainloop()
