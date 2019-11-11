######################################################
#Elaborado por: Fabrizio Ferreto y Crystel Montero
#Fecha de creación: 27/04/2019
#Última modificación: 13/05/2019 1:00pm
#Versión: 3.5.2
#######################################################
#Importación de librerías
#Interfaz gráfica
from tkinter import*
from tkinter import ttk as t
from tkinter import messagebox as MS
#Api
import requests
#XML
import xml.etree.ElementTree as ET
import codecs
from xml.dom import minidom
#Correo
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
#Manual de usuario
import webbrowser
#Definición de funciones
#Matriz y diccionario
def agregarFraseMatriz(matriz,numapli):
    """
    Función: agrega las frases, separando las partes que obtiene del API a una matriz.
    Entradas: una matriz vacía y el número de aplicación.
    Salidas: las frases separadas con el formato de "Personaje-frase-id-codigoAplicacion". Para insertar
    en el listbox
    """
    listanue=[]
    listafra=[]
    listanueid=[]
    i=0
    url=requests.get("http://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote") #API.
    resp=dict(eval(url.text)) #Resp: el diccionario que devuelve el api.
    conver=str(resp["starWarsQuote"])
    conver=conver.replace(" - "," — ")
    conver=conver.replace(" ? "," — ")
    conver=conver.replace("r — n","r, n")
    frase=conver.split(" — ")
    while i<=len(matriz)-1:
        if frase[1] in matriz[i]:
            matriz[i][-1].append("*")
            if frase[0] not in matriz[i][1]:
                f=0
                compara=int(resp["id"])
                while f<len(matriz[i][2]):
                    if compara==matriz[i][2][f]:
                        return agregarFraseMatriz(matriz, numapli)
                    f+=1
                matriz[i][1].append(frase[0])
                matriz[i][2].append(resp["id"])
                mF.insert(END, frase[1]+" "+frase[0]+" id:"+str(resp["id"])+" codigo:"+matriz[i][-2])
                return""
            else:
                return agregarFraseMatriz(matriz,numapli)
        i+=1
    listanue.append(frase[1])
    listafra.append(frase[0])
    listanue.append(listafra)
    listanueid.append(resp["id"])
    listanue.append(listanueid)
    if (frase[1][-1])==")":
        codapli="#"+(frase[1][0]).upper() +(str(numapli)).zfill(3)+ "-R"
    else:
        codapli="#"+(frase[1][0]).upper() +(str(numapli)).zfill(3)+ "-" +(frase[1][-1]).upper()
    listanue.append(codapli)
    listanue.append(["*"])
    matriz.append(listanue)
    mF.insert(END, frase[1]+" "+frase[0]+" id:"+str(resp["id"])+" codigo:"+str(codapli))
    return ""
def agregarFraseDicc(matriz, dicc):
    """
    Función: agrega el personaje, la cantidad de frases que le salen(contando las repetidas)
    y el código de aplicación. También determina quien es el personaje con más frases. 
    Entradas: la matriz y un diccionario vacío.
    Salidas: el diccionario ya formado.
    """
    i=0
    lisNum=[]
    while i<len(matriz):
        dicc[matriz[i][0]]=int(len(matriz[i][-1])), matriz[i][-2]
        i+=1
        diccFra=dicc #Asignar el diccionario que se forma dentro de la función a la variable global del diccionario.
    matrizFra=matriz #Asigna la matriz que se formó anteriormente a una variable global de la matriz.
    #Personaje con más frases.
    for i in dicc:
        num=int(dicc[i][0])
        lisNum.append(num)
    numMax=max(lisNum)
    print("Máximo",numMax)
    for j in dicc:
        if numMax==int(dicc[j][0]):
            persMax=j
    mayor=Label(venPrin, text="El personaje \ncon más frases es: \n"+persMax)
    mayor.config(bg="Light Blue", font=("Star Jedi", 10))
    mayor.place(x=650, y=200)
    return dicc    
def contarFrase(matriz, numaplica, dicc):
    """
    Función: ejecuta las funciones anteriores basada en la variable canti, que sería la cantidad de veces
    que debe ejecutarse el programa para encontrar es cantidad de frases. 
    Entradas: la matriz, el número de aplicación y el diccionario.
    Salidas: N/A
    Restricciones: la cantidad de frases no puede ser mayor a 50, y deben ser número enteros mayores a 0.
    """
    try:
        canti=int(cantEnt.get())
        if canti>50:
            MS.showinfo(message="No puede buscar más de 50 frases.", title="Cantidad inválida.")
        i=0
        j=0
        while i<canti:
            numaplica+=1
            print(agregarFraseMatriz(matriz,numaplica))
            i+=1
        
        print("*******************************")    
        print(agregarFraseDicc(matriz, dicc))
        print("*******************************")
        return ""
    except ValueError:
        MS.showerror(message="Debe ingresar una cantidad de frases válida para ejecutar el programa.", title="Cantidad inválida.")

#XML
def leerXml(matrizfin,diccfin):
    """
    Función: cargar el archivo de respaldo en el cuadro del listBox cuando se abra la aplicación.
    Entradas: matriz y diccionario.
    Salidas: la matriz.
    """
    cont=0
    with codecs.open('Backup_StarWars.xml',"r", encoding="latin 1") as xml:
        tree=ET.parse(xml)
    ET.dump(tree)
    raiz=tree.getroot()
    for matriz in raiz:
        for llave in matriz.iter("llave"):
            personaje=(llave.attrib.get("personaje"))
            for apli in llave.iter("Aplicacion"):
                apli=(apli.attrib.get("numapli"))
            for repe in llave.iter("Repeticion"):
                repet=(repe.attrib.get("numrep"))
                diccfin[personaje]=apli,int(repet)
        for personaje in matriz.iter("personaje"):
            idleer=[]
            for codfra in personaje.iter("ids"):
                idfra=(codfra.attrib.get("idfra"))
                idleer.append(int(idfra))
            fraseleer=[]
            for frase in personaje.iter("frases"):
                frase=(frase.attrib.get("frase"))
                frase=frase.replace("\x92","'")
                frase=frase.replace("\x85","...")
                fraseleer.append(frase)
                listaindivid=[]
            for info in personaje.iter("infopers"):
                nom=(info.attrib.get("nom"))
                codigo=(info.attrib.get("codigo"))
                listaindivid.append(nom)
                listaindivid.append(fraseleer)
                listaindivid.append(idleer)
                listaindivid.append(codigo)
            matrizfin.append(listaindivid)
    for i in diccfin:
        j=0
        listest=[]
        while j<(int(diccfin[i][1])):
            listest.append("*")
            j+=1
        for linea in matrizfin:
            if i in linea:
                linea.append(listest)
    return matrizfin
def escribirXml(matriz,dicc):
    """
    Función: hace el archivo XML en base a la matriz y el diccionario. Solo se ejecuta cuando el usuario
    desee realizar un back up.
    Entradas: la matriz y el diccionario.
    Salidas: N/A
    """
    print(matriz)
    mat=0
    diccion=0
    raiz=ET.Element("ElementosStarWars")
    ramaMat=ET.SubElement(raiz,"Matriz")
    ramaDicc=ET.SubElement(raiz,"Diccionario")
    while mat<=len(matriz)-1:
        ramaapli2=ET.SubElement(ramaMat,"personaje")
        lineaperso3=ET.SubElement(ramaapli2,"infopers",nom=(matriz[mat][0]),codigo=str(matriz[mat][3]))
        for i in (matriz[mat][1]):
            perfrases3=ET.SubElement(ramaapli2,"frases", frase=i)
        for i in(matriz[mat][2]):
            perids3=ET.SubElement(ramaapli2,"ids", idfra=str(i))
        mat+=1
    for i in dicc:
        ramllav2=ET.SubElement(ramaDicc, "llave", personaje=i)
        ramaplidicc3=ET.SubElement(ramllav2,"Aplicacion",numapli=str(dicc[i][1]))
        ramarep3=ET.SubElement(ramllav2,"Repeticion",numrep=str(dicc[i][0]))
    arbol=ET.ElementTree(raiz)
    ET.dump(arbol)
    xml=(prettify(raiz))
    with open("Backup_StarWars.xml", "w") as file:
        file.write(xml)
    return ""
def prettify(elem):
    """
    Función: ordenar el XML de una forma más entendible para el usuario.
    Entradas: elem
    Salidas: elem reparseado de manera legible. 
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent=" ")
def mostrarXML(matrizfin,diccfin):
    """
    Función: muestra las frases del XML del backUp por separado, no todas en una sola línea como la matriz
    completa.    
    Entradas: matriz y diccionario.
    Salidas: N/A
    """
    matriz=leerXml(matrizfin,diccfin)
    cont=0
    while cont<=len(matrizfin)-1:
        if len(matrizfin[cont][1])>1:
            k=0
            while k<=len(matrizfin[cont][1])-1:
                mF.insert(END, [str(matrizfin[cont][0]),str(matrizfin[cont][1][k])," id:",str(matrizfin[cont][2][k])," codigo:",str(matrizfin[cont][3])])
                k+=1
        else:
            mF.insert(END, [str(matrizfin[cont][0])+str(matrizfin[cont][1])+" id:"+str(matrizfin[cont][2])+" codigo:"+str(matrizfin[cont][3])])
        cont+=1
    return ""    
#Botones, interfaz gráfica
def ejecutarBotonBuscarCant():
    """
    Función: ejecuta el programa después de presionar el botón.
    Entradas:N/A
    Salidas:N/A
    Restricciones: debe haber conexión a internet para ejecutar el programa. 
    """
    try:
        contarFrase(matrizFra, numapli, diccFra)
    except requests.exceptions.ConnectionError:
        MS.showerror(message="No se pudo establecer conexión a internet, intente conectarse a otra red."\
                     ,title="Fallo de conexión")
def backUp():
    """
    Función: pregunta al usuario si desea realizar un archivo de respaldo.
    Entradas:N/A
    Salidas: N/A
    """
    def ejecutarSi():
        """
        Función: Realiza un archivo de tipo XML para guardar todas las frases que se ejecuten
        en la aplicación. Además cierra la aplicación
        Entradas: N/A
        Salidas: N/A
        """
        escribirXml(matrizFra,diccFra)
        MS.showinfo(message="Se creó el archivo Backup_StarWars.xml", title="BackUp")
        ven.destroy()
        venPrin.destroy()
    def ejecutarNo():
        """
        Función: No realiza el respaldo y cierra la aplicación. 
        Entradas: N/A
        Salidas: N/A
        """
        MS.showinfo(message="¡Gracias por usar la aplicación!, vuelva pronto.", title="Cierre")
        ven.destroy()
        venPrin.destroy()
    ven=Tk()
    ven.title("Respaldo")
    ven.config(bg="Azure2")
    ven.geometry("400x100")
    backUp=Label(ven, text="¿Desea realizar un respaldo?", font=("Homoarakhn", 12))
    backUp.config(bg="Azure2")
    backUp.grid(row=0, column=1)
    si=t.Button(ven, text="SÍ", command=ejecutarSi)
    si.place(x=100, y=30)
    no=t.Button(ven, text="NO", command=ejecutarNo)
    no.place(x=250, y=30)
    ven.mainloop()
def compartir():
    """
    Función: comparte las frases seleccionadas por el usuario por medio de correo electrónico.
    Entradas: N/A
    Salidas: N/A
    """
    MS.showinfo(message="Solo se pueden enviar correos de una cuenta gmail a cualquier otra.",\
                title="Info")
    def seleccionarFrases():
        """
        Función: toma las frases seleccionadas por el usuario y las agrega a una lista.
        Entradas: N/A
        Salidas: llamar a la aplicación de escribir correo. 
        """
        lisEnviar=[]
        lisFrase=mF.curselection()
        for item in lisFrase:
            frase=mF.get(item)
            frase=str(frase)
            lisEnviar.append(frase)
        MS.showinfo(message="Agregados al archivo para compartir.", title="Información.")
        def escribirCorreo(lisEnviar):
            """
            Función: escribe el archivo XML que contiene las frases seleccionadas por el usuario.
            Entradas: la lista de frases que se creó en la función anterior.
            Salidas: N/A
            """
            raiz=ET.Element("FrasesCompartidas")
            for i in lisEnviar:
               fra=ET.SubElement(raiz,"frase",frases=i)
            arbol=ET.ElementTree(raiz)
            ET.dump(arbol)
            print(prettify(raiz))
            xml=(prettify(raiz))
            with open(nombreArchComp, "w") as file:
                file.write(xml)
            return ""
        return escribirCorreo(lisEnviar)
    def enviarCorreo():
        """
        Función: envía un correo con el XML que tiene las frases seleccionadas por el usuario.
        Entradas: el correo, la contraseña y el destinatario, se toman directamente de los widgets de
        Entry que se encuentran en el programa principal.
        Salidas: N/A
        """
        try:
            print(seleccionarFrases())
            mensaje=MIMEMultipart()
            archivo=open(nombreArchComp, 'rb')
            archiv=MIMEBase('application', 'octet-stream')
            archiv.set_payload((archivo).read())
            encoders.encode_base64(archiv)
            archiv.add_header('Content-Disposition', "attatchment; filename= "+nombreArchComp)
            mensaje.attach(archiv)
            mail=smtplib.SMTP("smtp.gmail.com",587)
            mail.starttls()
            mail.login(correoEnt.get(),contraEnt.get())
            conte=mensaje.as_string()
            mail.sendmail(correoEnt.get(), destEnt.get(),conte)
            mail.quit()
            MS.showinfo(message="Enviado, recuerde revisar la carpeta de spam.", title="correo")
        except smtplib.SMTPAuthenticationError:
            MS.showerror(message="Contraseña, destinatario o correo inválidos, verifique", title="Error")
        except requests.exceptions.ConnectionError:
            MS.showerror(message="No se pudo enviar el correo por un error de conexión")
        except TypeError:
            MS.showerror(message="Ingrese valores válidos en los espacios de correo, contraseña y destinatario.")
    horaYfecha=str(time.strftime("%d_%m_%Y")+"."+time.strftime("%I_%M_%S"))
    nombreArchComp="share"+"_"+horaYfecha+".xml"
    #Ventana de enviar correo.
    win=Tk()
    win.title("Compartir")
    win.config(bg="Azure2")
    win.geometry("400x200")
    correo=Label(win, text="Correo")
    correo.config(bg="Azure2")
    correo.grid(row=0, column=0, padx=10, pady=10)
    correoEnt=t.Entry(win)
    correoEnt.grid(row=0, column=1, padx=10, pady=10)
    contraseña=Label(win, text="Contraseña")
    contraseña.config(bg="Azure2")
    contraseña.grid(row=1, column=0, padx=10, pady=10)
    contraEnt=t.Entry(win)
    contraEnt.grid(row=1, column=1, padx=10, pady=10)
    contraEnt.config(show="*")
    destinatario=Label(win, text="Destinatario: ")
    destinatario.config(bg="Azure2")
    destinatario.grid(row=2, column=0, padx=10, pady=10)
    destEnt=t.Entry(win)
    destEnt.grid(row=2, column=1, padx=10, pady=10)
    enviar=t.Button(win, text="Enviar", command=enviarCorreo)
    enviar.grid(row=3, column=1)
    win.mainloop()
#Nota aclaratoria: en esta función hay varias funciones dentro ya que la idea es que el archivo se cree
#y se envíe al mismo tiempo por cuestiones del nombre.
def abrirManual():
    """
    Función: abre el pdf del manual de usuario.
    Entradas: N/A
    Salidas: N/A
    """
    webbrowser.open("https://drive.google.com/file/d/16vhTSufcJuNOvUpKuqytR4eG6xnOB_PK/view?usp=drive_open")
#Variables globales
matrizFra=[]
diccFra={}
numapli=len(matrizFra)
#Ventana principal
venPrin=Tk()
venPrin.title("Frases StarWars")
venPrin.geometry("1000x500")
venPrin.config(bg="Light Blue")
venPrin.config(relief="groove")
venPrin.config(bd=20)
frases=Label(venPrin, text="FRASES ALEATORIAS")
frases.config(bg="Light Blue")
frases.config(font=("STARWARS", 12))
frases.grid(row=0, column=0, padx=10, pady=10)
#ListBox donde se van a mostrar las frases
mF=Listbox(venPrin, selectmode=MULTIPLE, width=100, height=20)
mF.grid(row=1, column=0, padx=10, pady=10)
barrav=Scrollbar(venPrin, command=mF.yview)
barrav.grid(row=1,column=0, sticky="nsew")
mF.config(yscrollcommand=barrav.set)
instr=Label(venPrin, text="Selecciona las frases que desea enviar por correo")
#Buscar la cantidad de frases
cant=Label(venPrin, text="Cantidad de frases")
cant.config(bg="Light Blue")
cant.config(font=("Star Jedi Outline", 10))
cant.grid(row=0, column=1)
cantEnt=t.Entry(venPrin)
cantEnt.grid(row=0, column=2)
cantBot=t.Button(venPrin, text="Buscar", command=ejecutarBotonBuscarCant)
cantBot.place(x=810, y=40)
#Botón manual de usuario
manualUsuario=t.Button(venPrin, text="Manual de Usuario", command=abrirManual)
manualUsuario.place(x=500, y=400)
#Compartir 
shareBot=t.Button(venPrin, text="Compartir", command=compartir)
shareBot.place(x=350, y=400)
#Botón de cerrar
venPrin.protocol('WM_DELETE_WINDOW', backUp)
#Imágenes
ima1=PhotoImage(file="YODA.png")
ima1=ima1.subsample(5,5)
eti=Label(venPrin, image=ima1)
eti.config(bg="Light Blue")
eti.place(x=700, y=300)
ima2=PhotoImage(file="1_12_21.png")
ima2=ima2.subsample(5,5)
eti2=Label(venPrin, image=ima2)
eti2.config(bg="Light Blue")
eti2.place(x=800, y=110)
#Leer XML al abrir la aplicación
"""
Esta parte lee el xml del backUp al abrir la aplicación.
Tiene una validación sobre sino existe el archivo que no lea nada. 
"""
try:
    mostrarXML(matrizFra,diccFra)
except FileNotFoundError:
    None 
venPrin.mainloop() #Esta función es de la interfaz, lo que hace es que mantiene todas las líneas de código
                   #antes de esa ejecutándose. 


