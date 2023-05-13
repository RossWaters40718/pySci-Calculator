import tkinter as tk
from tkinter import *
from tkinter.scrolledtext import ScrolledText
from tkinter import ttk, font, messagebox, Menu, colorchooser, Frame, simpledialog
from tkfontchooser import askfont
from win32api import GetMonitorInfo, MonitorFromPoint
import pathlib
import os
import re as reo
import mpmath as mp
from mpmath import *
import numpy as np
import sympy as sym
from sympy import *
import configparser
class XY_Scrollbars(tk.Frame):
    def __init__(self, parent, hgt, wid):
        super().__init__(parent)
        style=ttk.Style()
        style.theme_use('classic')
        # Pad X And Y Using Percent Of Width And Height 
        pad_10x=int(wid*0.0305)
        pad_20x=int(wid*0.061)
        pad_10y=int(hgt*0.0157)
        pad_20y=int(hgt*0.0313)
        self.canvas = tk.Canvas(self, width=wid, height=hgt, border=2, relief="sunken",bg='#f3f6f4')
        style.configure("Vertical.TScrollbar", background='#048c8c', bordercolor='#444444', arrowcolor='#2986cc')
        self.vbar=ttk.Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.vbar.pack(side=RIGHT,fill=Y,padx=(2,2),pady=(pad_10y,pad_20y))                                        
        style.configure("Horizontal.TScrollbar", background='#048c8c', bordercolor='#444444', arrowcolor='#2986cc')
        self.hbar=ttk.Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        self.hbar.pack(side=BOTTOM,fill=X,padx=(pad_20x,pad_10x),pady=(2,2))                                        
        self.canvas.pack(side=TOP, anchor=NW, fill=BOTH, expand=True, padx=(pad_10x,0), pady=(0,0))
        self.window=tk.Frame(self.canvas,width=wid, height=hgt, bg='#f3f6f4')
        self.window.pack(side=TOP,anchor=NW,fill=BOTH, expand=True, padx=(0,0), pady=(0,0))                     
        self.canvas.configure(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)                          
        self.canvas_window=self.canvas.create_window((0,0),window=self.window,anchor=NW, tags="self.window") 
        # Bind canvas And Scroll Window To Events                
        self.canvas.bind("<Key-Prior>", self.page_up)
        self.canvas.bind("<Key-Next>", self.page_down)
        self.canvas.bind("<Key-Up>", self.unit_up)
        self.canvas.bind("<Key-Down>", self.unit_down)        
        self.canvas.bind("<Key-Left>", self.unit_left)
        self.canvas.bind("<Key-Right>", self.unit_right)        
        self.window.bind("<Configure>", self.rst_frame)                       
        self.window.bind('<Enter>', self.inside_canvas)                                 
        self.window.bind('<Leave>', self.outside_canvas)                                 
        self.rst_frame(None)
    def rst_frame(self, event):                                              
        self.canvas.configure(scrollregion=self.canvas.bbox(ALL))
    def unit_up(self, event):
        self.canvas.yview_scroll(-1, "unit")
        return "break"
    def unit_down(self, event):
        self.canvas.yview_scroll(1, "unit")
        return "break"
    def unit_left(self, event):
        self.canvas.xview_scroll(-1, "unit")
        return "break"
    def unit_right(self, event):
        self.canvas.xview_scroll(1, "unit")
        return "break"
    def page_up(self, event):
        self.canvas.yview_scroll(-1, "page")
        return "break"
    def page_down(self, event):
        self.canvas.yview_scroll(1, "page")
        return "break"
    def scroll_mousey(self, event):
        self.canvas.yview_scroll(int(-1* (event.delta/120)), 'units')
    def inside_canvas(self, event):                                                       
        self.canvas.focus_set()                                                 
        self.canvas.bind_all("<MouseWheel>", self.scroll_mousey)
    def outside_canvas(self, event):                                                       
        self.canvas.unbind_all("<MouseWheel>")
class Ratio_Calculator:
    def __init__(self):
        def ratio_resize(event):
            if self.state()=='zoomed':
                txtfont.config(size=24)
                ratiofont.config(size=30)
                formulafont.config(size=18)
                btnfont.config(size=20)
            else:    
                txtfont.config(size=12)
                ratiofont.config(size=16)
                formulafont.config(size=9)
                btnfont.config(size=10)
            return
        def ratio_destroy():# X Icon Was Clicked
            for widget in self.winfo_children():
                if isinstance(widget, tk.Canvas):widget.destroy()
                else:widget.destroy()
            self.withdraw()
            if Window_State.get()=='zoomed':root.state('zoomed')
            root.deiconify()
            root.grab_set()
            root.focus_force()
            root.update()
        def validate_Entries(string):# Allow Only Numeric values, negative sign and decimal point for Entry Widgets
            result=reo.match(r"^[-,]?\d*[.,]?\d*$", string) # Float With Sign
            return (string == "" or (string.count('-') <= 1 and string.count('.') <= 1
                and result is not None and result.group(0) != ""))
        def on_validate(P):return validate_Entries(P)
        def clear_entries():# Clears all text from Entry widgets
            a1_txtbx.config(state='normal') 
            a2_txtbx.config(state='normal') 
            b1_txtbx.config(state='normal') 
            b2_txtbx.config(state='normal')
            a1_txtbx.delete('0',tk.END)
            a2_txtbx.delete('0',tk.END)
            b1_txtbx.delete('0',tk.END)
            b2_txtbx.delete('0',tk.END)
            a3_txtbx.delete('0',tk.END)
            b3_txtbx.delete('0',tk.END)
            a4.set('')
            b4.set('')
            formula_txtbx.delete('1.0',tk.END)
            self.focus_force()
            a1_txtbx.focus_force()
        def calculate_ratio(a_1,a_2,b_1,b_2,a_3,b_3):
            try:
                count=0
                missing_ratio=''
                exist=a_1.get()
                if len(exist) != 0:
                    a_1=float(a_1.get())
                    count+=1
                else: missing_ratio='a1'
                exist=a_2.get()
                if len(exist) != 0:
                    a_2=float(a_2.get())
                    count+=1
                else: missing_ratio='a2'
                exist=b_1.get()
                if len(exist) != 0:
                    b_1=float(b_1.get())
                    count+=1
                else: missing_ratio='b1'
                exist=b_2.get()
                if len(exist) != 0:
                    b_2=float(b_2.get())
                    count+=1
                else: missing_ratio='b2'
                if count < 3:
                    messagebox.showerror('INFORMATION', 'A Minimum Of 3 Variables Are Required For Calculations And '\
                            'You Have Only Entered '  + str(count) + '. Please Enter The Missing Variable/s.')
                if count == 3: # count=3, find & calculate missing ratio value
                    if default_text.get():
                        formula_txtbx.delete('1.0',tk.END)
                        default_text.set(False)
                    if missing_ratio == 'a1':
                        zero_exist=div_by_zero(b2_txtbx, b_2, 'B2') # Prohibit Division by Zero
                        if zero_exist: return
                        tmpstr=(b_1 * a_2) / b_2 #a1=(b1 * a2) / b2, where b2 != 0
                        formula_txtbx.delete('1.0',tk.END)
                        formula=(f"A1 = (B1 * A2) / B2 = ({b_1} * {a_2}) / {b_2} = {tmpstr}\n")    
                        formula_txtbx.insert('1.0', formula)
                        update_ratio(a1_txtbx,tmpstr)
                        a_1=tmpstr
                        count+=1
                    elif missing_ratio == 'a2':
                        zero_exist=div_by_zero(b1_txtbx, b_1, 'B1') # Prohibit Division by Zero
                        if zero_exist: return
                        tmpstr=(a_1 / b_1) * b_2 #a2=(a1 / b1) * b2, where b1 != 0
                        formula_txtbx.delete('1.0',tk.END)
                        formula=(f"A2 = (A1 / B1) * B2 = ({a_1} / {b_1}) * {b_2} = {tmpstr}\n")    
                        formula_txtbx.insert('1.0', formula)
                        update_ratio(a2_txtbx,tmpstr)
                        a_2=tmpstr
                        count+=1
                    elif missing_ratio == 'b1':
                        zero_exist=div_by_zero(a2_txtbx, a_2, 'A2') # Prohibit Division by Zero
                        if zero_exist: return
                        tmpstr=(a_1 * b_2) / a_2 #b1=(a1 * b2) / a2, where a2 != 0
                        formula_txtbx.delete('1.0',tk.END)
                        formula=(f"B1 = (A1 * B2) / A2 = ({a_1} * {b_2}) / {a_2} = {tmpstr}\n")    
                        formula_txtbx.insert('1.0', formula)
                        update_ratio(b1_txtbx,tmpstr)
                        b_1=tmpstr
                        count+=1
                    elif missing_ratio == 'b2':
                        zero_exist=div_by_zero(a1_txtbx, a_1, 'A1') # Prohibit Division by Zero
                        if zero_exist: return
                        tmpstr=(b_1 * a_2) / a_1 #b2=(b1 * a2) / a1, where a1 != 0
                        formula_txtbx.delete('1.0',tk.END)
                        formula=(f"B2 = (B1 * A2) / A1 = ({b_1} * {a_2}) / {a_1} = {tmpstr}\n")    
                        formula_txtbx.insert('1.0', formula)
                        update_ratio(b2_txtbx,tmpstr)
                        b_2=tmpstr
                        count+=1
                    default_text.set(False)
                if count == 4: # All ratio value present, examine for porportion values
                    if default_text.get():
                        formula_txtbx.delete('1.0',tk.END)
                        default_text.set(False)
                    exist=a_3.get()
                    if(len(exist) != 0): a_3=float(a_3.get())
                    exist=b_3.get()
                    if(len(exist) != 0): b_3=float(b_3.get())
                    # Check for ratio inversions
                    if a_1 > a_2: a_inverse=True
                    else: a_inverse=False
                    if b_1 > b_2: b_inverse=True
                    else: b_inverse=False
                    # Set inversion true or false for calculations
                    if a_inverse and not b_inverse: inverse=True
                    if not a_inverse and b_inverse: inverse=True
                    if not a_inverse and not b_inverse: inverse=False
                    if a_inverse and b_inverse: inverse=False
                    # Get the numerical sizes of the ratios for K-Factor calculations
                    if(a_1 >= 0) and (a_2 > 0):
                        asize=abs(a_2 - a_1)
                        bsize=abs(b_1 - b_2)
                    elif(b_1 > 0) and (b_2 >= 0):
                        asize=abs(a_1 - a_2)
                        bsize=abs(b_2 - b_1)
                    else:
                        asize=abs(a_1 - a_2) #0,-100 or -10,-100 Examples
                        bsize=abs(b_1 - b_2) #0,-100 or 10,-100
                    # Calculate the K=Factors using the sizes
                    Kfactor_ba=round(abs(bsize / asize),7) #X Amount Of B's Per X Amount Of A's
                    KDisplay_ba="K = Abs(B range / A range)"
                    Kfactor_ab=round(abs(asize / bsize),7) #X Amount Of A's Per X Amount Of B's
                    KDisplay_ab="K = Abs(A range / B range)"
                    # Final Calculations
                    if inverse == False: # Case Not A_Inverse And Not B_Inverse Or A_Inverse And B_Inverse
                        exist=a3.get()
                        if len(exist) != 0:# B=B1 - (K * (A1 - A))
                            a_3=float(a3.get())
                            formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                            formula_txtbx.insert('2.0', formula)
                            b_4=round(b_1 - (Kfactor_ba * (a_1 - a_3)), 3)
                            formula=(f"B = B1 - (K * (A1 - A)) = {b_1} - ({Kfactor_ba} * ({a_1} - {a_3})) = {b_4}\n")
                            formula_txtbx.insert('3.0', formula)
                            b4.set(b_4)
                        exist=b3.get()
                        if len(exist) != 0:# A=A1 - (K * (B1 - B))
                            b_3=float(b3.get())
                            formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                            formula_txtbx.insert('4.0', formula)
                            a_4=round(a_1 - (Kfactor_ab * (b_1 - b_3)), 3) 
                            formula=(f"A = A1 - (K * (B1 - B)) = {a_1} - ({Kfactor_ab} * ({b_1} - {b_3})) = {a_4}\n")
                            formula_txtbx.insert('5.0', formula)
                            a4.set(a_4)
                    else: # Case A_Inverse And Not B_Inverse Or Not A_Inverse And B_Inverse
                        exist=a3.get()
                        if len(exist) != 0:# B=B1 - ((A - A1) * K)
                            a_3=float(a3.get())
                            formula=(f"{KDisplay_ba}={bsize} / {asize}={Kfactor_ba}\n")
                            formula_txtbx.insert('2.0', formula)
                            b_4=round(b_1 - ((a_3 - a_1) * Kfactor_ba), 3)
                            formula=(f"B = B1 - ((A - A1) * K) = {b_1} - (({a_3} - {a_1}) * {Kfactor_ba}) = {b_4}\n")
                            formula_txtbx.insert('3.0', formula)
                            b4.set(b_4)
                        exist=b3.get()
                        if len(exist) != 0:# A=A1 - ((B - B1) * K)
                            b_3=float(b3.get())
                            formula=(f"{KDisplay_ab}={asize} / {bsize}={Kfactor_ab}\n")
                            formula_txtbx.insert('4.0', formula)
                            a_4=round(a_1 - ((b_3 - b_1) * Kfactor_ab), 3) 
                            formula=(f"A = A1 - ((B - B1) * K) = {a_1} - (({b_3} - {b_1}) * {Kfactor_ab}) = {a_4}\n")
                            formula_txtbx.insert('5.0', formula)
                            a4.set(a_4)
            except Exception as e:
                msg1='Exception occurred while code execution:\n'
                msg2= repr(e)+'calculate_ratio'
                messagebox.showerror('Exeption Error', msg1+msg2)
        def div_by_zero(widget_name, value, focused):
            if value == 0:# Prohibit Division By Zero, Set Focus On Entry Widget
                messagebox.showerror('Entry Error!', 'Division By Zero! Please Change '+ focused + ' Value!')
                widget_name.delete(0,"end")
                widget_name.focus_set()   
                return True
            else: return False
        def update_ratio(widget_name, new_value):
            widget_name.delete(0,"end")
            widget_name.insert(0, new_value)
            widget_name.focus_set()
        def validate_keyboard(string):# Allow Only Numeric values, negative sign and decimal point for Entry Widgets
            result=reo.match(r"^[-,]?\d*[.,]?\d*$", string) # Signed Float
            if result==None:return ''
            else:return string    
        def keyboard(event):
            f=focused.get()
            txt=event.widget["text"]
            if txt!='Backspace':
                if f=='A1':
                    txt=a1.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':a1.set(txt)
                elif f=='A2':
                    txt=a2.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':a2.set(txt)
                elif f=='B1':
                    txt=b1.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':b1.set(txt)
                elif f=='B2':
                    txt=b2.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':b2.set(txt)
                elif f=='A3':
                    txt=a3.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':a3.set(txt)
                elif f=='B3':
                    txt=b3.get()+event.widget["text"]
                    val=validate_keyboard(txt)
                    if val!='':b3.set(txt)
            else:        
                if f=='A1':
                    txt=a1.get()
                    txt=txt[:-1]
                    a1.set(txt)
                elif f=='A2':
                    txt=a2.get()
                    txt=txt[:-1]
                    a2.set(txt)
                elif f=='B1':
                    txt=b1.get()
                    txt=txt[:-1]
                    b1.set(txt)
                elif f=='B2':
                    txt=b2.get()
                    txt=txt[:-1]
                    b2.set(txt)
                elif f=='A3':
                    txt=a3.get()
                    txt=txt[:-1]
                    a3.set(txt)
                elif f=='B3':
                    txt=b3.get()
                    txt=txt[:-1]
                    b3.set(txt)
        def keyboard_focus(event, widget):
            if widget=='A1':a1_txtbx.focus_force()
            elif widget=='A2':a2_txtbx.focus_force()
            elif widget=='B1':b1_txtbx.focus_force()
            elif widget=='B2':b2_txtbx.focus_force()
            elif widget=='A3':a3_txtbx.focus_force()
            elif widget=='B3':b3_txtbx.focus_force()
            focused.set(widget)
            return("break")            
        self=Toplevel(root)# Displays The ratio Window
        root.withdraw()
        self.deiconify()
        self.grab_set() # Receive Events And Prevent root Window Interaction
        self.title('Ratio / Porportion Calculator')
        monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
        work_area = monitor_info.get("Work")
        screen_width=work_area[2]
        width=screen_width/4.5 # width of the main
        height=root_hgt
        x=root.winfo_x()
        y=root.winfo_y()
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))
        self.configure(bg='#00FFFF') # Set main backcolor to aqua
        self.bind("<Configure>", ratio_resize)
        self.protocol("WM_DELETE_WINDOW", ratio_destroy)
        txtfont=font.Font(family='Times New Romans', size=14, weight='normal', slant='italic')
        formulafont=font.Font(family='Times New Romans', size=9, weight='bold', slant='italic')
        btnfont=font.Font(family='Times New Romans', size=10, weight='bold', slant='italic')
        ratiofont=font.Font(family='Times New Romans', size=16, weight='bold')
        # Entry widgets StringVar()
        focused=tk.StringVar() 
        formula=tk.StringVar()
        a1=tk.StringVar()
        a2=tk.StringVar()
        b1=tk.StringVar()
        b2=tk.StringVar()
        a3=tk.StringVar()
        b3=tk.StringVar()
        a4=tk.StringVar()
        b4=tk.StringVar()
        # Create and position scrolled textbox to display calculation formulas
        formula_txtbx=ScrolledText(self, bg='#0c012e', fg='#07f7d8', font=formulafont, 
                borderwidth=5, relief="sunken", wrap=tk.WORD)
        formula_txtbx.place(relx=0.015, rely=0.01, relwidth=0.97, relheight=0.22)
        formula_txtbx.focus()
        formula='3 Ratio Values Must Be Present To Calculate'
        formula_txtbx.insert(tk.INSERT, formula)
        formula='\nThe 4th Ratio Value And Porportion Values.'
        formula_txtbx.insert(tk.END, formula)
        formula='\nAll 4 Ratio Values May Be Entered Manually For Porportion Calculations.\n'
        formula_txtbx.insert(tk.END, formula)
        default_text=tk.BooleanVar()
        default_text.set(True)
       # Create and Position Frame1 and Widgets inside Frame1
        frame1=Frame(self, background='#E5E5E5',  
                highlightbackground="#696969", highlightthickness=5)
        frame1.place(relx=0.015, rely=0.24, relwidth=0.97, relheight=0.295)    
        frame1_lbl=tk.Label(frame1, background='#E5E5E5', font=txtfont,
                text="Enter At Lease 3 Ratio Values")
        frame1_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
        a1_lbl=tk.Label(frame1, background='#E5E5E5', font=txtfont, text='A1')
        a1_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
        a1_txtbx=tk.Entry(frame1, background='#FFFFF0', font=txtfont, textvariable=a1)
        a1_txtbx['validatecommand']=(a1_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(a1_txtbx.register(on_validate), '%P')
        a1_txtbx.config(validate="key", validatecommand=val_cmd)
        a1_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
        a1_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'A1'))
        a1_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'A2'))
        a2_lbl=tk.Label(frame1, background='#E5E5E5', font=txtfont, text='A2')
        a2_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
        a2_txtbx=tk.Entry(frame1, background='#FFFFF0', font=txtfont, textvariable=a2)
        a2_txtbx['validatecommand']=(a2_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(a2_txtbx.register(on_validate), '%P')
        a2_txtbx.config(validate="key", validatecommand=val_cmd)
        a2_txtbx.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
        a2_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'A2'))
        a2_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'B1'))
        ratio_lbl=tk.Label(frame1, background='#E5E5E5', font=ratiofont,
                text='__________     :    __________')
        ratio_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
        b1_lbl=tk.Label(frame1, background='#E5E5E5', font=txtfont, text='B1')
        b1_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
        b1_txtbx=tk.Entry(frame1, background='#FFFFF0', font=txtfont, textvariable=b1)
        b1_txtbx['validatecommand']=(b1_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(b1_txtbx.register(on_validate), '%P')
        b1_txtbx.config(validate="key", validatecommand=val_cmd)
        b1_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
        b1_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'B1'))
        b1_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'B2'))
        b2_lbl=tk.Label(frame1, background='#E5E5E5', font=txtfont, text='B2')
        b2_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
        b2_txtbx=tk.Entry(frame1, background='#FFFFF0', font=txtfont, textvariable=b2)
        b2_txtbx['validatecommand']=(b2_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(b2_txtbx.register(on_validate), '%P')
        b2_txtbx.config(validate="key", validatecommand=val_cmd)
        b2_txtbx.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
        b2_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'B2'))
        b2_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'A3'))
        # Create and Position Frame2 and Widgets inside Frame2
        kb_frame=Frame(self, background='#696969',  
                highlightbackground="#696969", highlightthickness=4)
        kb_frame.place(relx=0.015, rely=0.524, relwidth=0.97, relheight=0.08)
        keys=['0','1','2','3','4','5','6','7','8','9','-','.','Backspace']
        key_btn=[]
        for i, item in enumerate(keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
            key_btn.append([num])
            key_btn[i]=Button(kb_frame, text=item, bg="black", fg="white",font=txtfont)
            key_btn[i].pack(side=LEFT,fill=Y)
            key_btn[i].bind("<Button-1>", keyboard)
        # Create and Position Frame2 and Widgets inside Frame2
        frame2=Frame(self, background='#E5E5E5',  
                highlightbackground="#696969", highlightthickness=5)
        frame2.place(relx=0.015, rely=0.596, relwidth=0.97, relheight=0.295)    
        frame2_lbl=tk.Label(frame2, background='#E5E5E5', font=txtfont,
                text="Find Unknown Porportions")
        frame2_lbl.place(relx=0.015, rely=0.02, relwidth=0.97, relheight=0.17)    
        a_lbl=tk.Label(frame2, background='#E5E5E5', font=txtfont, text='A')
        a_lbl.place(relx=0.028, rely=0.23, relwidth=0.07, relheight=0.17)
        a3_txtbx=tk.Entry(frame2, background='#FFFFF0', font=txtfont, textvariable=a3)
        a3_txtbx['validatecommand']=(a3_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(a3_txtbx.register(on_validate), '%P')
        a3_txtbx.config(validate="key", validatecommand=val_cmd)
        a3_txtbx.place(relx=0.11, rely=0.23, relwidth=0.34, relheight=0.17)
        a3_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'A3'))
        a3_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'B3'))
        bAnswer_lbl=tk.Label(frame2, background='#E5E5E5', font=txtfont, text='B =')
        bAnswer_lbl.place(relx=0.53, rely=0.23, relwidth=0.07, relheight=0.17)
        bAnswer=tk.Label(frame2, background='lightgray', font=txtfont, textvariable=b4, justify='right',
                anchor='w', borderwidth=1, relief="sunken") 
        bAnswer.place(relx=0.61, rely=0.23, relwidth=0.34, relheight=0.17)
        porportion_lbl=tk.Label(frame2, background='#E5E5E5', font=ratiofont,
                text='__________    ::    __________')
        porportion_lbl.place(relx=0.08, rely=0.42, relwidth=0.9, relheight=0.17)
        b_lbl=tk.Label(frame2, background='#E5E5E5', font=txtfont, text='B')
        b_lbl.place(relx=0.028, rely=0.74, relwidth=0.07, relheight=0.17)
        b3_txtbx=tk.Entry(frame2, background='#FFFFF0', font=txtfont, textvariable=b3)
        b3_txtbx['validatecommand']=(b3_txtbx.register(validate_Entries),'%P','%d')
        val_cmd=(b3_txtbx.register(on_validate), '%P')
        b3_txtbx.config(validate="key", validatecommand=val_cmd)
        b3_txtbx.place(relx=0.11, rely=0.74, relwidth=0.34, relheight=0.17)
        b3_txtbx.bind("<Button-1>", lambda event:keyboard_focus(event,'B3'))
        b3_txtbx.bind("<Tab>", lambda event:keyboard_focus(event,'A1'))
        aAnswer_lbl=tk.Label(frame2, background='#E5E5E5', font=txtfont, text='A =')
        aAnswer_lbl.place(relx=0.53, rely=0.74, relwidth=0.07, relheight=0.17)
        aAnswer=tk.Label(frame2, background='lightgray', font=txtfont, textvariable=a4, justify='right',
                anchor='w', borderwidth=1, relief="sunken") 
        aAnswer.place(relx=0.61, rely=0.74, relwidth=0.34, relheight=0.17)
        clr_btn=tk.Button(self, font=btnfont, text="CLEAR", fg="black", command=lambda:clear_entries())
        clr_btn.place(relx=0.197, rely=0.912, relwidth=0.16, relheight=0.06)
        calc_btn=tk.Button(self, font=btnfont, text="CALCULATE", fg="red",
                command=lambda:calculate_ratio(a1,a2,b1,b2,a3,b3))
        calc_btn.place(relx=0.38, rely=0.912, relwidth=0.25, relheight=0.06)
        quit_btn=tk.Button(self, font=btnfont, text="QUIT", fg="black", command=ratio_destroy)
        quit_btn.place(relx=0.65, rely=0.912, relwidth=0.16, relheight=0.06)
        self.focus_force()
        a1_txtbx.focus_force()
        focused.set('A1')
        self.mainloop()
class Convert_Base:
    # Class Converts To And From Binary, Octal, Decimal And Hexadecimal, Returned Value Is String Object
    def __init__(self,from_base,to_base,str_val):
        self.f_base=from_base # Integer, Convert From Base
        self.t_base=to_base # Integer, Convert To Base
        self.val=(str_val.split('.')[0])# Remove Any Decimal Values       
        self.r_val='' # String, Returned Converted Value
    def __str__(self):
        def dec_to_bin(val):
            bin_list=list(range(4, 512, 4)) # Good To Hex Length 56 
            value=bin(val & (2**Bit_Size.get() - 1))
            value=value.replace("0b", "")
            bin_len=len(value)
            if bin_len in bin_list:# If In List Then Good To Go
                bin_list=[]
                return str(value)
            else:# Add Extra Zeros
                while bin_len not in bin_list:
                    value=value.rjust(bin_len+1,"0")# Add Zeroes
                    bin_len=len(value)
                    if bin_len in bin_list:
                        bin_list=[]
                        return str(value)
        def dec_to_oct(val):
            if val==0:return'0'
            oct_list=list(range(3, 224, 3))
            value=oct(val & (2**Bit_Size.get() - 1))
            value= value.replace("0o", "")
            oct_len = len(value)
            if oct_len in oct_list:# If In List Then Good To Go
                oct_list=[]
                return str(value)
            else:# Add Extra Zeros
                while oct_len not in oct_list:
                    value=value.rjust(oct_len+1,"0")# Add Zeroes
                    oct_len=len(value)
                    if oct_len in oct_list:
                        oct_list=[]
                        return str(value)
        def dec_to_hex(val):
            if val==0:return'0'
            value=hex(val & (2**Bit_Size.get()-1))
            upper=value.upper() # Uppercase
            value=upper.replace("0X", "")#  Strip 0X
            hex_list=list(range(4, 128, 4))
            hex_len=len(value)
            if hex_len in hex_list:# If In List Then Good To Go
                hex_list=[]
                return str(value)
            else:# Add Extra Zeros
                while hex_len not in hex_list:
                    value=value.rjust(hex_len+1,"0")# Add Zeroes
                    hex_len=len(value)
                    if hex_len in hex_list:
                        hex_list=[]
                        return str(value)
        try:                
            if self.f_base==2:# Binary
                dec_val=int(self.val, 2)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==8:# Octal
                dec_val=int(self.val, 8)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==10:# Decimal
                dec_val=int(self.val, 10)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==16:
                    self.r_val=dec_to_hex(dec_val)
                    return self.r_val
            if self.f_base==16:# Hexadecimal
                dec_val=int(self.val, 16)
                if dec_val>2**(Bit_Size.get())-1:
                    dec_val=2**(Bit_Size.get())-1
                if self.t_base==2:
                    self.r_val=dec_to_bin(dec_val)
                    return self.r_val
                elif self.t_base==8:
                    self.r_val=dec_to_oct(dec_val)
                    return self.r_val
                elif self.t_base==10:
                    self.r_val=dec_val
                    return str(self.r_val)
            return        
        except Exception as e:
            msg1='Exception occurred while code execution:\n'
            msg2= repr(e)+'Convert_Base'
            messagebox.showerror('Exeption Error', msg1+msg2)
            return 'break'
class Convert_Trig_Units:# Class Converts To And From Degrees, Radians, And Gradians. Returns String
    def __init__(self,from_units,to_units,str_val):
        self.f_units=from_units # String, Convert From Units
        self.t_units=to_units # String, Convert To Units
        self.val=float(str_val) # String, Value To Convert       
        self.r_val='' # String, Returned Converted Value
    def __str__(self):
        if self.f_units==self.t_units:
            self.r_val=str(self.val)
            return self.r_val
        def degrees_to_radians():
            value=self.val*(mp.pi/180)
            return str(value)
        def degrees_to_gradians():
            value=self.val*mpf(400/360)
            return str(value)
        def radians_to_degrees():
            value=self.val*(180/mp.pi)
            return str(value)
        def radians_to_gradians():
            degrees=self.val*(180/mp.pi)
            value=degrees*mpf(400/360)
            return str(value)
        def gradians_to_degrees():
            value=self.val*mpf(360/400)
            return str(value)
        def gradians_to_radians():
            degrees=self.val*mpf(360/400)
            value=degrees*(mp.pi/180)        
            return str(value)
        try:    
            if self.f_units=='Degrees':
                if self.t_units=='Radians':
                    self.r_val=degrees_to_radians()
                    return self.r_val
                elif self.t_units=='Gradians':
                    self.r_val=degrees_to_gradians()
                    return self.r_val
            if self.f_units=='Radians':
                if self.t_units=='Degrees':
                    self.r_val=radians_to_degrees()
                    return self.r_val
                elif self.t_units=='Gradians':
                    self.r_val=radians_to_gradians()
                    return self.r_val
            if self.f_units=='Gradians':
                if self.t_units=='Radians':
                    self.r_val=gradians_to_radians()
                    return self.r_val
                elif self.t_units=='Degrees':
                    self.r_val=gradians_to_degrees()
                    return self.r_val
            return        
        except Exception as e:
            msg1='Exception occurred while code execution:\n'
            msg2= repr(e)+'Convert_Trig_Units'
            messagebox.showerror('Exeption Error', msg1+msg2)
            return 'break'
def free_sys_symbols(*args):
    if not D_Memory1 and not  D_Memory2 and not  D_Memory3 and not  D_Memory4:
        if not args:
            for abc in Symbols_Used:
                Symbol(abc).free_symbols
            Symbols_Used.clear()
            Symbol_Names.clear()
            Symbol_Values.clear()
        else:
            for ar in args:
                Symbol(ar).free_symbols
    else:return
class Calculus:
    def __init__(self, funct):
        if not Disp_List:return
        base=Base.get()
        if base!='Decimal':return
        def destroy():# X Icon Was Clicked
            for widget in self.winfo_children():
                if isinstance(widget, tk.Canvas):
                    widget.destroy()
                else:
                    widget.destroy()
            if Window_State.get()=='zoomed':root.state('zoomed')
            self.withdraw()
            root.deiconify()
            root.grab_set()
            root.focus_force()
            root.update()
        def get_next_symbol(val):
            if val in Symbol_Values:# Value Already Symbolized, return Symbol
                for i, j in enumerate(Symbol_Values):
                    if j == val:return Symbol_Names[i]
            for symbol in list(map(chr,range(ord('a'),ord('z')+1))):
                if not symbol in _MyClash and not symbol in Symbols_Used:
                    parsed=parse_expr(symbol, evaluate=False)
                    symbol=sym.symbols(symbol)
                    Symbols_Used.append(str(symbol))
                    Symbol_Names.append(parsed)
                    Symbol_Values.append(val)
                    return symbol
            else: 
                for symbol in list(map(chr,range(ord('A'),ord('Z')+1))):
                    if not symbol in _MyClash and not symbol in Symbols_Used:
                        symbol=sym.symbols(symbol)
                        Symbols_Used.append(str(symbol))
                        return symbol
        disp=Display.get()
        self=Toplevel(root)
        root.withdraw()
        self.deiconify()
        self.grab_set() # Receive Events And Prevent root Window Interaction
        if funct=='integrate':self.title('Integral Work Sheet')
        elif funct=='differentiate':self.title('Derivative Work Sheet')
        # Set Tk main Dimensions and Position Center Of Screen
        wid=root_wid
        hgt=root_hgt
        x=root.winfo_x()
        y=root.winfo_y()
        self.geometry('%dx%d+%d+%d' % (wid, hgt, x, y, ))
        self.configure(bg='#f3f6f4')
        self.protocol("WM_DELETE_WINDOW", destroy)
        self.font=font.Font(family='Times New Romans', size=12, weight='normal', slant='italic')
        self.option_add('*TCombobox*Listbox.font', self.font)
        tk.Frame.scroll = XY_Scrollbars(self, wid, hgt) 
        tk.Frame.scroll.pack(side="top", fill="both", expand=True)
        def integral_doit(event):
            try:
                resp=parse_expr(respect.get(), evaluate=False)
                parsed_integral=parse_expr(expr, evaluate=True)
                disp_update('clear')
                integral_expr=Integral(parsed_integral,resp)
                exp=integral_expr.doit()
                newstr=str(expr2)
                for i in range(5):# Remove Extra Brackets
                    if newstr[0]=='(' and newstr[-1]==')':
                        newstr=newstr[1:-1]
                    else:break    
                lbl_4[0].config(text = f"Equation = ∫{resp}({newstr}) = {exp}")
                answer=nround_answer(exp) # Round Answer To User Preference
                Answer_Present.set(True)
                Answer.set(answer)
                lbl_4[1].config(text = f"{exp} = {answer}")
                disp_update(f"∫{resp}({newstr}) = {answer}\n")
                lbl_4[2].config(text = f"Answer = {answer}")
                return
            except Exception:
                Answer.set('')
                Answer_Present.set(False)
                Answer_Err.set(True)
                disp_update(' = Invalid Entry!')
                expr_update(' = Invalid Entry!')
                lbl_4[1].config(text = 'Invalid Entry!')
                return 'break'
        def derivative_doit(event):
            multiple_derivatives=multiple.get()
            resp=respect.get()
            if multiple_derivatives=='':return
            if resp=='':return
            try:
                resp=parse_expr(respect.get(), evaluate=False)
                parsed_derative=parse_expr(expr, evaluate=True)
                disp_update('clear')
                multiple_derivatives=multiple.get()
                tmp_str=''
                for i in multiple.get(): # Extract Number From String
                    if i.isdigit():tmp_str+=i
                multi=parse_expr(tmp_str, evaluate=False)    
                if multiple_derivatives=='1st Derivative':mstr="f '"
                elif multiple_derivatives=='2nd Derivative':mstr="f ''"
                elif multiple_derivatives=='3rd Derivative':mstr="f '''"
                elif multiple_derivatives=='4th Derivative':mstr="f ''''"
                elif multiple_derivatives=='5th Derivative':mstr="f '''''"
                derative_expr=Derivative(parsed_derative, resp, multi)
                exp=derative_expr.doit()
                newstr=str(expr2)
                for i in range(5):# Remove Extra Brackets
                    if newstr[0]=='(' and newstr[-1]==')':
                        newstr=newstr[1:-1]
                    else:break    
                lbl_4[0].config(text = f"Equation = {mstr}{resp}({newstr}) = {exp}")
                answer=nround_answer(exp)
                Answer_Present.set(True)
                Answer.set(answer)
                lbl_4[1].config(text = f"{exp} = {answer}")
                disp_update(f"{mstr}{resp}({newstr}) = {answer}\n")
                lbl_4[2].config(text = f"Answer = {answer}")
                return    
            except Exception:
                Answer.set('')
                Answer_Present.set(False)
                Answer_Err.set(True)
                disp_update(' = Invalid Entry!')
                expr_update(' = Invalid Entry!')
                lbl_4[1].config(text = 'Invalid Entry!')
                return 'break'
        tk.Frame.scroll.canvas.xview_moveto(0)
        tk.Frame.scroll.canvas.yview_moveto(0)
        close_brackets('all')# (Just In Case) Close All Opened Brackets Before Preceding
        disp=Display.get()
        expr=Expression.get()
        expr2=expr
        txt='Expression = '+disp
        r=1    
        lbl_1=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                text=txt, anchor='w')
        lbl_1.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)        
        val=''
        last=False
        for i, item in enumerate(expr):# Populate Names With Values
            if item.isnumeric() or item=='.' or item=='-':
                if item=='-': # Only Populate Negative Numbers And Not Negative Functions 
                    if disp[1].isnumeric(): # Negative Number
                        #Build Value
                        val+=item
                        last=True
                else:#Build Value        
                    val+=item
                    last=True
            else:
                if last==True:
                    xyz=get_next_symbol(float(val))
                    expr=str(expr).replace(str(val),str(xyz),1) #replace value with Symbol_Names
                    last=False
                    val=''
        if last==True:
            xyz=get_next_symbol(float(val))
            expr=str(expr).replace(str(val),str(xyz),1)#replace value with Symbol_Names
            last=False
            val=''
        lbl_2=[]
        used_symbols=[]
        used_txt=[]
        c=0
        for i in range(len(Symbol_Names)):# Place Names And Values into Dictionary And Populate Labels
            txt=''
            sub_dict[Symbol_Names[i]] = Symbol_Values[i]
            if Symbol_Names[i] not in used_symbols:# Prevent Duplicate Symbol Population
                txt=str(Symbol_Names[i])+' = '+str(Symbol_Values[i])
                used_txt.append(txt) # Used To Populate These Labels
                used_symbols.append(Symbol_Names[i]) # Used To Polulate symbol_bx 
                r+=1        
                lbl_2.append([c])
                lbl_2[c]=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                    text=used_txt[c], anchor='w', justify='left')
                lbl_2[c].grid(column=0,row=r, sticky=tk.W, padx=5, pady=1)
                c+=1
        r+=1
        newstr=str(expr)
        if newstr[0]=='(' and newstr[-1]==')':newstr=newstr[1:-1] # Remove Extra Brackets
        txt='Expression Symbolized = '+newstr
        lbl_3=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
            text=txt, anchor='w')
        lbl_3.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
        r+=1
        cbo_lbl=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
            text='Respect to:', anchor='w')
        cbo_lbl.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
        respect=StringVar()
        style= ttk.Style()
        style.theme_use('default')
        r+=1
        style.configure("TCombobox", fieldbackground= '#f0ffff', background= '#f3f6f4')
        symbol_bx=ttk.Combobox(tk.Frame.scroll.window, values=used_symbols, font=self.font, width=13, 
        textvariable=respect, justify=tk.LEFT) 
        symbol_bx.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
        symbol_bx['state'] = 'readonly'
        if funct=='differentiate':
                r+=1
                multiples=['1st Derivative','2nd Derivative','3rd Derivative','4th Derivative','5th Derivative']
                multi_lbl=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font, 
                    text='No. of Derivatives:', anchor='w')
                multi_lbl.grid(column=0, row=r, sticky=tk.W, padx=5, pady=0)
                multiple=StringVar()
                style= ttk.Style()
                style.theme_use('default')
                r+=1
                style.configure("TCombobox", fieldbackground= '#f0ffff', background= '#f3f6f4')
                multi_bx=ttk.Combobox(tk.Frame.scroll.window, values=multiples, font=self.font, width=13, 
                textvariable=multiple, justify=tk.LEFT) 
                multi_bx.grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
                multi_bx.bind('<<ComboboxSelected>>', derivative_doit)
                multi_bx['state'] = 'readonly'
        if funct=='integrate':symbol_bx.bind('<<ComboboxSelected>>', integral_doit)
        elif funct=='differentiate':symbol_bx.bind('<<ComboboxSelected>>', derivative_doit)
        lbl_4=[]
        for i in range(0,3):
            r+=1
            lbl_4.append([i])
            lbl_4[i]=tk.Label(tk.Frame.scroll.window, background='#f3f6f4', font=self.font,
                text='',anchor='w')
            lbl_4[i].grid(column=0, row=r, sticky=tk.W, padx=5, pady=1)
        self.mainloop()
class Init_Calculator:
    def __init__(self, funct):
        dir=pathlib.Path(__file__).parent.absolute()
        filename='pySci.ini' # Program icon
        ini_path=os.path.join(dir, filename)
        config = configparser.ConfigParser()
        def read_ini_data():
            # Reading Data
            config.read(ini_path)
            keys=["calculator","rounding","scientific_notation","exponential_notation","binary_bit_size"]
            for key in keys:
                try:
                    value=config.get("PRECISIONS", key)
                    if key=="calculator":mp.dps=int(value)
                    elif key=="rounding":Round.set(int(value))
                    elif key=="scientific_notation":Exp_Precision.set(int(value))
                    elif key=="exponential_notation":Exp_Digits.set(int(value))
                    elif key=="binary_bit_size":Bit_Size.set(int(value))
                except configparser.NoOptionError:
                    pass
            config.read(ini_path)
            keys=["forecolor","backcolor","font"]
            for key in keys:
                try:
                    value = config.get("DISPLAY", key)
                    if key=="forecolor":
                        Display_fg.set(value)
                        Display_Text.focus_force()
                        Display_Text.config(bg=Display_bg.get())
                        Display_Text.config(fg=Display_fg.get())
                    elif key=="backcolor":
                        Display_bg.set(value)
                        Display_Text.focus_force()
                        Display_Text.config(bg=Display_bg.get())
                        Display_Text.config(fg=Display_fg.get())
                    elif key=="font":
                        NewFont.set(value)
                        new_font=parse_expr(value, evaluate=False)
                        new_font['family'] = new_font['family'].replace('\\', '')
                        display_font.config(family=new_font['family'], size=new_font['size'], 
                            weight=new_font['weight'], slant=new_font['slant'])
                        NewFont_Size.set(new_font['size'])
                        Display_Text.focus_force()
                        Display_Text.configure(font=display_font)
                except configparser.NoOptionError:
                    pass
            config.read(ini_path)
            keys=["x","y","state","width","height"]
            for key in keys:
                try:
                    value=config.get("WINDOW", key)
                    if key=="x":x=int(value)
                    elif key=="y":y=int(value)
                    elif key=="state":
                        Window_State.set(value)
                        root.state(value)
                    elif key=="width":width=float(value)    
                    elif key=="height":height=float(value)    
                except configparser.NoOptionError:
                    pass
            root.geometry('%dx%d+%d+%d' % (width, height, x, y, ))
            root.bind("<Configure>", calculator_resize)
            root.update()
        def write_ini_data():
            config = configparser.ConfigParser()
            config.read(ini_path)
            try:
                config.add_section("PRECISIONS")
            except configparser.DuplicateSectionError:
                pass    
            config.set("PRECISIONS", "calculator", str(mp.dps))
            config.set("PRECISIONS", "rounding", str(Round.get()))
            config.set("PRECISIONS", "scientific_notation", str(Exp_Precision.get()))
            config.set("PRECISIONS", "exponential_notation", str(Exp_Digits.get()))
            config.set("PRECISIONS", "binary_bit_size", str(Bit_Size.get()))
            try:
                config.add_section("DISPLAY")
            except configparser.DuplicateSectionError:
                pass
                config.set("DISPLAY", "forecolor", str(Display_fg.get()))
                config.set("DISPLAY", "backcolor", str(Display_bg.get()))
                config.set("DISPLAY", "font", NewFont.get())
            try:
                config.add_section("WINDOW")
            except configparser.DuplicateSectionError:
                pass
                if Window_State.get()=='normal':
                    config.set("WINDOW", "x", str(root.winfo_x()))
                    config.set("WINDOW", "y", str(root.winfo_y()))
                    config.set("WINDOW", "state", str(Window_State.get()))
                    config.set("WINDOW", "width", str(root.winfo_width()))
                    config.set("WINDOW", "height", str(root.winfo_height()))
            with open(ini_path, 'w') as configfile:
                config.write(configfile)
        if funct=='read':read_ini_data()        
        elif funct=='write':write_ini_data()
def convert_script(from_script,to_script,txt):# Convert Between Normal Script, Superscript And Subscript
    new_txt=txt.maketrans(''.join(from_script), ''.join(to_script))
    return txt.translate(new_txt)
def menu_popup(event):# display the popup menu
   try:
      popup.tk_popup(event.x_root, event.y_root)
   finally:
      popup.grab_release()#Release the grab
def precision(which): # Calculator Precision Configuration
    if which=='dp':
        dpp=simpledialog.askinteger("<Calculator Precision>","Enter Number Of Digits For Calculations. Max = 500",
            parent=root,minvalue=1, maxvalue=500, initialvalue=mp.dps)
        if dpp is not None:
            mp.dps=int(dpp)
            mp.pretty==False
    elif which=='round':        
        rnd=simpledialog.askinteger("<Round Displayed Answer>","Round Answer To nth Decimal Places. 0 = No Rounding, Max = 500",
            parent=root,minvalue=0, maxvalue=500, initialvalue=Round.get())
        if rnd is not None:Round.set(int(rnd))
    elif which=='exp':        
        snp=simpledialog.askinteger("<Scientific Notation Digits>","Total Decimal Digits To Display For Scientific Notation. Max = 500",
            parent=root,minvalue=1, maxvalue=500, initialvalue=Exp_Precision.get())
        if snp is not None:Exp_Precision.set(int(snp))
    elif which=='exp_digits':
        enp=simpledialog.askinteger("<Exponential Notation Digits>","Exponential Notation Precision. Max = 4",
            parent=root,minvalue=1, maxvalue=4, initialvalue=Exp_Digits.get())
        if enp is not None:Exp_Digits.set(int(enp))
    elif which=='bit_size':
        choices=['4','8','16','32','64','128','512']
        bbs=simpledialog.askinteger("<Binary Bit Size>","Choices Are 8(Byte) 16(Word), 32(DWord), 64(QWord), 128(DQ).",
            parent=root,minvalue=4, maxvalue=512, initialvalue=Bit_Size.get())
        if bbs is not None:
            if str(bbs) in choices:
                Bit_Size.set(int(bbs))
            else:
               messagebox.showinfo('Binary Bit Size', f'The Value You Entered "{bbs}" Is Incorrect. Please Try Again!')
def choose_font(): # Display Font
    default_font=NewFont.get()
    old_font=parse_expr(default_font, evaluate=False)
    old_font['family'] = old_font['family'].replace('\\', '')
    if Display.get()!='':sample=Display.get()
    else:sample='Sample text for selected font.'
    new_font=askfont(root,text=sample,title="Choose Display Font" ,family=old_font['family'],
        size=old_font['size'],weight=old_font['weight'],slant=old_font['slant'])
    if new_font!='':
        new_font['family'] = new_font['family'].replace('\\', '')
        NewFont.set(new_font)
        NewFont_Size.set(new_font['size'])
        display_font.config(family=new_font['family'], size=new_font['size'], weight=new_font['weight'], 
            slant=new_font['slant'])
        Display_Text.focus_force()
        Display_Text.configure(font=display_font)
def choose_color(which): # Display fg and bg Colors
    if which=='bg':# Background
        color_code = colorchooser.askcolor(title ="Choose Display Background Color", initialcolor=Display_bg.get())
        if color_code[1]==None:return
        Display_bg.set(color_code[1])
        Display_Text.focus_force()
        Display_Text.config(bg=Display_bg.get())
        Display_Text.config(fg=Display_fg.get())
    elif which=='fg':# Foreground     
        color_code = colorchooser.askcolor(title ="Choose Display ForeColor", initialcolor=Display_fg.get())
        if color_code[1]==None:return
        Display_fg.set(color_code[1])
        Display_Text.focus_force()
        Display_Text.config(bg=Display_bg.get())
        Display_Text.config(fg=Display_fg.get())
def about():
    messagebox.showinfo('About pySci Calculator', 'Creator: Ross Waters\nEmail: RossWatersjr@gmail.com'\
        '\nProblems Encountered: Please Contact Me @email'\
        '\nScientific Calculator Created In Python'\
        '\nLanguage: Python version 3.11.2 64-bit'\
        '\nProgram: pySci Calculator Created Using\ntkinter version 8.6,\nsympy version 1.11.1,\nmpmath version 1.2.1'\
        '\nRevision \ Date: 2.3.0 \ 05/08/2023'\
        '\nCreated For Windows 10/11')
def calculator_destroy():
    try:# X Icon Was Clicked
        Init_Calculator('write')            
        clear_memories()
        clear_all()
        Symbol_Names.clear()
        Symbol_Values.clear()
        _MyClash.clear()
        _MyConstants.clear()
        Operators.clear()
        for widget in root.winfo_children():
            if isinstance(widget, tk.Canvas):widget.destroy()
            else:widget.destroy()
        os._exit(0)
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+'calculator_destroy'
        messagebox.showerror('Exeption Error', msg1+msg2)
        os._exit(0)
def disp_update(txt, b=None):
    if txt!='clear':
        if txt==' = ' or Answer_Present.get():
            disp=Display.get()
            disp+=txt
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp)
            Display.set(disp)
            Disp_List.append(str(txt))
        elif txt=='refresh':    
            Display.set('')
            Display_Text.delete('1.0','end')
            disp=''.join(Disp_List)
            disp2=str(disp).replace('{','').replace('}','')
            Display.set(disp2)
            Display_Text.insert('end',disp2)
        else:     
            Display.set('')
            Display_Text.delete('1.0','end')
            Disp_List.append(str(txt))
            disp=''.join(Disp_List)
            disp2=str(disp).replace('{','').replace('}','')
            Display.set(disp2)
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp2)
            if b==None:
                if txt=='(':bracket_clicked('auto','disp','open')
                elif txt==')':bracket_clicked('auto','disp','close')
            if txt=='{':
                td_open=Temp_Disp_Open.get()
                td_open+=1
                Temp_Disp_Open.set(td_open)
            elif txt=='}':
                td_open=Temp_Disp_Open.get()
                td_open-=1
                Temp_Disp_Open.set(td_open)
    else:
        Display.set('')
        Display_Text.delete('1.0','end')
        Disp_List.clear()
        bracket_clicked('manual','both','clear')
def expr_update(txt, b=None):
    if txt!='clear':
        if txt==' = ' or Answer_Present.get():
            expr=Expression.get()
            expr+=txt
            Expression.set(expr)
            Expr_List.append(str(txt))
        elif txt=='refresh':    
            Expression.set('')
            expr=''.join(Expr_List)
            expr2=str(expr).replace('{','').replace('}','')
            Expression.set(expr2)
        else:     
            Expression.set('')
            Expr_List.append(str(txt))
            expr=''.join(Expr_List)
            expr2=str(expr).replace('{','').replace('}','')
            Expression.set(expr2)
            if b==None: 
                if txt=='(':bracket_clicked('auto','expr','open')
                elif txt==')':bracket_clicked('auto','expr','close')
            if txt=='{':
                te_open=Temp_Expr_Open.get()
                te_open+=1
                Temp_Expr_Open.set(te_open)
            elif txt=='}':
                te_open=Temp_Expr_Open.get()
                te_open-=1
                Temp_Expr_Open.set(te_open)
    else:
        Expression.set('')
        Expr_List.clear()
        bracket_clicked('manual','both','clear')
def numeric_clicked(event):
    try:
        if event.type=='4':text=event.widget["text"] # ButtonPress
        elif event.type=='2':text=event.char # KeyPress
        Display_Text.focus_force()    
        Display_Text.unbind('<period>')
        if text=='??': # Binding event Overrides Disabled State So Check State. If State = 'disabled' return
            if 'disabled' in event.widget.config('state'):return
        elif text=='.' and not Disp_List:
            clear_all()
            return
        elif text=='.'and Disp_List[-1]=='.':
            disp=Display.get()
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',disp)
            Display.set(disp)
            return    
        if Answer_Present.get() and text=='.':return  
        if Answer_Present.get() or Answer_Err.get():clear_all()
        base=Base.get()
        Display_Text.focus_set()
        if base=='Decimal':
            text=str(text)    
            dec_values=['0','1','2','3','4','5','6','7','8','9']
            if text=='.':# Prevent Multiple Periods From Keyboard Entry
                reverse_value('disp',False)
                value=return_value('disp',False,True) 
                if '.' in value:
                    text=''
                    Display_Text.focus_force()    
                    Display_Text.bind(('<period>'), lambda e: "break")
                    return
                else:    
                    Display_Text.focus_force()    
                    Display_Text.unbind('<period>')
                if Disp_List:
                    if not type_isnumerical(Disp_List[-1]):return       
                    if Disp_List[-1]=='.':return       
                    disp_update(text)
                    expr_update(text)
            elif text in dec_values:     
                if Answer_Present.get() or Answer_Err.get():clear_all()
                disp_update(text)
                expr_update(text)
        else:
            active_values=[]
            text=str(text).upper()
            if base=='Hexadecimal':
                hex_values=['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
                if not text in hex_values:return
                active_values=hex_values
            elif base=='Octal':
                octal_values=['0','1','2','3','4','5','6','7']
                if not text in octal_values:return
                active_values=octal_values
            elif base=='Binary':
                bin_values=['0','1']
                if not text in bin_values:return
                active_values=bin_values
            if Answer_Present.get() or Answer_Err.get():clear_all()
            disp_update(text)
            Reversed_List.clear()
            opened=0
            closed=0
            if Disp_List:# Reverse Disp_List  But Do Not Pop
                if Disp_List[-1]==')':# Value Inside Brackets
                    for i in list(reversed(Disp_List)):
                        if i=='(':opened+=1
                        if i==')':closed+=1
                        if i in active_values:Reversed_List.append(i)
                        if opened==closed:break
                else:# No Brackets, Only Get Numbers    
                    for i in list(reversed(Disp_List)):
                        if i in active_values:Reversed_List.append(i)
                        else:break
            val2='' # Return Hex Sequence And Get Decimal Equalivent
            for i in list(reversed(Reversed_List)):
                val2+=i
            if base=='Hexadecimal':value=Convert_Base(16,10,str(val2))
            elif base=='Octal':value=Convert_Base(8,10,str(val2))
            elif base=='Binary':value=Convert_Base(2,10,str(val2))
            # Update Expr_List With New Value
            if Expr_List:
                reverse_value('expr',True)
                expr_update(str(value))
            else:expr_update(str(value))
        return    
    except Exception:
        return 'break'
def set_numeric_type(value):
    try:
        float(value)
        status=float(value).is_integer()
        if status and '.' in str(value):return str(value) # Convert xx.0 To Integer xx
        elif status and not '.' in value:return str(int(value))# True Integer
        elif not status and 'e' in value:return str(mpf(value))# Scientific Notation
        elif not status and '.' in value:return str(mpf(value))# True Float
        else:return value   
    except Exception:return 'Invalid Type!'
def type_isnumerical(instr):
    # numeric_list Chars As Part Of Numerical Values
    numeric_list=['-','.',',','!',')','}','^','**']
    try:
        if instr in numeric_list:return True
        elif float(instr): return True
        elif instr.isnumeric():return True
        elif instr.isdigit():return True
        elif instr.isdecimal():return True
        elif instr=='0.0':return True
        else:return False
    except ValueError:
        return False
def clear_memories():
    mem_btn[0]['text']='ms1'
    mem_btn[0].configure(bg='#ffff99')
    D_Memory1.clear()
    E_Memory1.clear()
    mem_btn[1]['text']='ms2'
    mem_btn[1].configure(bg='#ffff99')
    D_Memory2.clear()
    E_Memory2.clear()
    mem_btn[2]['text']='ms3'
    mem_btn[2].configure(bg='#ffff99')
    D_Memory3.clear()
    E_Memory3.clear()
    mem_btn[3]['text']='ms4'
    mem_btn[3].configure(bg='#ffff99')
    D_Memory4.clear()
    E_Memory4.clear()
def memory_clicked(event):
    try:
        allowed=['^','**',', ']
        txt=event.widget["text"]
        if Disp_List and Expr_List:
            if Answer_Present.get():
                display_value=Disp_List[-1]
                expression_value=Expr_List[-1]
            else:
                disp_open=Disp_Bkts_Open.get()
                expr_open=Expr_Bkts_Open.get()
                if disp_open==0 and expr_open>0: # If Display Closed, Close Expression
                    for i in range(expr_open):
                        expr_update(')')
                display_value=''.join(Disp_List)
                expression_value=''.join(Expr_List)
        else:
            display_value=''
            expression_value=''    
        if txt=='ms1':
            D_Memory1.clear()
            E_Memory1.clear()
            if display_value!='':
                for i in display_value:D_Memory1.append(i)
                mem_btn[0]['text']='mr1'
                mem_btn[0].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory1.append(i)
        elif txt=='ms2':
            D_Memory2.clear()
            E_Memory2.clear()
            if display_value!='':
                for i in display_value:D_Memory2.append(i)
                mem_btn[1]['text']='mr2'
                mem_btn[1].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory2.append(i)
        elif txt=='ms3':
            D_Memory3.clear()
            E_Memory3.clear()
            if display_value!='':
                for i in display_value:D_Memory3.append(i)
                mem_btn[2]['text']='mr3'
                mem_btn[2].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory3.append(i)
        elif txt=='ms4':
            D_Memory4.clear()
            E_Memory4.clear()
            if display_value!='':
                for i in display_value:D_Memory4.append(i)
                mem_btn[3]['text']='mr4'
                mem_btn[3].configure(bg='#ffffff')
            if expression_value!='':
                for i in expression_value:E_Memory4.append(i)
        if txt=='mr1':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory1)): 
                    disp_update(D_Memory1[i])
                for i in range(len(E_Memory1)): 
                    expr_update(E_Memory1[i])
            else:    
                if Disp_List[-1] == D_Memory1[-1] and Expr_List[-1]==E_Memory1[-1]:return
                else:
                    if Disp_List[-1] not in Operators and Disp_List[-1] not in allowed:return
                    else:    
                        for i in range(len(D_Memory1)): 
                            disp_update(D_Memory1[i])
                        for i in range(len(E_Memory1)): 
                            expr_update(E_Memory1[i])
        elif txt=='mr2':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory2)): 
                    disp_update(D_Memory2[i])
                for i in range(len(E_Memory2)): 
                    expr_update(E_Memory2[i])
            else:    
                if Disp_List[-1] == D_Memory2[-1] and Expr_List[-1]==E_Memory2[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory2)): 
                            disp_update(D_Memory2[i])
                        for i in range(len(E_Memory2)): 
                            expr_update(E_Memory2[i])
        elif txt=='mr3':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory3)): 
                    disp_update(D_Memory3[i])
                for i in range(len(E_Memory3)): 
                    expr_update(E_Memory3[i])
            else:    
                if Disp_List[-1] == D_Memory3[-1] and Expr_List[-1]==E_Memory3[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory3)): 
                            disp_update(D_Memory3[i])
                        for i in range(len(E_Memory3)): 
                            expr_update(E_Memory3[i])
        elif txt=='mr4':
            if not Disp_List and not Expr_List:
                for i in range(len(D_Memory4)): 
                    disp_update(D_Memory4[i])
                for i in range(len(E_Memory4)): 
                    expr_update(E_Memory1[4])
            else:    
                if Disp_List[-1] == D_Memory4[-1] and Expr_List[-1]==E_Memory4[-1]:return
                else:    
                    if Disp_List[-1] not in Operators and Expr_List[-1] not in Operators:return
                    else:    
                        for i in range(len(D_Memory4)): 
                            disp_update(D_Memory4[i])
                        for i in range(len(E_Memory4)): 
                            expr_update(E_Memory4[i])
        return                    
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+'memory_clicked'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def sign_clicked(event):
    base=Base.get()
    if Answer_Present.get() or base!='Decimal':return
    if event.widget["text"]!=chr(177) or 'disabled' in event.widget.config('state'):return
    dbo,tdo,ebo,teo=Disp_Bkts_Open.get(),Temp_Disp_Open.get(),Expr_Bkts_Open.get(),Temp_Expr_Open.get() 
    # If Display Closed, Close Expression
    if dbo==0:
        for i in range(ebo):expr_update(')')
    if tdo==0:            
        for i in range(teo):expr_update('}')
    try:
        if Disp_List and Expr_List:
            # Open Brackets With Numeric End ,'-10.3'(10.3' or Is Constant Or % 
            if Disp_List[-1].isdecimal() and Expr_List[-1].isdecimal() or Disp_List[-1] in _MyConstants and \
                Expr_List[-1] in _MyConstants or Disp_List[-1]=='%': # Change Sign For Value Not Enclosed In Brackets
                allowed=['-','.','%']
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10' 
                        if i.isdecimal() or i in allowed or i in _MyConstants:n-=1
                        else:break
                    if active_list[n]!='-':active_list.insert(n,'-')
                    elif active_list[n]=='-':active_list.pop(n)
                    if l==0:disp_update('refresh')        
                    elif l==1:expr_update('refresh')        
                return        
            elif Disp_List[-1]==')' and Expr_List[-1]==')': # Change Sign For Values Inside Parentheses
                bkt_opened,bkt_closed=0,0
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    for i in list(reversed(active_list)): # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                        n-=1
                        if i==')':bkt_closed+=1
                        elif i=='(':bkt_opened+=1
                        if bkt_opened==bkt_closed:
                            if i=='(':
                                if active_list[n-1]!='-':active_list.insert(n,'-')
                                elif active_list[n-1]=='-':active_list.pop(n-1)
                                if l==0:disp_update('refresh')        
                                elif l==1:expr_update('refresh')        
                                break
                return        
            elif Disp_List[-1]=='}' and Expr_List[-1]=='}': # Change Sign For Completed Functions Inside Temp Brackets
                for l in range(2): # Do Both List
                    if l==0:active_list=Disp_List
                    elif l==1:active_list=Expr_List     
                    n=len(active_list)        
                    closed,opened=0,0        
                    for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                        n-=1
                        if i=='}':closed+=1
                        elif i=='{':opened+=1
                        if i=='{' and closed==opened:
                            if active_list[n+1]!='-':active_list.insert(n+1,'-')
                            elif active_list[n+1]=='-':active_list.pop(n+1)
                            if l==0:disp_update('refresh')        
                            elif l==1:expr_update('refresh')        
                            break
                return                
    except:pass
def operator_clicked(event):
    try:
        if event.type=='4':text=event.widget["text"] # ButtonPress
        elif event.type=='2':text=' '+event.char+' ' # KeyPress
        if not Disp_List:return
        if Disp_List[-1] in Operators:return # Prevent Multiple Operators
        disp_open=Disp_Bkts_Open.get()
        expr_open=Expr_Bkts_Open.get()
        if not disp_open and expr_open:bracket_clicked('manual','expr','close')
        if not Answer_Err.get():
            disp_update(text)
            expr_update(text)
            if Answer_Present.get():# Answer Becomes 1st Entry, Operator Becomes Second Entry
                answer=Answer.get()
                clear_all()# Start Fresh
                disp_update(answer)
                disp_update(text)
                base=Base.get() # If Base = Hex, Convert Expression Answer To Decimal
                if base=='Hexadecimal':answer=Convert_Base(16,10,str(answer))
                elif base=='Octal':answer=Convert_Base(8,10,str(answer))
                elif base=='Binary':answer=Convert_Base(2,10,str(answer))
                expr_update(answer)
                expr_update(text)
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' Operator_Clicked, Button Pressed = '+Math_Function.get()
        msg3='\nPlease Check Entry Values!'
        messagebox.showerror('Exeption Error', msg1+msg2+msg3)
        return 'break'
def is_float(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
def reverse_value(which,pop):
    Reversed_List.clear()
    if not Disp_List:return
    if not Expr_List:return
    try:
        active_list=[]
        if which=='disp':active_list=Disp_List
        elif which=='expr':active_list=Expr_List
        # Populate With Value (Exposed) Not Enclosed In Brackets
        if active_list[-1].isdecimal() or is_float(active_list[-1]) or active_list[-1] in _MyConstants  or active_list[-1]=='%':
            allowed=['-','.','%']
            for i in list(reversed(active_list)): # Display, # '10', '(10 + 10', '{(10) + 10', ', 10'
                if i.isdecimal() or is_float(i) or i in allowed or i in _MyConstants or i in Hex_List:
                    Reversed_List.append(i)
                    if pop:active_list.pop()
                else:break
            return ''.join(Reversed_List)
        elif active_list[-1]==')': # Values Inside Parentheses (Rounded Brackets).
            bkt_opened,bkt_closed=0,0
            for i in list(reversed(active_list)):  # (10), '(10 + 10), '{(10 + 10)', ((10*3)+2), etc...
                Reversed_List.append(i)
                if pop:active_list.pop()
                if i==')':bkt_closed+=1
                elif i=='(':bkt_opened+=1
                if bkt_opened==bkt_closed:break
            return ''.join(Reversed_List)
        elif active_list[-1]=='}': # Value Is Completed Function Inside Temp Brackets
            bkt_opened,bkt_closed=0,0
            for i in list(reversed(active_list)): # '{(10 + 10)}, {(log(20000), 10)}, etc...
                Reversed_List.append(i)
                if pop:active_list.pop()
                if i=='}':bkt_closed+=1
                elif i=='{':bkt_opened+=1
                if bkt_opened==bkt_closed:break
            return ''.join(Reversed_List)
    except:pass
def return_value(which, update, bracket):
    try:
        value=''
        for i in list(reversed(Reversed_List)):value+=i
        if value[0]!='{' and value[-1]!='}': # Value Not Enclosed In {}
            if value[0]!='(' and value[-1]!=')': # Value Not Enclosed In ()
                if bracket:value='('+value+')' # Bracket value With ()
                if update:
                    if which=='disp':
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
            elif value[0]=='(' and value[-1]==')': # Value Enclosed In ()
                if update:
                    if which=='disp':        
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
            else: # Something Else    
                if update:
                    if which=='disp':        
                        for element in value:disp_update(element,'Some')
                    elif which=='expr':    
                        for element in value:expr_update(element,'Some')
                return value
        else: # Value Enclosed With {}     
            if update:
                if which=='disp':
                    for element in value:disp_update(element,'Some')
                elif which=='expr':    
                    for element in value:expr_update(element,'Some')
            return value
    except:pass
def open_temp_bracket(which): # Only Used To Increment Unfinished Function Brackets
    if which=='disp':
        td_open=Temp_Disp_Open.get()
        td_open+=1
        Temp_Disp_Open.set(td_open)
    elif which=='expr':
        te_open=Temp_Expr_Open.get()
        te_open+=1
        Temp_Expr_Open.set(te_open)
def close_brackets(which): # Close Unfinished Function Brackets
    if which=='all' or which=='disp':
        disp_open=Disp_Bkts_Open.get()
        if disp_open>0:
            for b in range(0,disp_open):
                disp_update(')')
    if which=='all' or which=='expr':            
        expr_open=Expr_Bkts_Open.get()
        if expr_open>0:
            for b in range(0,expr_open):
                expr_update(')')
    if which=='all' or which=='temp_disp':    
        td_open=Temp_Disp_Open.get()
        if td_open>0:
            for b in range(0,td_open):
                disp_update('}')
    if which=='all' or which=='temp_expr':            
        te_open=Temp_Expr_Open.get()
        if te_open>0:
            for b in range(0,te_open):
                expr_update('}')
def function_check(val):# Prevents Decimal Functions From Trying To Be Converted To Another Base.
    val=str(val)
    list1=['sin','cos','tan','sec','csc','cot','sinh','cosh','tanh','sech','csch','coth']
    list2=['asin','acos','atan','asec','acsc','acot','asinh','acosh','atanh','asech','acsch','acoth']
    list3=['log𝒆','log₁₀','log','1 / ','^','**','ʸ√','²√','³√','n!']
    for item in list1:
        for value in Disp_List:
            if item in value:return True
    for item in list2:
        for value in Disp_List:
            if item in value:return True
    for item in list3:
        for value in Disp_List:
            if item in value:return True
    return False        
def funct_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if event.widget["text"]=='':return
    if Answer_Err.get():return
    try:
        answer_was_present=False
        if Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
            answer=Answer.get()
            clear_all()
            answer_was_present=True
            for i, item in enumerate(answer):
                disp_update(item)
                expr_update(item)
        funct=event.widget["text"]
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        if Disp_List:# Prevent Double Constants
            if event.widget["text"] in _MyConstants and Disp_List[-1] in _MyConstants:return
        # Functions Requiring Data Entry First 
        if funct=='1/𝓧':
            if not Disp_List:return
            if Disp_List[-1] in Operators:return       
            reverse_value('disp',True) # Display 
            disp_update('{')
            disp_update('(')
            disp_update('1')    
            disp_update(' / ')
            value=return_value('disp',True,False) 
            disp_update(')')
            disp_update('}')
            reverse_value('expr',True) # Expression
            expr_update('{')
            expr_update('(')
            expr_update('1')    
            expr_update(' / ')
            value=return_value('expr',True,True)
            expr_update(')')
            expr_update('}')
        elif funct=='𝓧ʸ':# Expression = x**y, Display = x^y
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('(')
                return_value('disp',True,False)
                disp_update('^')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,False)
                expr_update('**')
        elif funct=='𝓧²' or funct=='𝓧³':
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('(')
                value=return_value('disp',True,False)
                disp_update('^')
                if funct=='𝓧²':disp_update('2')
                if funct=='𝓧³':disp_update('3')
                disp_update(')')
                disp_update('}')
                reverse_value('expr',True)
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,False)
                expr_update('**')
                if funct=='𝓧²':expr_update('2')
                if funct=='𝓧³':expr_update('3')
                expr_update(')')
                expr_update('}')
        elif funct=='ʸ√':# mpMath = root(x, y), Simplified = x**(1 / y), Display = ʸ√(x, y)
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                if Disp_List and Disp_List[-1]=='(':bracket=True
                else:bracket=False
                disp_update('{')
                disp_update('ʸ√')
                if not bracket:disp_update('(')
                value=return_value('disp',True,False) 
                disp_update(', ')
                reverse_value('expr',True) # Expression
                if Expr_List and Expr_List[-1]=='(':bracket=True
                else:bracket=False
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,True)
                expr_update('**')
                expr_update('(')
                expr_update('1')
                expr_update(' / ')
        elif funct=='²√'or funct=='³√':#sympify = x**(1 / 2), Display = ²√x, sympify = x**(1 / 3), Display = ³√x
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update(event.widget["text"])
                value=return_value('disp',True,True)
                disp_update('}')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                value=return_value('expr',True,True)
                expr_update('**') 
                expr_update('(')
                expr_update('1')
                expr_update(' / ')
                if funct=='²√':expr_update(' 2 ')
                if funct=='³√':expr_update(' 3 ')
                expr_update(')')
                expr_update(')')
                expr_update('}')
        elif funct=='n!': # Factorial Of n where n Is Natural Number And Positive, expr=factorial(n)
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in _MyConstants:
                reverse_value('disp',True) # Display
                disp_update('{')
                disp_update('fact')
                value=return_value('disp',True,True)
                disp_update('}')
                reverse_value('expr',True) # Expression
                expr_update('{')
                expr_update('(')
                expr_update('factorial')
                value=return_value('expr',True,True)
                expr_update(')')
                expr_update('}')
        elif funct=='%':
            if not Disp_List:return
            if Disp_List[-1] in Operators:return
            if not Disp_List[-1].isdecimal() or Disp_List[-1] in _MyConstants:return        
            disp_update('%') # Display
            reverse_value('expr',True) # Expression
            value=return_value('disp',False,True)
            expr=str(value+' * 0.01')    
            expr=parse_expr(expr, evaluate=False)# Change Reversed_List To Percent
            f=str(expr.evalf())
            for i in f:expr_update(i)# Recreate Expr_List With Calculated Percent
        elif funct=='mod':# a % b, remainder, expr = Mod(100, 21)= 16, Display = Mod(100, 21)
            if not Disp_List:return
            reverse_value('disp',True) # Display
            disp_update('{')
            disp_update('mod')
            disp_update('(')
            value=return_value('disp',True,False)
            if value=='break':
                mod_btn.config(state="normal")
                return
            disp_update(', ')
            reverse_value('expr',True) # Expression
            expr_update('{')
            expr_update('Mod')
            expr_update('(')
            value=return_value('expr',True,False)
            expr_update(', ')
        elif funct=='exp':# Scientific Notation
            if not Disp_List:return
            if type_isnumerical(Disp_List[-1]):
                reverse_value('disp',True)
                val1=return_value('disp',False,True)# Do Not Update
                val2=str(val1).replace('{','').replace('}','').replace('(','').replace(')','') # Remove Temp Brackets For Examination
                value=np.format_float_scientific(mpf(val2), unique=False, precision=Exp_Precision.get(), exp_digits=Exp_Digits.get())            
                disp_update(value)
                reverse_value('expr',True)
                expr_update(value)
        elif funct in _MyConstants: # Constants
            if not answer_was_present:
                if Disp_List: # End Strip All Brackets For Examination
                    allowed=['^','**',', ']
                    val=''.join(Disp_List)
                    val2 = str(val).replace('{','').replace('}','').replace('(','').replace(')','')
                    if val2!='':
                        if event.widget["text"] in _MyConstants and val2[-1].isdecimal() or \
                            val2[-1] in allowed or Disp_List[-1] in Operators or Disp_List[-1] in allowed:pass
                        else:return
                if funct=='Π₂':
                    disp_update(event.widget["text"])
                    expr_update('Π')
                    parsed=parse_expr('Π')
                else:
                    disp_update(event.widget["text"])
                    expr_update(event.widget["text"])
                    parsed=parse_expr(event.widget["text"], evaluate=False)
                Symbol_Names.append(parsed)
                if funct=='𝓔':Symbol_Values.append(mp.euler)
                elif funct=='π':Symbol_Values.append(mp.pi)
                elif funct=='𝜯':Symbol_Values.append(2*mp.pi)
                elif funct=='𝜱':Symbol_Values.append(mp.phi)
                elif funct=='𝑮':Symbol_Values.append(mp.catalan)
                elif funct=='𝜁3':Symbol_Values.append(mp.apery)
                elif funct=='𝑲':Symbol_Values.append(mp.khinchin)
                elif funct=='𝑨':Symbol_Values.append(mp.glaisher)
                elif funct=='𝑴':Symbol_Values.append(mp.mertens)
                elif funct=='Π₂':Symbol_Values.append(mp.twinprime)
                elif funct=='𝒆':Symbol_Values.append(mp.e)
            else:
                clear_all()
                disp_update(answer)
                expr_update(answer)
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' funct_clicked!'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def trig_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    if Disp_List[-1]=='^':return
    if Disp_List[-1] in Operators:return
    try:       
        if Answer_Present.get():# If Answer, Start Fresh With Answer As 1st Part Of Expression
            answer=Answer.get()
            clear_all()
            disp_update(answer)
            expr_update(answer)
        unit=Trig_Units.get()
        if unit=='Radians':unit_txt='ʳ'
        elif unit=='Degrees':unit_txt='ᵈ'
        elif unit=='Gradians':unit_txt='ᵍ'
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        # Display
        reverse_value('disp',True)
        disp_update('{')
        disp_update(event.widget["text"]+unit_txt)
        disp_value=return_value('disp',False,False)
        bkt=False
        if disp_value[0]=='{' and disp_value[-1]=='}':
            if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
        elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
        if not bkt:disp_update('(')
        disp_update(disp_value)
        if not bkt:disp_update(')')
        disp_update('}')
        # Expression
        reverse_value('expr',True)
        expr_update('{')
        expr_update(event.widget["text"])
        expr_value=return_value('expr',False,True)
        if unit=='Radians':
            expr_update(expr_value)
            expr_update('}')
            return
        if event.widget["text"][0]!='a': # (No arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
            if unit=='Degrees':# {sin(40 * (pi / 180))}, {sin((20 + 20) * (pi / 180))}
                parsed=parse_expr('rad_to_deg', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(mp.pi/180)
                expr_update('(')
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('rad_to_deg')
                expr_update(')')
            elif unit=='Gradians':# {sin(40 * (pi / 200))}, {sin((20 + 20) * (pi / 200))}          
                    parsed=parse_expr('rad_to_grad', evaluate=False)
                    Symbol_Names.append(parsed)
                    Symbol_Values.append(mp.pi/200)
                    expr_update('(')
                    expr_update(expr_value)
                    expr_update(' * ')
                    expr_update('rad_to_grad')
                    expr_update(')')
        elif event.widget["text"][0]=='a': # (arc) sin,cos,tan,sec,csc,cot,sinh,cosh,tanh,sech,csch,coth
            if unit=='Degrees':
                parsed=parse_expr('arc_rad_to_deg', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(180/mp.pi)
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('arc_rad_to_deg')
            elif unit=='Gradians':          
                parsed=parse_expr('arc_rad_to_grad', evaluate=False)
                Symbol_Names.append(parsed)
                Symbol_Values.append(200/mp.pi)
                expr_update(expr_value)
                expr_update(' * ')
                expr_update('arc_rad_to_grad')
        expr_update('}')
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' trig_clicked!'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def log_clicked(event):
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    if Disp_List[-1]=='^' or Disp_List[-1]==', ':return
    if Disp_List[-1] in Operators:return
    try:       
        if Answer_Present.get():# For Only Functions That Require Entry Before Function Click.
            answer=Answer.get()
            clear_all()
            disp_update(answer)
            expr_update(answer)
        if Math_Function.get()=='':Last_Function.set(event.widget["text"])
        else:Last_Function.set(Math_Function.get())    
        Math_Function.set(event.widget["text"])
        if event.widget["text"]=='log𝒆':text='log𝒆'     
        elif event.widget["text"]=='log10':text='log₁₀'     
        elif event.widget["text"]=='log(x,b)':text='log'
        # Display
        ret=reverse_value('disp',True)
        disp_update('{')
        disp_update(text)
        disp_value=return_value('disp',False,False)# Only Return Value
        bkt=False
        if disp_value[0]=='{' and disp_value[-1]=='}':
            if disp_value[1]=='(' and disp_value[-2]==')':bkt=True
        elif disp_value[0]=='(' and disp_value[-1]==')':bkt=True   
        # Expression
        reverse_value('expr',True)
        expr_update('{')
        expr_update('log')
        expr_value=return_value('expr',False,True)# Only Return Value
        if text=='log𝒆':    
            if not bkt:disp_update('(')
            disp_update(disp_value)
            if not bkt:disp_update(')')
            disp_update('}')
            expr_update(expr_value)
            expr_update('}')
        elif text=='log₁₀':
            if not bkt:disp_update('(')
            disp_update(disp_value)
            if not bkt:disp_update(')')
            disp_update('}')
            expr_update('(')
            expr_update(expr_value)
            expr_update(', ')
            expr_update('10')
            expr_update(')')
            expr_update('}')
        elif text=='log': #'log(x,b)'
            disp_update('(')
            disp_update(disp_value)
            disp_update(', ')
            expr_update('(')
            expr_update(expr_value)
            expr_update(', ')
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' log_clicked!'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def temp_clicked(event):# C = K - 273.15, C = (R - 491.67) * (5 / 9), C = (F - 32) * (5/9), F = 32 + (C / (5/9)) 
    base=Base.get()
    if base!='Decimal':return
    if not Disp_List:return
    try:
        if Answer_Present.get():
            newval=Answer.get()
            Answer_Present.set(False)
            disp_update('clear')
            expr_update('clear')
            disp_update(str(newval))
            expr_update(str(newval))
        reverse_value('expr',True)
        if event.widget["text"]=='°F→°C':
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' - 32) * (5 / 9')
            expr_update(')')
        elif event.widget["text"]=='°C→°F':
            expr_update('32 + ')
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' / (5 / 9)')
            expr_update(')')
        elif event.widget["text"]=='°K→°C':
            value=return_value('expr',True,True) 
            expr_update(' - ')
            expr_update('273.15')
        elif event.widget["text"]=='°R→°C':
            expr_update('(')
            value=return_value('expr',True,True) 
            expr_update(' - 491.67')
            expr_update(')')
            expr_update(' * (5 / 9)')
        equal_clicked(event)
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' temp_clicked!'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def bracket_clicked(how,which,status):
    if Answer_Present.get():return# Brackets Not Allowed If Answer Present
    if Answer_Err.get():return
    if  Disp_List and Disp_List[-1]=='^' and status=='close':return
    if status=='close' and Disp_List[-1]=='(':
        disp=Display.get()
        Display_Text.delete('1.0','end')
        Display_Text.insert('end',disp)
        Display.set(disp)
        return    
    unwanted_list=['-','.',',','!',')']
    disp_open=Disp_Bkts_Open.get()
    expr_open=Expr_Bkts_Open.get()
    try:
        # Avoid Unwanted Brackets
        if status=='open':
            if which=='disp' or which=='both':
                if Disp_List:
                    if type_isnumerical(Disp_List[-1]) or Disp_List[-1] in unwanted_list:
                        if Disp_List[-1]!='^':return
        elif status=='close' and how!='auto':
            if which=='disp' or which=='both':
                if Disp_List:
                    early_list=['(','.',',']
                    if Disp_List[-1]in early_list:return
                    if disp_open==0:return
        elif status=='clear': # Reset Brackets To Zero
            if which=='disp' or which=='both':
                Disp_Bkts_Open.set(0)
                Temp_Disp_Open.set(0)
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,'0'))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                Expr_Bkts_Open.set(0)
                Temp_Expr_Open.set(0)
            return
        if how=='manual': # Brackets Entered Manually By Click. Add Bracket And Increase Or Decrease Count   
            if which=='disp' or which=='both':
                disp_open=Disp_Bkts_Open.get()
                if status=='open':# Create New '('
                    disp_open+=1
                    disp_update('(','Some')
                    Disp_Bkts_Open.set(disp_open)
                elif status=='close':# Create New ')'
                    if disp_open > 0:
                        disp_update(')','Some')
                        disp_open-=1
                        Disp_Bkts_Open.set(disp_open)
                        disp_open=Disp_Bkts_Open.get()
                        td_open=Temp_Disp_Open.get()
                        if td_open>0 and disp_open==0:close_brackets('temp_disp')
                disp_open=Disp_Bkts_Open.get()
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,str(disp_open)))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                expr_open=Expr_Bkts_Open.get()
                if status=='open':# Create New '('
                    expr_open+=1
                    expr_update('(','Some')
                    Expr_Bkts_Open.set(expr_open)
                elif status=='close':# Create New ')'
                    if expr_open > 0:
                        expr_update(')','Some')    
                        expr_open-=1
                        Expr_Bkts_Open.set(expr_open)
                        expr_open=Expr_Bkts_Open.get()
                        disp_open=Disp_Bkts_Open.get()
                        if disp_open==0:
                            for i in range(expr_open):
                                expr=Expression.get()
                                expr_update(')','Some')
                                expr_open-=1
                                Expr_Bkts_Open.set(expr_open)
                            td_open=Temp_Expr_Open.get()
                            if td_open>0 and expr_open==0:close_brackets('temp_expr')
        elif how=='auto': # Brackets Entered Automatically By Expression. Only Increase Or Decrease Count.
            if which=='disp' or which=='both':
                disp_open=Disp_Bkts_Open.get()
                if status=='open':# Increase open count
                    disp_open+=1
                elif status=='close':# Decrease open count 
                    if disp_open > 0:
                        disp_open-=1
                Disp_Bkts_Open.set(disp_open)
                open_btn['text']='('+(convert_script(Normal_Script,Super_Script,str(disp_open)))# Convert To Superscript And Update Button
            if which=='expr' or which=='both':
                expr_open=Expr_Bkts_Open.get()
                if status=='open':expr_open+=1 # Increase open count
                elif status=='close':
                    if expr_open > 0:expr_open-=1 # Decrease open count
                Expr_Bkts_Open.set(expr_open)
        return        
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' bracket_clicked!'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def nround_answer(expr):# Use nstr In Conj. With Round.get() To Round Answer
    try:
        expr_answer=expr.evalf(mp.dps, subs=sub_dict)
        answer_str=str(expr_answer)
        rund=Round.get()
        n_str=''
        for i in answer_str:
            n_str=i+n_str
            if i=='.':break
            else:count=len(n_str)
        if '-' in answer_str:count-=1
        n=rund+count
        if rund>0:
            if type_isnumerical(answer_str):
                answer=nstr(mpf(expr_answer), n)
            else:answer=str(expr_answer) # Answer Isn't Numerical   
        else:answer=str(expr_answer) # No Rounding
        return answer # Return Value = n For nstr
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+' nround Function! Rounding Answer.'
        messagebox.showerror('Exeption Error', msg1+msg2)
        return 'break'
def equal_clicked(event):
    if not Disp_List:return
    if Answer_Err.get():return
    if Disp_List[-1]==' = ':return
    expr=Expression.get()
    close_brackets('all')# (Just In Case) Close All Opened Brackets Before Preceding
    sub_dict={}
    for i in range(len(Symbol_Names)):
        sub_dict[Symbol_Names[i]] = Symbol_Values[i]
    if not Answer_Present.get():
        try:
            constant=False
            expr=Expression.get()
            if expr in _MyConstants: constant=True
            exp=parse_expr(expr, evaluate=True)
            expr_answer=exp.evalf(mp.dps, subs=sub_dict)
            if not constant:answer=nround_answer(expr_answer)
            else:
                answer=str(expr_answer)
            if answer!='' or answer!=None:# Required 2 Entries (= And Answer)
                answer=set_numeric_type(answer) # Test For Valid Answer
                newval=answer
                disp_update(' = ')
                expr_update(' = ')
                if newval!='Invalid Type!'and newval!='Type is Imaginary Literal!':
                    base=Base.get()
                    if base=='Decimal':
                        Answer.set(newval)
                    elif base=='Hexadecimal':
                        hex=Convert_Base(10,16,str(newval))
                        Answer.set(hex)
                    elif base=='Octal':
                        oct=Convert_Base(10,8,str(newval))
                        Answer.set(oct)
                    elif base=='Binary':
                        bin=Convert_Base(10,2,str(newval))
                        Answer.set(bin)
                    Answer_Present.set(True)
                    Answer_Err.set(False)
                    disp_update(Answer.get())
                    expr_update(Answer.get())
                else:    
                    Answer.set('')
                    Answer_Present.set(False)
                    Answer_Err.set(True)
                    disp_update(str(newval))
                    expr_update(str(newval))
            Math_Function.set('')
            return
        except Exception:
            Answer.set('')
            Answer_Present.set(False)
            Answer_Err.set(True)
            disp_update(' = Invalid Entry!')
            expr_update(' = Invalid Entry!')
            return 'break'
def config_base(base):
    Base.set(base)
    if base=='Binary':
        base_btn[0].configure(bg='white', fg='navy')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,2):
            num_btn[num]['state']="normal"
        for num in range(2,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Octal':
        base_btn[3].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        for num in range(0,8):
            num_btn[num]['state']="normal"
        for num in range(8,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Decimal':
        base_btn[1].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[2].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,10):
            num_btn[num]['state']="normal"
        for num in range(10,16):
            num_btn[num]['state']="disabled"
        Display_Text.focus_force()    
        Display_Text.unbind('<period>')
        Display_Text.bind('<period>')
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item), lambda e: "break")
        root.focus_force()
        root.bind('<period>')
        for i, item in enumerate(Hex_List):
            root.bind(str(item), lambda e: "break")
    if base=='Hexadecimal':
        base_btn[2].configure(bg='white', fg='navy')
        base_btn[0].configure(bg='navy', fg='white')
        base_btn[1].configure(bg='navy', fg='white')
        base_btn[3].configure(bg='navy', fg='white')
        for num in range(0,16):
            num_btn[num]['state']="normal"
        Display_Text.focus_force()    
        Display_Text.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            Display_Text.unbind(str(item))
        for i, item in enumerate(Hex_List):
            Display_Text.bind(str(item))
        root.focus_force()
        root.bind(('<period>'), lambda e: "break")
        for i, item in enumerate(Hex_List):
            root.bind(str(item), numeric_clicked)
    return
def base_clicked(event):
    value=Disp_List
    exist=False
    if not Answer_Present.get():
        exist=function_check(value)
    if exist:return
    if value=='':return
    hex_values=['A','B','C','D','E','F']
    try:
        if Answer_Present.get():from_val=Answer.get()
        else:from_val=Display.get()
        if from_val=='':
            Base.set(event.widget["text"])
            config_base(event.widget["text"])
        elif from_val!='' and Base.get()!= event.widget["text"]:
            f_base=Base.get()# Get Present Base
            if f_base=='Binary':from_base=2
            elif f_base=='Octal':from_base=8
            elif f_base=='Decimal':from_base=10
            elif f_base=='Hexadecimal':from_base=16
            is_numerical=False
            disp=Display.get()
            for i in disp: # Examine Display String For Only Numerical Value
                if i.isdigit() or i in hex_values:is_numerical=True
                else:
                    is_numerical=False
                    break
            if Answer_Present.get() or is_numerical==True: # If Answer Or Only Numerical Value Exist Then Convert
                Answer_Present.set(False)
                Base.set(event.widget["text"])
                t_base=Base.get()    
                if t_base=='Binary':to_base=2
                elif t_base=='Octal':to_base=8
                elif t_base=='Decimal':to_base=10
                elif t_base=='Hexadecimal':to_base=16
                config_base(t_base)
                base_val=Convert_Base(from_base,to_base,from_val)
            else:return    
            # Pop Last Base Value From Both List And Replace With New Base Value
            disp_update('clear')
            if Answer.get():expr_update('clear')
            for i, item in enumerate(str(base_val)):
                disp_update(item)
            if Answer_Present.get():
                if from_base!=10:
                    answer_val=Convert_Base(from_base,10,from_val)
                else:
                    answer_val=from_val   
                for i, item in enumerate(str(answer_val)):
                    expr_update(item)
                Answer_Present.set(False)
                Answer.set('')    
        else: Base.set(event.widget["text"])   
        config_trig(Trig_Units.get())
        return
    except Exception as e:
        msg1='Exception occurred while code execution:\n'
        msg2= repr(e)+'base_clicked'
        msg3='\nPlease Check Entry Values!'
        messagebox.showerror('Exeption Error', msg1+msg2+msg3)
        return 'break'
def config_trig(unit):
    base=Base.get()
    Trig_Units.set(unit)
    if base=='Decimal':
        for num in range(0, len(unit_btn)):
            unit_btn[num]['state']="normal"
    else:    
        for num in range(0, len(unit_btn)):
            unit_btn[num]['state']="disabled"
    if unit=='Degrees':
        unit_btn[0].configure(bg='white', fg='green')
        unit_btn[1].configure(bg='green', fg='white')
        unit_btn[2].configure(bg='green', fg='white')
    elif unit=='Radians':
        unit_btn[1].configure(bg='white', fg='green')
        unit_btn[0].configure(bg='green', fg='white')
        unit_btn[2].configure(bg='green', fg='white')
    elif unit=='Gradians':
        unit_btn[2].configure(bg='white', fg='green')
        unit_btn[0].configure(bg='green', fg='white')
        unit_btn[1].configure(bg='green', fg='white')
    return    
def trig_unit_clicked(event):
    # Binding event Overrules Disabled State So Check State. If State = 'disabled' return
    base=Base.get() # Only Allow Conversions For Decimal Base
    if 'disabled' in event.widget.config('state') or base!='Decimal':return
    if Answer_Present.get():
        str_val=Answer.get()
    else:
        str_val=Display.get()
    if str_val=='':
        Trig_Units.set(event.widget["text"])
        config_trig(event.widget["text"])    
    from_angle=Trig_Units.get()
    if str_val!='':
        Trig_Units.set(event.widget["text"])
        unit=Trig_Units.get()
        config_trig(unit)
        is_numerical=False
        disp=Display.get()
        is_numerical=type_isnumerical(disp)
        if Answer_Present.get() or is_numerical: # If Answer Or Only Numerical Value Exist Then Convert
            val=Convert_Trig_Units(from_angle,unit,str_val)
            Answer_Present.set(False)
        else:return
        rund=Round.get()
        if rund>0:
            expr=str(val)
            exp=parse_expr(expr, evaluate=True)
            expr_answer=exp.evalf(mp.dps, subs=sub_dict)
            answer=nround_answer(expr_answer)
        else:answer=str(val)    
        Display.set(answer)
        Display_Text.delete('1.0','end')
        Display_Text.insert('end',answer)
        Answer_Present.set(True)
        Answer.set(answer)
    return    
def config_trig_btns(event):
    arc=Arc.get()
    hyp=Hyp.get()
    if event.widget["text"]=='Hyp':
        if hyp:
            Hyp.set(False)
            hyp=False
        else:
            Hyp.set(True)
            hyp=True
    elif event.widget["text"]=='Arc':        
        if arc:
            Arc.set(False)
            arc=False
        else:
            Arc.set(True)
            arc=True
    if not hyp and not arc:
        trig1=['sin','sec','cos','csc','tan','cot']
        for i, item in enumerate(trig1):
            trig_btn[i]['text']=item
        hyp_btn.configure(bg='green', fg='white')
        arc_btn.configure(bg='green', fg='white')
    elif hyp and not arc:
        trig2=['sinh','sech','cosh','csch','tanh','coth']
        for i, item in enumerate(trig2):
            trig_btn[i]['text']=item
        hyp_btn.configure(bg='white', fg='green')
        arc_btn.configure(bg='green', fg='white')
    elif not hyp and arc:
        trig3=['asin','asec','acos','acsc','atan','acot']
        for i, item in enumerate(trig3):
            trig_btn[i]['text']=item
        arc_btn.configure(bg='white', fg='green')
        hyp_btn.configure(bg='green', fg='white')
    elif hyp and arc:        
        trig4=['asinh','asech','acosh','acsch','atanh','acoth']
        for i, item in enumerate(trig4):
            trig_btn[i]['text']=item
        arc_btn.configure(bg='white', fg='green')
        hyp_btn.configure(bg='white', fg='green')
    return
def clear_entry(event):
    if Answer_Present.get():Answer_Present.set(False)
    if Disp_List and Expr_List:
        if Disp_List[-1]==Expr_List[-1] or Disp_List[-1]=='^' and Expr_List[-1]=='**': 
            last_element = Disp_List[-1]
            if last_element==')':bracket_clicked('auto','both','open')
            if last_element=='(':bracket_clicked('auto','both','close')
            if Disp_List:Disp_List.pop()
            if Expr_List:Expr_List.pop()
            e1=''.join([str(item) for item in Expr_List])
            Expression.set(e1)
            d1=''.join([str(item) for item in Disp_List])
            d2 = str(d1).replace('{','').replace('}','') # Remove Temp Brackets For Examination
            Display.set(d2)
            Display_Text.delete('1.0','end')
            Display_Text.insert('end',d2)
    else:clear_all()
def menu_popup2(event):# display the popup menu
    try: # This popup is used simular to tool tip
        popup2=Menu(root, tearoff=0)
        popup2.delete(0,'end')
        btn=event.widget['text']
        if event.type=='4': #<EventType.ButtonPress: '4'>
            if btn=='C':popup2.add_command(label='Clear All. Sets To Default',  background='aqua')
            elif btn=='CE':popup2.add_command(label='Clear Last Entry If Numeric and Base 10.', background='aqua')
            elif btn=='n!':popup2.add_command(label='Factorial of Positive Natural Number n.', background='aqua')
            elif btn=='𝜯':popup2.add_command(label='Constant tau (𝜯) = 2*π.', background='aqua')
            elif btn=='𝑮':popup2.add_command(label="Catalan's Constant (𝑮).", background='aqua')
            elif btn=='𝓔':popup2.add_command(label="Euler's Constant (𝓔)." , background='aqua')
            elif btn=='π':popup2.add_command(label='Constant PI (π).' , background='aqua')
            elif btn=='𝜁3':popup2.add_command(label="Apery's Constant (𝜁3).", background='aqua')
            elif btn=='𝒆':popup2.add_command(label='Natural Logarithm Base (𝒆).', background='aqua')
            elif btn=='𝜱':popup2.add_command(label='Golden Ratio (𝜱).', background='aqua')
            elif btn=='𝑲':popup2.add_command(label="Khinchin's Constant (𝑲).", background='aqua')
            elif btn=='𝑨':popup2.add_command(label="Glaisher's Constant (𝑨).", background='aqua')
            elif btn=='𝑴':popup2.add_command(label="Meissel-Mertens Constant (𝑴).", background='aqua')
            elif btn=='Π₂':popup2.add_command(label="Twin Prime Constant (Π₂).", background='aqua')
            elif btn=='ʸ√':popup2.add_command(label="Enter Value First Then Click Me. Then Enter Root (y) Value.", background='aqua')
            elif btn=='²√':popup2.add_command(label="Enter Value First Then Click Me.", background='aqua')
            elif btn=='³√':popup2.add_command(label="Enter Value First Then Click Me.", background='aqua')
            elif btn=='1/𝓧':popup2.add_command(label="Enter 𝓧 Value First Then Click Me.", background='aqua')
            elif btn=='𝓧ʸ':popup2.add_command(label="Enter 𝓧 Value First Then Click Me. Then Enter Power (y) Value.", background='aqua')
            elif btn=='𝓧³':popup2.add_command(label="Enter 𝓧 Value First Then Click Me.", background='aqua')
            elif btn=='𝓧²':popup2.add_command(label="Enter 𝓧 Value First Then Click Me.", background='aqua')
            elif btn=='%':popup2.add_command(label="Enter Value First Then Click Me.", background='aqua')
            elif btn=='mod':popup2.add_command(label="Modulo Returns Division Remainder. Enter Numerator Then Click Me.", background='aqua')
            elif btn=='exp':popup2.add_command(label="Changes Last Numeric Value To Scientific Notation.", background='aqua')
            elif btn=='CM':popup2.add_command(label="Clear All Memories.", background='aqua')
            elif btn=='ms1':popup2.add_command(label="Memory Set 1.", background='aqua')
            elif btn=='ms2':popup2.add_command(label="Memory Set 2.", background='aqua')
            elif btn=='ms3':popup2.add_command(label="Memory Set 3.", background='aqua')
            elif btn=='ms4':popup2.add_command(label="Memory Set 4.", background='aqua')
            elif btn=='mr1':popup2.add_command(label="Memory Recall 1.", background='aqua')
            elif btn=='mr2':popup2.add_command(label="Memory Recall 2.", background='aqua')
            elif btn=='mr3':popup2.add_command(label="Memory Recall 3.", background='aqua')
            elif btn=='mr4':popup2.add_command(label="Memory Recall 4.", background='aqua')
            elif btn=='log𝒆':popup2.add_command(label="Enter Value First Then Click Me.", background='aqua')
            elif btn=='log10':popup2.add_command(label="Enter Value First Then Click Me.", background='aqua')
            elif btn=='log(x,b)':popup2.add_command(label="Enter 𝓧 Value First Then Click Me. Then Enter Log Base", background='aqua')
            elif btn=='A : B':popup2.add_command(label="Calculate Ratios And Porportions.", background='aqua')
            elif btn=='∫':popup2.add_command(label="An Expression Must Be Present To Integrate.", background='aqua')
            elif btn=="f '(x)":popup2.add_command(label="An Expression Must Be Present To Differentiate.", background='aqua')
            elif btn=='°F→°C':popup2.add_command(label="Converts Degrees Fahrenheit To Degrees Celsius.", background='aqua')
            elif btn=='°C→°F':popup2.add_command(label="Converts Degrees Celsius To Degrees Fahrenheit.", background='aqua',)
            popup2.tk_popup(event.x_root, event.y_root,0)
        else: 
            popup2.delete(0,'end')
            popup2.grab_release()
    finally:#Release the grab
        popup2.grab_release()
def clear_all():
    Display.set('')
    Display_Text.delete('1.0','end')
    Math_Function.set('')
    Last_Function.set('')
    Disp_List.clear() 
    Disp_Bkts_Open.set(0)
    Temp_Disp_Open.set(0)
    Temp_Expr_Open.set(0)
    Reversed_List.clear()
    Expression.set('')
    Expr_List.clear()
    Expressions_Used.clear()  
    Expr_Bkts_Open.set(0)  
    bracket_clicked('auto','both','clear')
    Answer.set('')
    Answer_Present.set(False)
    Answer_Err.set(False)
    disp_update('clear') 
    expr_update('clear')
    free_sys_symbols()
def set_defaults():
    Init_Calculator('read')            
    mp.pretty==True
    Hyp.set(False)  
    Arc.set(False)
    config_base('Decimal')     
    config_trig('Degrees')
    clear_all()
def calculator_resize(event): # Change Font Sizes According To Root Width vs Root Height
    Window_State.set(root.state())
    x_ratio=round(((root.winfo_width()/screen_width)*10), 1) # Screen To Window X Ratio
    y_ratio=round(((root.winfo_height()/screen_height)*10), 1)# Screen To Window Y Ratio
    wid_hgt_min,wid_hgt_xmax,wid_hgt_ymax=1,10,9.8
    fontsize_min,fontsize_max=5,30 # Min Font Size = 5, Norm = 12, Max = 30. Based On Porportions
    fontrange=fontsize_max-fontsize_min
    xrange=wid_hgt_xmax-wid_hgt_min
    yrange=wid_hgt_ymax-wid_hgt_min
    kx=abs(fontrange/xrange) # Porportion X KFactor
    fontsize_x=int(fontsize_min-(kx*(wid_hgt_min-x_ratio)))
    ky=abs(fontrange/yrange) # Porportion Y KFactor
    fontsize_y=int(fontsize_min-(ky*(wid_hgt_min-y_ratio)))
    if fontsize_x<=fontsize_y:font_size=fontsize_x # Champion Is Smallest Font Of The 2
    elif fontsize_y<=fontsize_x:font_size=fontsize_y
    if font_size<6:font_size=6
    if root.state()=='zoomed':
        display_font.config(size=NewFont_Size.get()*2)
    else:display_font.config(size=NewFont_Size.get())    
    root.font.config(size=font_size-3)
    special_font.config(size=font_size)
    normal_font.config(size=font_size)
    num_font.config(size=font_size+2)
    bracket_font.config(size=font_size+6)
    big_font.config(size=font_size+12)
    calculus_font.config(size=font_size+4)
    calculus2_font.config(size=font_size+4)
    func_btn[0].config(font=font.Font(family='lucidas', size=font_size, weight='normal', slant='italic'))
    return
def copy_display():
    try:# popup menu item Copy Total Display Text To Clip-Board
        text=Display.get()
        if text!='':
            os.system("echo.%s|clip" % text)
            clipboard_msg=Label(root, text=" Display Text Copied To Clipboard! ",background="#33FFFF", 
                foreground='#000000',highlightthickness=4,highlightbackground = "#FFFFFF", highlightcolor= "#FFFFFF",font=bracket_font)
            clipboard_msg.place(x=root_wid/5, y=10)
            root.after(2000, clipboard_msg.destroy)
    except tk.TclError:# No selection was made
        pass
    return "break"
def copy_selected(event:tk.Event=None) -> str:
    try:# Ctrl+c Copy Selected Display Text To Clip-Board
        if event.keysym=='c':
            text=Display_Text.selection_get()
            os.system("echo.%s|clip" % text)
            clipboard_msg=Label(root, text=" Selected Text Copied To Clipboard! ",background="#33FFFF", 
                foreground='#000000',highlightthickness=4,highlightbackground = "#FFFFFF", highlightcolor= "#FFFFFF",font=bracket_font)
            clipboard_msg.place(x=root_wid/5, y=10)
            root.after(2000, clipboard_msg.destroy)
    except tk.TclError:# No selection was made
        pass
    return "break"
if __name__ == "__main__":
    root=tk.Tk()
    #root.update_idletasks()
    dir=pathlib.Path(__file__).parent.absolute()
    filename='pycal.ico' # Program icon
    ico_path=os.path.join(dir, filename)
    root.iconbitmap(default=ico_path) # root and children
    root.font=font.Font(family='lucidas', size=10, weight='bold', slant='roman')
    display_font=font.Font(family='Lucida Sans', size=14, weight='normal', slant='italic')
    special_font=font.Font(family='lucidas', size=12, weight='normal', slant='roman')
    normal_font=font.Font(family='lucidas', size=12, weight='bold', slant='italic')
    num_font=font.Font(family='lucidas', size=14, weight='normal', slant='italic')
    calculus2_font=font.Font(family='lucidas', size=16, weight='normal', slant='italic')
    bracket_font=font.Font(family='lucidas', size=18, weight='normal', slant='roman')
    big_font=font.Font(family='lucidas', size=24, weight='normal', slant='roman')
    calculus_font=font.Font(family='lucidas', size=18, weight='bold', slant='italic')
    user=os.getlogin()
    title='pySci Calculator'
    options='Right Click Display For Options'
    root.title(title + options.rjust(40+len(options)))
    monitor_info = GetMonitorInfo(MonitorFromPoint((0,0)))
    work_area = monitor_info.get("Work")
    monitor_area = monitor_info.get("Monitor")
    screen_width=work_area[2]
    screen_height=work_area[3]
    taskbar_hgt=(monitor_area[3]-work_area[3])
    root_hgt = screen_height/2-taskbar_hgt
    root_wid=((screen_width*root_hgt)/screen_height)/1.27
    root.configure(bg='#14fafa')
    root.option_add('*TCombobox*Listbox.font', root.font)
    root.protocol("WM_DELETE_WINDOW", calculator_destroy)
    # Bind Keyboard Keys
    root.bind("<Return>", equal_clicked)
    root.bind("<BackSpace>", clear_entry)
    for i in range(10):
        root.bind(str(i), numeric_clicked)
    root.bind("<period>", numeric_clicked)
    Hex_List=['a','A','b','B','c','C','d','D','e','E','f','F']
    for i, item in enumerate(Hex_List):
        root.bind(str(item), numeric_clicked)
    Operators2=['/','*','-','+'] # Bind Keyboard Operator Keys
    for i, item in enumerate(Operators2):
        root.bind(str(item), operator_clicked)
    root.bind("(", lambda event, a='manual', b='both', c='open':bracket_clicked(a,b,c))
    root.bind(")", lambda event, a='manual', b='both', c='close':bracket_clicked(a,b,c))
    # ****Variables And Widgets****
    Display=StringVar()# Text Shown On Display (Advancing Display Update)
    Display.set('')
    Disp_List=[]# Final Display Not Shown
    Reversed_List=[] # Display Or Expression List Reversed
    Disp_Bkts_Open=IntVar()# Number Of Display Brackets Open
    Temp_Disp_Open=IntVar()# Used To Highlight Total Display Function.
    Expression=StringVar()# Advancing Expression Update
    Expr_List=[]# Final Expression Sent To Parser
    Expressions_Used=[]
    Symbol_Names=[]
    Symbol_Values=[]
    Symbols_Used=[]
    sub_dict={}
    Expr_Bkts_Open=IntVar()# Number Of Expression Brackets Open
    Temp_Expr_Open=IntVar()# Used To Highlight Total Expression Function. 
    Math_Function=StringVar()
    Last_Function=StringVar()
    D_Memory1=[]
    D_Memory2=[]
    D_Memory3=[]
    D_Memory4=[]
    E_Memory1=[]
    E_Memory2=[]
    E_Memory3=[]
    E_Memory4=[]
    Exp_Precision=IntVar()
    Round=IntVar()
    Exp_Digits=IntVar()
    Bit_Size=IntVar()
    NewFont=StringVar()
    NewFont_Size=IntVar()
    Window_State=StringVar()
    Answer=StringVar()# Parsed Answer
    Answer_Err=BooleanVar()
    Answer_Present=BooleanVar()# Answer Received And Present
    Normal_Script="0123456789"
    Super_Script="⁰¹²³⁴⁵⁶⁷⁸⁹"
    Sub_Script="₀₁₂₃₄₅₆₇₈₉"
    _MyClash=['pi','beta','gamma','zeta','radian','C','O','Q','N','I','E','S']
    _MyConstants=['𝓔','𝑮','𝜱','𝜯','𝑲','𝑨','𝑴','π','𝒆','𝜁3','Π₂','Π','rad_to_deg','rad_to_grad','arc_rad_to_deg','arc_rad_to_grad']
    ####### Widgets #######
    Display_bg=StringVar()
    Display_fg=StringVar()
    Display_bg.set('#0c012e')
    Display_fg.set('#ffffff')
    Display_Text=ScrolledText(root, bg=Display_bg.get(), fg=Display_fg.get(), font=display_font, 
            borderwidth=5, relief="sunken")
    Display_Text.place(relx=0.015, rely=0.01, relwidth=0.97, relheight=0.16)
    Display_Text.bind("<Control-c>", copy_selected)    
    Display_Text.delete('1.0','end')
    Unbound_Keys='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&{[}]|:;",?~`'
    for i, item in enumerate(Unbound_Keys): # Prevent Unwanted Keyboard Keys From Appearing In Display
        if item in Unbound_Keys:
            Display_Text.bind(str(item), lambda e: "break")
    popup=Menu(Display_Text, tearoff=0) # PopUp Menu
    popup.add_command(label="Calculator Precision", background='aqua', command=lambda:precision('dp'))
    popup.add_command(label="Round Answer", background='aqua', command=lambda:precision('round'))
    popup.add_command(label="Scientific Notation Precision", background='aqua', command=lambda:precision('exp'))
    popup.add_command(label="Exponential Notation Precision", background='aqua', command=lambda:precision('exp_digits'))
    popup.add_command(label="Binary Bit Size (8, 16, 32, 64, 128)", background='aqua', command=lambda:precision('bit_size'))
    popup.add_command(label="Display Font", background='aqua', command=lambda:choose_font())
    popup.add_command(label="Display Font Color", background='aqua', command=lambda:choose_color('fg'))
    popup.add_command(label="Display Background Color", background='aqua', command=lambda:choose_color('bg'))
    popup.add_command(label="Copy Display Text To Clipboard", background='aqua', command=lambda:copy_display())
    popup.add_command(label="About pySci Calculator", background='aqua', command=lambda:about())
    Display_Text.bind("<Button-3>", menu_popup)
    base_btn=[] 
    Base=StringVar()
    text=['Binary','Decimal','Hexadecimal','Octal']
    wid=[0.19,0.21,0.32,0.17]
    x=[0.02,0.23,0.46,0.8]
    hgt=0.72
    y=0.14
    base_frame=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Base Buttons
    base_frame.place(relx=0.015, rely=0.19, relwidth=0.479, relheight=0.092)
    for num in range(0,len(text)):
        base_btn.append([num])
        base_btn[num]=tk.Button(base_frame, text=text[num], background='navy', foreground = '#ffffff', # Base Buttons
            borderwidth=5, relief="raised", font=root.font)
        base_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        base_btn[num].bind("<Button-1>", base_clicked)
    unit_btn=[]
    Trig_Units=StringVar()
    text=['Degrees','Radians','Gradians']
    wid=[0.29,0.29,0.29,0.294]
    x=[0.03,0.35,0.67]
    y=0.14
    hgt=0.72            
    unit_frame=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Trig Units Buttons
    unit_frame.place(relx=0.506, rely=0.19, relwidth=0.36, relheight=0.092)
    for num in range(0,len(text)):
        unit_btn.append([num])
        unit_btn[num]=tk.Button(unit_frame, text=text[num], background="green", foreground = '#ffffff', # Trig Units Buttons
            borderwidth=5, relief="raised", font=root.font)
        unit_btn[num].place(relx=x[num], rely=y, relwidth=wid[num], relheight=hgt)
        unit_btn[num].bind("<Button-1>", trig_unit_clicked)
    clrmem_btn=tk.Button(root, text='CM', background="#ffff99", foreground = 'maroon', # Clear Memory Button
            borderwidth=5, relief="raised", font=num_font, command=lambda:clear_memories())
    clrmem_btn.place(relx=0.886, rely=0.19, relwidth=0.085, relheight=0.092)
    popup2=Menu(clrmem_btn, tearoff=0)
    clrmem_btn.bind("<Button-3>", menu_popup2)
    pad_fra=Frame(root, bg='#999999', borderwidth=2, relief="sunken") # Frame For Key Pad
    pad_fra.place(relx=0.015, rely=0.3, relwidth=0.97, relheight=0.68)    
    num_btn=[]
    y,x1,x2=0.015,0.01,0.098
    for num in range(0,10):# Numbers 0 - 9
        num_btn.append([num])
        if (num % 2)==0:x=x1# Even 
        else:x=x2 
        num_btn[num]=tk.Button(pad_fra, text=num, bg='navy', fg = '#ffffff', # Number Buttons
            activebackground='#ffffff', borderwidth=5, relief="raised", font=num_font)
        num_btn[num].place(relx=x, rely=y, relwidth=0.08, relheight=0.12)
        num_btn[num].bind("<Button-1>", numeric_clicked) # Bind all the number keys with the callback function
        if (num % 2)!=0:y+=0.14# Odd
    x=[0.01,0.1,0.19,0.28,0.39,0.5]
    wid=[0.08,0.08,0.08,0.1,0.1,0.1]    
    text=['A','B','C','D','E','F'] # Hex Numbers A - F
    for num in range(10,16):
        num_btn.append([num])
        num_btn[num]=tk.Button(pad_fra, text=text[num-10], background='navy', foreground = '#ffffff', # Hex Buttons
            borderwidth=5, relief="raised", font=num_font)
        num_btn[num].place(relx=x[num-10], rely=y, relwidth=wid[num-10], relheight=0.12)
        num_btn[num].bind("<Button-1>", numeric_clicked)
    operator_btn=[]
    x=0.19
    y=0.015
    wid=0.08
    hgt=0.12
    Operators=[' / ',' * ',' - ',' + '] # Math Operators
    for num in range(0,len(Operators)):
        operator_btn.append([num])
        operator_btn[num]=tk.Button(pad_fra, text=Operators[num], background="whitesmoke", foreground = 'navy',
            activebackground='#ffe599', borderwidth=5, relief="raised", font=big_font)
        operator_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        operator_btn[num].bind("<Button-1>", operator_clicked)
        y+=0.14
    equal_btn=tk.Button(pad_fra, text=' = ', background="#14fafa", foreground = 'navy', # Equal Button
        borderwidth=5, relief="raised", font=big_font)
    equal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    equal_btn.bind("<Button-1>", equal_clicked)
    Logs,log_btn=[],[]
    text=['log𝒆','log10','log(x,b)']
    x=0.28
    y=0.015
    wid=0.1
    hgt=0.12
    for num in range(0,len(text)):
        Logs.append(StringVar(master=None))
        log_btn.append([num])
        log_btn[num]=tk.Button(pad_fra, text=text[num], background="purple", foreground = 'whitesmoke', # Log Buttons
            borderwidth=5, relief="raised", font=root.font)
        log_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        log_btn[num].bind("<Button-1>", log_clicked)
        log_btn[num].bind("<Button-3>", menu_popup2)
        Logs[num].set(num)
        y+=0.14
    sign_btn=tk.Button(pad_fra, text=chr(177), background='navy', foreground = 'whitesmoke', # Sign (Plus Or Minus) 
            borderwidth=5, relief="raised", font=big_font)
    sign_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    sign_btn.bind("<Button-1>", sign_clicked)
    y+=0.14
    decimal_btn=tk.Button(pad_fra, text=chr(46), background='navy', foreground = 'whitesmoke', # Decimal Point 
            borderwidth=5, relief="raised", font=big_font)
    decimal_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    decimal_btn.bind("<Button-1>", numeric_clicked)
    y+=0.14
    Trig,trig_btn=[],[]
    odd_list=['sec','csc','cot']
    text=['sin','sec','cos','csc','tan','cot']
    x1=0.39
    x2=0.5
    y=0.015
    wid=0.1
    hgt=0.12
    for num in range(0,len(text)):
        Trig.append(StringVar(master=None))
        trig_btn.append([num])
        if text[num] in odd_list:x=x2
        else:x=x1
        trig_btn[num]=tk.Button(pad_fra, text=text[num], background="green", foreground = 'whitesmoke', # Trig Buttons
            borderwidth=5, relief="raised", font=root.font)
        trig_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        trig_btn[num].bind("<Button-1>", trig_clicked)
        trig_btn[num].bind("<Button-3>", menu_popup2)
        Trig[num].set(num)
        if text[num] in odd_list:y+=0.14
    odd_list.clear()    
    Arc=BooleanVar()
    arc_btn=tk.Button(pad_fra, text='Arc', background="green", foreground = 'whitesmoke', # Trig Arc Button
        borderwidth=5, relief="raised", font=root.font)
    arc_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
    arc_btn.bind("<Button-1>", config_trig_btns)
    Hyp=BooleanVar()
    hyp_btn=tk.Button(pad_fra, text='Hyp', background="green", foreground = 'whitesmoke', # Trig Hyp Button
        borderwidth=5, relief="raised", font=root.font)
    hyp_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
    hyp_btn.bind("<Button-1>", config_trig_btns)
    x1=0.39
    x2=0.5
    y+=0.14
    open_btn=tk.Button(pad_fra, text='('+chr(8304), background='whitesmoke', foreground = 'black', # Parenthesis Open Button
        activebackground='#ffe599', borderwidth=5, relief="raised", font=bracket_font)
    open_btn.place(relx=x1, rely=y, relwidth=wid, relheight=hgt)
    open_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='open':bracket_clicked(a,b,c))
    closed_btn=tk.Button(pad_fra, text=')', background='whitesmoke', foreground = 'black',  # Parenthesis Close Button
        activebackground='#ffe599', borderwidth=5, relief="raised", font=bracket_font)
    closed_btn.place(relx=x2, rely=y, relwidth=wid, relheight=hgt)
    closed_btn.bind("<Button-1>", lambda event, a='manual', b='both', c='close':bracket_clicked(a,b,c))
    x=0.61
    y=0.015
    wid=0.08
    hgt=0.12
    func_btn=[]
    text=['1/𝓧','𝓧ʸ','𝓧³','𝓧²','n!','𝜯','𝑮']
    for num in range(0,len(text)): # Function Buttons Column 1
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[num], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
    func_btn[0].config(font=font.Font(family='lucidas', size=12, weight='normal', slant='italic'))
    clr=tk.Button(pad_fra, text='C', background="whitesmoke", foreground = 'black', # Clear Button
            activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font, command=lambda:clear_all())
    clr.place(relx=0.7, rely=0.015, relwidth=0.09, relheight=0.12)
    popup2=Menu(clr, tearoff=0)
    clr.bind("<Button-3>", menu_popup2)
    x=0.7
    y=0.155
    wid=0.09
    hgt=0.12
    text=['ʸ√','³√','²√','𝓔','π','𝜁3']
    i=0
    for num in range(6,12): # Function Buttons Column 2
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
        i+=1
    func_btn[6]['font']=special_font
    ce=tk.Button(pad_fra, text='CE', background="whitesmoke", foreground = 'black', # Clear Entry Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font)
    ce.place(relx=0.8, rely=0.015, relwidth=0.09, relheight=0.12)
    popup2=Menu(ce, tearoff=0)
    ce.bind("<Button-1>", clear_entry)
    ce.bind("<Button-3>", menu_popup2)
    x=0.8
    y=0.155
    wid=0.09
    hgt=0.12
    text=['%','𝑴','Π₂','𝒆','𝜱','𝑲','𝑨']
    i=0
    for num in range(12,18): # Function Buttons Column 3
        func_btn.append([num])
        func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
                activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font)
        func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        func_btn[num].bind("<Button-1>", funct_clicked)
        popup2=Menu(func_btn[num], tearoff=0)
        func_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
        i+=1
    func_btn[15]['font'] = bracket_font       
    x=0.9
    y-=0.14
    func_btn.append([num])
    func_btn[num]=tk.Button(pad_fra, text=text[i], background="whitesmoke", foreground = 'black', 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=num_font)
    func_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    func_btn[num].bind("<Button-1>", funct_clicked)
    popup2=Menu(func_btn[num], tearoff=0)
    func_btn[num].bind("<Button-3>", menu_popup2)
    mem_btn=[]
    x=0.9
    y=0.015
    wid=0.09
    hgt=0.12
    text=['ms1','ms2','ms3','ms4']
    for num in range(0,len(text)): 
        mem_btn.append([num])
        mem_btn[num]=tk.Button(pad_fra, text=text[num], background="#ffff99", foreground = 'maroon', # Memory Buttons 
                borderwidth=5, relief="raised", font=normal_font)
        mem_btn[num].place(relx=x, rely=y, relwidth=wid, relheight=hgt)
        mem_btn[num].bind("<Button-1>", memory_clicked)
        popup2=Menu(mem_btn[num], tearoff=0)
        mem_btn[num].bind("<Button-3>", menu_popup2)
        y+=0.14
    mod_btn=tk.Button(pad_fra, text='mod', background="whitesmoke", foreground = 'black', # Modulo Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=normal_font)
    mod_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    mod_btn.bind("<Button-1>", funct_clicked)
    popup2=Menu(mod_btn, tearoff=0)
    mod_btn.bind("<Button-3>", menu_popup2)
    y+=0.14
    exp_btn=tk.Button(pad_fra, text='exp', background="whitesmoke", foreground = 'black', # EXP Button 
            activebackground='#ffe599', borderwidth=5, relief="raised", font=normal_font)
    exp_btn.place(relx=x, rely=y, relwidth=wid, relheight=hgt)
    exp_btn.bind("<Button-1>", funct_clicked)
    popup2=Menu(exp_btn, tearoff=0)
    exp_btn.bind("<Button-3>", menu_popup2)
    ftoc_btn=tk.Button(pad_fra, text='°F→°C', background='#ff9c95', foreground = 'black', # °F→°C Button
        borderwidth=5, relief="raised", font=root.font)
    ftoc_btn.place(relx=0.01, rely=0.855, relwidth=0.117, relheight=0.12)
    ftoc_btn.bind("<Button-1>", temp_clicked)
    ftoc_btn.bind("<Button-3>", menu_popup2)
    ctof_btn=tk.Button(pad_fra, text='°C→°F', background='#ff9c95', foreground = 'black', # °C→°F Button
        borderwidth=5, relief="raised", font=root.font)
    ctof_btn.place(relx=0.137, rely=0.855, relwidth=0.117, relheight=0.12)
    ctof_btn.bind("<Button-1>", temp_clicked)
    ctof_btn.bind("<Button-3>", menu_popup2)
    ratio_btn=tk.Button(pad_fra, text='A : B', background='whitesmoke', foreground = 'black', # Ratios
        activebackground='#ffe599', borderwidth=5, relief="raised", font=normal_font, command=lambda:Ratio_Calculator())
    ratio_btn.place(relx=0.264, rely=0.855, relwidth=0.117, relheight=0.12)
    ratio_btn.bind("<Button-3>", menu_popup2)
    integrate_btn=tk.Button(pad_fra, text='∫', background='whitesmoke', foreground = 'black', # Integration ∫
        activebackground='#ffe599', borderwidth=5, relief="raised", font=calculus_font, command=lambda:Calculus('integrate'))
    integrate_btn.place(relx=0.39, rely=0.855, relwidth=0.1, relheight=0.12)
    integrate_btn.bind("<Button-3>", menu_popup2)
    diff_btn=tk.Button(pad_fra, text="f '(x)", background='whitesmoke', foreground = 'black',
        activebackground='#ffe599', borderwidth=5, relief="raised", font=calculus2_font, command=lambda:Calculus('differentiate')) # Differentiation
    diff_btn.place(relx=0.5, rely=0.855, relwidth=0.1, relheight=0.12)
    diff_btn.bind("<Button-3>", menu_popup2)
    text=[]
    set_defaults()
    root.mainloop()

