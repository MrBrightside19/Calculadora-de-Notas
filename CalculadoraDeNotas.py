from tkinter import *
from tkinter import messagebox

def validate_entry(text):
    return text.isdecimal()

def calcular():
    Respuesta.configure(state="normal")
    total_notas = [] 
    ponderaciones = []
    notas_ponderadas = [] 
    min = Entry_NotaMinima.get()
    cant_notas = raiz.counter
    cont =  0 
    ceros = 0 
    val = 0 

    if Entry_NotaMinima.get() == "":
        Respuesta.delete("1.0", "end")
        Respuesta.insert("insert", "Debe ingresar nota minima para pasar el ramo.")
        return 0
    else:
        if raiz.counter == 1 and Entry_Nota[1].get() == "":
            Respuesta.delete("1.0", "end")
            Respuesta.insert("insert", "Debe ingresar notas para continuar.")
            return 0
        else:
            min = int(Entry_NotaMinima.get())

    while cont != cant_notas:
        Respuesta.delete("1.0", "end")
        nota = Entry_Nota[cont].get()
        if nota == "":
            total_notas.append(nota) 
            ceros += 1
        else:
            nota = int(nota)
            total_notas.append(nota)

        if Button_CPond.winfo_ismapped() == False and Button_SPond.winfo_ismapped():
            try:
                pond = int(Entry_Pond[cont].get())
            except:
                Respuesta.insert("insert", "Ponderaciones no pueden ser vacias")
                return 0
            val = val + pond
            if val > 100:
                for i in range (len(Entry_Pond)):
                    Entry_Pond[i].delete(0,"end")
                Entry_Pond[0].focus()
                Respuesta.insert("insert", "Error, ponderaciones no pueden ser mayora 100")
                return 0
            pond = pond/100
            ponderaciones.append(pond)

            if total_notas[cont] != "":
                notas_ponderadas.append(round(total_notas[cont] * ponderaciones[cont],2)) 
            else:
                notas_ponderadas.append("")  
        cont +=1
    sum  =  0 
    if ceros == 0 and Button_SPond.winfo_ismapped() and Button_CPond.winfo_ismapped() == False: 
        for i in range(len(notas_ponderadas)):
            sum = sum + notas_ponderadas[i]
        Respuesta.insert("insert", "Su promedio es: "+ str(sum))

    elif Button_CPond.winfo_ismapped() and Button_SPond.winfo_ismapped() == False: 
        cont = 0
        for i in range(len(total_notas)):
            if total_notas[i] != "":
                sum = sum + total_notas[i] 
            else:
                cont += 1
        min = (min * cant_notas) - sum 
        if cont != 0:
            min = min / cont 
            Respuesta.insert("insert", "Necesita "+ str(cont) + " " + str(min) + " para  pasar el ramo.")
        else: 
            min = sum/cant_notas
            Respuesta.insert("insert", "Nota final es: " + str(min))

    elif ceros != 0 and Button_SPond.winfo_ismapped() and Button_CPond.winfo_ismapped() == False:
        num_pond = 0 
        dif_notas = 0
        for i in range(len(total_notas)):
            if total_notas[i] != "":
                dif_notas = dif_notas + notas_ponderadas[i]
            else:
                sum = round((sum + ponderaciones[i]),2) 
                num_pond += 1
        prom = round(((min - dif_notas)/sum),2) 
        sum = sum/num_pond
        nota = "" 
        notas_faltantes = []
        for i in range (len(total_notas)):
            if total_notas[i] == "":
                dif = ponderaciones[i] - sum 
                notas_faltantes.append(round(prom * round(dif,3)+ prom,0))

        for i in range(len(notas_faltantes)):
            nota = " - ".join(map(str, notas_faltantes))
        Respuesta.insert("insert", "En orden, la(s) nota(s) minima(s) para  pasar  el ramo es(son): "+ str(nota))
        Respuesta.configure(state="disabled")

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
    for i in range(1,len(Entry_Nota)):
        Entry_Nota[i].delete(0,"end")
        Entry_Nota[i].config(state="disabled", disabledbackground="grey85" )
        Entry_Pond[i].delete(0,"end")
        Entry_Pond[i].config(state="disabled", disabledbackground="grey85" )
    Respuesta.delete("1.0", "end")
    Entry_NotaMinima.delete(0, "end")
    Entry_NotaMinima.focus()
    raiz.counter = 1 

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

ABOUT_TEXT = """
╔════════════╗
║ Create by Space Invader!..♥║
╚════════════╝
20-11-2020

"""

def about():
    toplevel = Toplevel()
    toplevel.title("Acerca de...")
    toplevel.resizable(False, False)
    label1 = Label(toplevel, text=ABOUT_TEXT, height=6, width=34, padx=1, pady=1)
    label1.pack(fill='both')
    
INSTRU = """Instrucciones:
-Ingresa la nota minima para pasar el ramo.
-Las notas que ingreses pueden ser con o sin ponderacion. 
-Puedes agregar un máximo de 8 notas.
-Los rangos de notas van desde el '0' al '100'.
-Para saber que nota necesitas solo deja el espacio 
 en blanco, el programa te dirá las notas para pasar el ramo.
-Las ponderaciones no pueden estar vacias ni la suma  
de estas exceder el 100%
 
 Suerte:)
"""
def instrucciones():
    messagebox.askokcancel("Instrucciones",INSTRU)

raiz = Tk()
raiz.geometry("350x470")
raiz.resizable(False,False)
raiz.title("Calculadora de Notas")
raiz.counter = 1 
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

Button_Agregar = Button(Label_Botones, text="Agregar", width=13, command=agregar)
Button_Agregar.grid(row=0,column=0, padx=5, pady=5)

Button_Quitar = Button(Label_Botones, text="Quitar", width=13, command=quitar)
Button_Quitar.grid(row=1,column=0, padx=5, pady=5)

Button_SPond = Button(Label_Botones, text="Sin Ponderación", width=13, command=desactivar)
Button_SPond.grid(row=2,column=0, padx=5, pady=5)
Button_CPond = Button(Label_Botones, text="Con Ponderación", width=13, command=activar)

Button_Limpiar = Button(Label_Botones, text="Limpiar", width=13, command=limpiar)
Button_Limpiar.grid(row=4,column=0, padx=5, pady=5)

Button_Calcular = Button(Label_Botones, text="Calcular", width=13, command=calcular)
Button_Calcular.grid(row=5,column=0, padx=5, pady=5)

Respuesta = Text(Panel_2, height=3,borderwidth=2, relief=GROOVE,width=40)
Respuesta.grid(row=1, column=0, sticky=W, padx=5 ,pady=5,columnspan=3)
Respuesta.configure(state="disabled")

Entry_Nota = ["Entry_Nota1","Entry_Nota2","Entry_Nota3","Entry_Nota4",
                "Entry_Nota5","Entry_Nota6","Entry_Nota7","Entry_Nota8"] 

Label_Notas = LabelFrame(Panel_2, text="Notas",background="grey77")
Label_Notas.grid(row=0, column=1, padx=5, pady=5, sticky="W")

Entry_Pond = ["Entry_Pond1","Entry_Pond2","Entry_Pond3","Entry_Pond4",
                "Entry_Pond5","Entry_Pond6","Entry_Pond7","Entry_Pond8"] 
Label_Pond = LabelFrame(Panel_2, text="Ponderación",background="grey77")
Label_Pond.grid(row=0, column=2, padx=5, pady=5, sticky="E")

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
raiz.config(menu=menubar)
raiz.mainloop()