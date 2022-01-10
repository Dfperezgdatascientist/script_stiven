# -*- coding: utf-8 -*-
from automagica import empty_folder
import win32com.client as win
import pandas as pd
import numpy as np
import paramiko
import datetime
import os
### Conexion python to linux server ####

s = paramiko.SSHClient()
s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
s.connect('10.1.1.250',username='',password='')
sftp = s.open_sftp()

#### FECHAS ###
#today = datetime.datetime(2020,8,31)
today = datetime.datetime.now()


## Año - Mes - Día
year = str(today.year)
month = today.strftime("%m")
mes = str(today.month)
day = str(today.day)

## Meses en texto
def fecha(one):
    Mes = [(today.month == 1),
           (today.month == 2),
           (today.month == 3),
           (today.month == 4),
           (today.month == 5),
           (today.month == 6),
           (today.month == 7),
           (today.month == 8),
           (today.month == 9),
           (today.month == 10),
           (today.month == 11),
           (today.month == 12)
                   ]
    if one == 1 :
        elecciones = np.array(("01 Enero","02 Febrero","03 Marzo","04 Abril","05 Mayo",
                            "06 Junio","07 Julio","08 Agosto","09 Septiembre","10 Octubre",
                            "11 Noviembre","12 Diciembre"), dtype="str")
        new = np.select(Mes, elecciones, -1)
    else:
        elecciones = np.array(("Enero","Febrero","Marzo","Abril","Mayo",
                            "Junio","Julio","Agosto","Septiembre","Octubre",
                            "Noviembre","Diciembre"), dtype="str")
        new = np.select(Mes, elecciones, -1)
    
    return str(new)

os.makedirs('D:/Temporal', exist_ok=True)
carpeta =  'D:/Temporal'
os.chdir(carpeta)
#extension='.xlsx'
#empty_folder(carpeta)
"""
for item in os.listdir(carpeta): #recorrer todos los items de la carpeta
            if item.endswith(extension): #comprueba la extensión    
                nombrearchivo= os.path.abspath(item)
                x = nombrearchivo.split("\\")
                print(str(x[2]))
                sftp.put(nombrearchivo, '/home/rsadmin/rsadmin-history/Info360/CEXHome/'+str(x[2]))
"""


Ruta = '//10.1.1.7/01 Oficina Planeación y Control/22 Reportes/COMFAMA/08 Tipificacion/'+year+'/'+fecha(1)+'/'+year+'_'+month+'_Tipificacion_Comfama.xlsb'
df = pd.read_excel(Ruta,engine='pyxlsb',sheet_name='Tipificación_BD',skiprows=7)

cols = ['Area', 'Descripcion', 'codigo_resultado',
       'Area_Resultado', 'Asesor', 'Asesor_Nombre', 'Fecha', 'Fecha_Inicio',
       'Hora_Inicio', 'Numero_Doc', 'cuenta', 'Tipo_Doc', 'Tienda', 'CallId',
       'Telefono', 'Prospecto_Venta', 'Fuente', 'Nit Empresa Evento',
       'Contacto Empresa', 'Municipio', 'Negocio']

df = df[cols]

df.to_excel('Tipificacion_Comfama.xlsx')

Ruta1 = r'D:\Temporal\Tipificacion_Comfama.xlsx'
sftp.put(Ruta1, '/home/rsadmin/rsadmin-history/Info360/Comfama/Tipificacion_Comfama.xlsx')
#empty_folder(carpeta)
print('ok')