import tkinter
from tkinter import *
from tkinter import messagebox ,ttk,simpledialog
import algoritmo as C
from pathlib import Path
import os
import win32file
import win32con
os.system("cls")

ABOUT_TEXT = """
╔════════════╗
║ Create by Space Invader!..♥║
╚════════════╝
20-11-2020

"""

INSTRU = """Instrucciones:
-Debe ingresar la nota minima para pasar su ramo.
-Las notas que usted ingrese pueden ser con o sin
 ponderacion. 
-Puede agregar espacios correspondiente a la cantidad de 
 notas que desee calcular con un máximo de 8 notas. (Si
 cometió un error puede Quitar el espacio).
-Los rangos de notas van desde el '0' al '100'.
-Si desconoce su nota puede dejar el espacio en blanco, 
 el programa le dirá que notas necesita para pasar su materia.
-Las ponderaciones no pueden estar vacias ni la suma exceder
 el 100%
 
 Suerte:)
"""
def about():
    toplevel = Toplevel()
    toplevel.title("Acerca de...")
    toplevel.resizable(False, False)
    label1 = Label(toplevel, text=ABOUT_TEXT, height=6, width=34, padx=1, pady=1)
    label1.pack(fill='both')

def instrucciones():
    messagebox.askokcancel("Instrucciones",INSTRU)

def agregar():
    if raiz.counter > len(Entry_Nota)-1:
        raiz.counter = len(Entry_Nota)-1
    Entry_Nota[raiz.counter].config(state="normal")
    if Button_SPond.winfo_ismapped() and Button_CPond.winfo_ismapped() == False:
        Entry_Pond[raiz.counter].config(state="normal")
    raiz.counter +=1

def quitar():
    raiz.counter -=1
    if raiz.counter < 1:
        raiz.counter = 1
    Entry_Nota[raiz.counter].delete(0,"end")
    Entry_Nota[raiz.counter].config(state="disabled", disabledbackground="grey85" )
    Entry_Pond[raiz.counter].delete(0,"end")
    Entry_Pond[raiz.counter].config(state="disabled", disabledbackground="grey85" )

def activar():
    Button_CPond.grid_forget()
    for i in range(len(Entry_Pond)):
        if (Entry_Nota[i]['state']=="normal"):
            Entry_Pond[i].config(state="normal")
    Button_SPond.grid(row=2,column=0, padx=5, pady=5)
def desactivar():
    Button_SPond.grid_forget()
    for i in range(len(Entry_Pond)):
        Entry_Pond[i].config(state="disabled", disabledbackground="grey85")
    Button_CPond.grid(row=2,column=0, padx=5, pady=5)

def limpiar():
    Respuesta.configure(state="normal")
    for i in range(0,len(Entry_Nota)):
        Entry_Nota[i].configure(state="normal")
        Entry_Nota[i].delete(0,"end")
        Entry_Pond[i].configure(state="normal")
        Entry_Pond[i].delete(0,"end")
        quitar()
        if i > 0 :
            Entry_Nota[i].configure(state="disabled")
            Entry_Pond[i].configure(state="disabled")
        if Button_CPond.winfo_ismapped() and i == 0:
            Entry_Pond[0].configure(state="disabled")
    Respuesta.delete("1.0", "end")
    Entry_NotaMinima.delete(0, "end")
    Text_Ramo.delete(0, "end")
    Entry_NotaMinima.focus()
    Respuesta.configure(state="disabled")
def calcular():
    if Button_SPond.winfo_ismapped():
        pond_exist = 'S'
    else:
        pond_exist = 'N'
    if errors(0):
        registro_notas = []
        for i in range(raiz.counter):
            if Entry_Pond[i].get().isdigit():
                registro_notas.append([Entry_Nota[i].get(),str(int(Entry_Pond[i].get())/100)])
            else:
                registro_notas.append([Entry_Nota[i].get(),""])

        ramo = C.Calculadora(int(Entry_NotaMinima.get()),
        raiz.counter,
        pond_exist,
        registro_notas
        )
        Respuesta.insert("insert",C.Calculadora.calculo(ramo))
        Respuesta.configure(state="disabled")

def actualizar():
    matriz_ramos = ['Seleccione Ramo...']
    notas = open("notas.dat","r+")
    registros = notas.readline()
    while registros != "":
        registros = registros.strip().split(";")
        matriz_ramos.append(registros[0])
        registros = notas.readline()
    ComboBox_Ramos.config(values=matriz_ramos)
    ComboBox_Ramos.current(0)
    notas.close()

def seleccionar(event):
    limpiar()
    j = 3
    with open("notas.dat") as f:
        for line in f:
            if ComboBox_Ramos.get() in line:
                ramo = line.strip().split(";")
                Entry_NotaMinima.insert(0,ramo[2])
                if ramo[1] == 'S':
                    for i in range(int((len(ramo)-3)/2)):
                        activar()
                        Entry_Nota[i].insert(0,str(ramo[j]))
                        j+=1
                        Entry_Pond[i].insert(0,str(ramo[j]))
                        j+=1
                        agregar()

                else:
                    desactivar()
                    for i in range(int((len(ramo)-3)/2)):
                        Entry_Nota[i].insert(0,str(ramo[j]))
                        j+=2
                        agregar()
        quitar()
    f.close()

def errors(save):
    Respuesta.configure(state="normal")
    Respuesta.delete("1.0", "end")
    pond = 0
    for j in range(raiz.counter):
        if  Text_Ramo.get() == "" and save == 1:
            Respuesta.insert("insert","Debe ingresar nombre del ramo")
            return False
        if  Entry_NotaMinima.get() == "":
            Respuesta.insert("insert","Debe ingresar nota minima")
            return False
        if Entry_Pond[j].get() == "" and Button_SPond.winfo_ismapped():
            Respuesta.insert("insert","Debe ingresar ponderaciones")
            return False
        elif Button_SPond.winfo_ismapped():
            pond = pond + int(Entry_Pond[j].get())
        if pond > 100:
            Respuesta.insert("insert","Ponderaciones no pueden ser mayor a 100")
            return False
    return True

def guardar():
    
    if errors(1):
        Respuesta.configure(state="disabled")
        datos = []
        datos.append(Text_Ramo.get().upper())
        if Button_SPond.winfo_ismapped():
            datos.append("S")
        else:
            datos.append("N")
        datos.append(Entry_NotaMinima.get())
        for i in range(raiz.counter):
            if Entry_Nota[i]['state'] == tkinter.NORMAL:
                if Entry_Nota[i].get() == "":
                    nota = "-"
                else:
                    nota = Entry_Nota[i].get()
            if Entry_Pond[i]['state'] == tkinter.NORMAL:
                pond = Entry_Pond[i].get()
            else:
                pond = "-"
            datos.extend([nota,pond])
        new = ";".join(datos)
        os.system('attrib -h notas.dat')
        if Text_Ramo.get().upper() in ComboBox_Ramos['values']:
            notas = open("notas.dat", "r")
            buffer = notas.readlines()
            notas.close()
            notas = open("notas.dat", "w")
            for i in range(len(buffer)):
                buscar = buffer[i].find(";")
                if Text_Ramo.get().upper() == buffer[i][0:buscar]:
                    answer = messagebox.askokcancel("Advertencia",
                    "Está apunto de modificar notas del ramo '"+Text_Ramo.get().upper()+
                    "', ¿Desea continuar?")
                    if answer:
                        buffer[i] = new + "\n"
                        notas.write(buffer[i])
                        messagebox.showinfo("Información","Nota cambiada exitosamente")
                    else:
                        notas.write(buffer[i])
                        messagebox.showinfo("Información","Notas mantenida")
                else:
                    notas.write(buffer[i])
            notas.close()
        else:
            archivo = open ("notas.dat","a")
            archivo.write(new + "\n")
            archivo.close()
            messagebox.showinfo("Información","Notas ingresadas correctamente")
        os.system('attrib +h notas.dat')

def eliminar():
    answer = simpledialog.askstring("Input",
    "Escriba nombre del ramo que desee eliminar",
    parent=raiz).upper()
    os.system('attrib -h notas.dat')
    if answer in ComboBox_Ramos['values']:
        ramos = open("notas.dat", "r")
        buffer = ramos.readlines()
        ramos.close()
        ramos = open("notas.dat", "w")
        for ramo in range(len(buffer)):
            buscar = buffer[ramo].find(";")
            if answer == buffer[ramo][0:buscar]:
                messagebox.showinfo("Información","Se ha borrado '"+ answer+"'")
            else:
                ramos.write(buffer[ramo])
        ramos.close()
        limpiar()
    else:
        messagebox.showinfo("Información","Ramo no existe")
    os.system('attrib +h notas.dat')
    

def validate_entry(text):
    return text.isdecimal()

raiz = Tk()
raiz.geometry("370x480")
raiz.resizable(False,False)
raiz.title("Calculadora de Notas")
raiz.counter= 1 
raiz.config(background="grey77")

Panel_1 = Frame(raiz,background="grey77")
Panel_1.pack(pady=(15,0))

Label_NotaMinima = Label(Panel_1, text="Ingrese nota minima para pasar el ramo:",background="grey77")
Label_NotaMinima.grid(column=0, row=0,columnspan=2, sticky=S, padx=5, pady=5)

Entry_NotaMinima = Entry(Panel_1, width=10,borderwidth=2,validate="key",
    validatecommand=(raiz.register(validate_entry), "%S"))
Entry_NotaMinima.grid(column=3, row=0, padx=5, pady=5)
Entry_NotaMinima.focus()

Panel_2 = Frame(raiz,background="grey77")
Panel_2.pack()

Label_Botones = LabelFrame(Panel_2, text="Opciones",background="grey77")
Label_Botones.grid(row=0,column=0, padx=5, pady=5,sticky=N)

Button_Agregar = Button(Label_Botones, text="Agregar Nota", width=18, command=agregar)
Button_Agregar.grid(row=0,column=0, padx=5, pady=5)

Button_Quitar = Button(Label_Botones, text="Quitar Nota", width=18, command=quitar)
Button_Quitar.grid(row=1,column=0, padx=5, pady=5)

Button_SPond = Button(Label_Botones, text="Sin Ponderacion", width=18, command=desactivar)
Button_SPond.grid(row=2,column=0, padx=5, pady=5)
Button_CPond = Button(Label_Botones, text="Con Ponderacion", width=18, command=activar)

Button_Limpiar = Button(Label_Botones, text="Limpiar", width=18, command=limpiar)
Button_Limpiar.grid(row=4,column=0, padx=5, pady=5)

Button_Calcular = Button(Label_Botones, text="Calcular", width=18, command=calcular)
Button_Calcular.grid(row=5,column=0, padx=5, pady=5)

LabelF_Ramos = LabelFrame(Panel_2, text="Guardar Notas", background="grey77")
LabelF_Ramos.grid(row=1,column=0, padx=5, pady=5)

Lbl_Ramo = Label(LabelF_Ramos,text="Ingrese nombre ramo", background="grey77")
Lbl_Ramo.grid(row=0,column=0,padx=5,pady=2)

Text_Ramo = Entry(LabelF_Ramos,borderwidth=2,width=18)
Text_Ramo.grid(row=1,column=0,padx=5,pady=5)

Button_Guardar = Button(LabelF_Ramos,text ="Guardar",command=guardar)
Button_Guardar.grid(row=2,column=0,padx=5,pady=5)

ComboBox_Ramos = ttk.Combobox(LabelF_Ramos, width=18, state="readonly",postcommand=actualizar)
ComboBox_Ramos.grid(row=3,column=0,padx=5,pady=5)
ComboBox_Ramos.bind("<<ComboboxSelected>>", seleccionar)

Respuesta = Text(Panel_2, height=3,borderwidth=2, relief=GROOVE,width=43)
Respuesta.grid(row=2, column=0, sticky=W, padx=5 ,pady=5,columnspan=3)
Respuesta.configure(state="disabled")

Entry_Nota = ["Entry_Nota1","Entry_Nota2","Entry_Nota3","Entry_Nota4",
                "Entry_Nota5","Entry_Nota6","Entry_Nota7","Entry_Nota8"] 

Label_Notas = LabelFrame(Panel_2, text="Notas",background="grey77")
Label_Notas.grid(row=0,rowspan=2, column=1, padx=5, pady=5, sticky="W")

Entry_Pond = ["Entry_Pond1","Entry_Pond2","Entry_Pond3","Entry_Pond4",
                "Entry_Pond5","Entry_Pond6","Entry_Pond7","Entry_Pond8"] 
Label_Pond = LabelFrame(Panel_2, text="Ponderación",background="grey77")
Label_Pond.grid(row=0,rowspan=2, column=2, padx=5, pady=5, sticky="E")

for i in range(len(Entry_Nota)):
    Entry_Nota[i] = Entry(Label_Notas,width=10,borderwidth=2,validate="key",
    validatecommand=(raiz.register(validate_entry), "%S"))
    Entry_Nota[i].pack(padx=10, pady=10)

    Entry_Pond[i] = Entry(Label_Pond,width=10,borderwidth=2,validate="key",
    validatecommand=(raiz.register(validate_entry), "%S"))
    Entry_Pond[i].pack(padx=10, pady=10)
    if i >= 1:
        Entry_Nota[i].config(state="disabled", disabledbackground="grey85" )
        Entry_Pond[i].config(state="disabled", disabledbackground="grey85" )

menubar = Menu(raiz)
menubar.add_command(label="Instrucciones", command=instrucciones)
menubar.add_command(label="Acerca de...", command=about)
menubar.add_command(label="Eliminar ramo", command=eliminar)
raiz.config(menu=menubar)
    
notas = Path('notas.dat')
notas.touch(exist_ok=True)
os.system('attrib +h notas.dat')

actualizar()
raiz.mainloop()