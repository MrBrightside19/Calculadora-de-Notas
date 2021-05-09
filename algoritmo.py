
def val(registro_notas):
    cont_nota=0
    cont_pond=0
    for i in range(len(registro_notas)):
        if registro_notas[i][0].count("") == 1:
            cont_nota+=1
        if registro_notas[i][1].count("") == 1:
            cont_pond+=1
    return cont_nota,cont_pond

def func(self, sum):
    for i in range(len(self.registro_notas)):
            if self.registro_notas[i][0] != "":
                sum = sum + float(self.registro_notas[i][0]) 
    return sum

class Calculadora:
    def calculo(self):
        self.sum = 0
        for i in range (len(self.registro_notas)):
            if self.pond_exist:
                if self.pond > 0:
                    return "Debe ingresar todas las ponderaciones"
                elif self.registro_notas[i][0] != "":
                    self.registro_notas[i][0] = round(int(self.registro_notas[i][0]) * float(self.registro_notas[i][1]),2)
            else:
                self.min = (self.min * self.cant_notas) - func(self,self.sum)
                if self.nota > 0:
                    self.min = self.min / self.nota
                    return "Necesita "+ str(self.nota) + " " + str(self.min) + " para  pasar el ramo."
                else: 
                    self.min = func(self,self.sum)/self.cant_notas
                    return "Nota final es: " + str(self.min)
        if self.nota == 0 and self.pond_exist:
            return "Su promedio es: "+ str(func(self,self.sum))
        elif self.nota > 0 and self.pond_exist:
            num_pond = 0 
            dif_notas = 0
            for i in range(len(self.registro_notas)):
                if self.registro_notas[i][0] != "":
                    dif_notas = dif_notas + float(self.registro_notas[i][0])
                    
                else:
                    self.sum = round((self.sum + float(self.registro_notas[i][1])),2) 
                    num_pond += 1 #self.total_notas.count("")
            prom = round(((self.min - dif_notas)/self.sum),2) 
            self.sum = self.sum/num_pond
            nota = "" 
            for i in range (len(self.registro_notas)):
                if self.registro_notas[i][0] == "":
                    dif = float(self.registro_notas[i][1]) - self.sum 
                    self.registro_notas[i].append(round(prom * round(dif,3)+ prom,0))
            for i in range(len(self.registro_notas)):
                # nota = " - ".join(map(str, self.registro_notas[i][3]))
                if self.registro_notas[i][0] == "":
                    nota = nota +" "+ str(self.registro_notas[i][2])
            return "En orden, la(s) nota(s) minima(s) para pasar  el ramo es(son): "+nota

    def __init__(self, min, cant_notas, pond_exist,registro_notas):
        self.registro_notas = registro_notas
        self.min = min
        self.cant_notas = cant_notas
        self.pond_exist = pond_exist
        if self.pond_exist == 'S':
            self.pond_exist = True
        else:
            self.pond_exist = False
        self.nota,self.pond = val(self.registro_notas)