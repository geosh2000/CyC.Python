import Tkinter
from Tkinter import *
import time

root = Tk()
root.title("QM rtcalls Loader")
#root.config(bg="black") # Le da color al fondo
root.geometry("450x100")
wcode = Toplevel(root) # Crea una ventana hija
wcode.withdraw()  # oculta v1

running = False  # Global flag

global flag
flag = 0

def scanning():
    global flag
    
        
    if running:  # Only do this if the Stop button has not been clicked
        if flag==0:
            flag=300000
            try:
                execfile( "calls_day.py" )
                refresh_fecha()
                status.set("Running dcalls")
                l2.config(text="Running dcalls")
               
            except:
                pass
        else:
            flag=flag-1000
            status.set("Running dcalls (" + str(flag/1000) + " seg)")
            l2.config(text="Running dcalls (" + str(flag/1000) + " seg)")
        
    else:
        status.set("Stopped dcalls")
        l2.config(text="Stopped dcalls")
        

    # After 1 second, call scanning again (create a recursive loop)
    root.after(1000, scanning)

def start():
    """Enable scanning by setting the global flag to True."""
    global running
    running = True
    global flag
    flag = 0

def stop():
    """Stop scanning by setting the global flag to False."""
    global running
    running = False
    


def imprimir_fecha():
    return str(time.localtime()[2]) + "/" + str(time.localtime()[1]) + "/" + str(time.localtime()[0]) + ", " + str(time.localtime()[3]) + ":" + str(time.localtime()[4]) + ":" + str(time.localtime()[5])

def refresh_fecha():
    mifecha.set(imprimir_fecha())
    l1.config(text=imprimir_fecha())
    
def refresh_fecha2():
    mifecha_2.set(imprimir_fecha())
    l1_2.config(text=imprimir_fecha())
    
def refresh_fecha3():
    mifecha_3.set(imprimir_fecha())
    l1_3.config(text=imprimir_fecha())


start = Button(root, text="Start Scan", command=start)
stop = Button(root, text="Stop", command=stop)

mifecha=StringVar()
mifecha_2=StringVar()
mifecha_3=StringVar()
status=StringVar()
status_2=StringVar()
status_3=StringVar()
l1=Label(root,textvar=mifecha,font=(16))
l1.grid(column=5,row=1)
l2=Label(root,textvar=status,font=(16))
l2.grid(column=4,row=1)
l1_2=Label(root,textvar=mifecha_2,font=(16))
l1_2.grid(column=5,row=2)
l2_2=Label(root,textvar=status_2,font=(16))
l2_2.grid(column=4,row=2)
l1_3=Label(root,textvar=mifecha_3,font=(16))
l1_3.grid(column=5,row=3)
l2_3=Label(root,textvar=status_3,font=(16))
l2_3.grid(column=4,row=3)
lrtcalls=Label(root,text="RT Calls",font=(16))
lrtcalls.grid(column=1,row=1)

refresh_fecha()

start.grid(row=1, column=2)
stop.grid(row=1, column=3)



root.after(1000, scanning)  # After 1 second, call scanning
root.mainloop()