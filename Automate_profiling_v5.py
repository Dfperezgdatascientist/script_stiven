# %% 
'''
'''

## Se importan las librerias necesarias

import pandas as pd
import numpy as np
import datetime as dt
from datetime import timedelta
pd.options.display.max_columns = None
pd.options.display.max_rows = None
import glob as glob
import datetime
import re
import jenkspy
import tkinter as tk

root= tk.Tk()

canvas1 = tk.Canvas(root, width = 300, height = 300)
canvas1.pack()

# %%
def profiling():
        #### Read Databases
        datas=pd.read_csv('C:/Users/scadacat/Desktop/TIGO (Cliente)/Cobranzas/Notebooks/Bds/data_con_drop.csv',sep=';',encoding='utf-8',dtype='str')
        salida=pd.read_csv('C:/Users/scadacat/Desktop/TIGO (Cliente)/Cobranzas/Notebooks/Bds/salida_limpia.csv',sep=';',encoding='utf-8',dtype='str')
        seguimiento=pd.read_csv('C:/Users/scadacat/Desktop/TIGO (Cliente)/Cobranzas/Notebooks/Bds/seguimiento.csv',sep=';',encoding='utf-8',dtype='str')
        virtuales=pd.read_csv('C:/Users/scadacat/Desktop/TIGO (Cliente)/Cobranzas/Notebooks/Bds/virtuales.csv',encoding='utf-8',sep=';')
        df=datas.copy()
        out=salida.copy()
        seg=seguimiento.copy()
        vir=virtuales.copy()
        out.sort_values(['Identificacion Del Cliente','Fecha_Gestion'],inplace=True)
        out=out[out['Repetido CC']=='0']
        out=out[~out.duplicated(keep='last')]

        ## Cleaning
        df['Marca Score']=df['Marca Score'].str.strip().fillna('NO REGISTRA')
        df['Marca Score'][df['Marca Score']==''] ='NO REGISTRA'
        df['Analisis De Habito']=df['Analisis De Habito'].fillna('NO DEFINE')
        df['Analisis De Habito'][df['Analisis De Habito']==' '] ='NO DEFINE'
        df['Tipo de Cliente'][df['Tipo de Cliente']==' '] ='NO DEFINE'
        df['Marca Funcional']=df['Marca Funcional'].str.replace(' ','0')
        df['Marca']=df['Marca'].str.replace(' ','0')
        df['Antiguedad Cliente'][df['Antiguedad Cliente']==' '] ='NO REGISTRA'
        df['Perfil Digital']=df['Perfil Digital'].fillna('Sin perfil')
        df['Nivel de riesgo experian']=df['Nivel de riesgo experian'].str.replace(' ','NO REGISTRA')
        df['Nivel de Riesgo']=df['Nivel de Riesgo'].str.replace(' ','NO REGISTRA')
        df['Nivel Estrategia Cobro']=df['Nivel Estrategia Cobro'].str.replace(' ','NO REGISTRA')
        df['Real reportado en central de riesgos']=df['Real reportado en central de riesgos'].str.replace(' ','0')
        df['Nivel de Riesgo'][df['Nivel de Riesgo']==' '] ='NO REGISTRA'
        df['Estado del Cliente'][df['Estado del Cliente']==' '] ='SIN IDENTIFICAR'
        df['TipificaciÃ³n Cliente'][df['TipificaciÃ³n Cliente']==' '] ='SIN IDENTIFICAR'
        df['Estrategia'][df['Estrategia']==' '] ='SIN ESTRATEGIA'
        df['Autopago'][df['Autopago']==' '] ='NO APLICA'
        df['Tipo de Cliente']=df['Tipo de Cliente'].fillna('NO DEFINE')
        df['Tipo de Reporte a Central de Riesgos'][df['Tipo de Reporte a Central de Riesgos']==' '] ='NO REGISTRA'
        df['Codigo edad de mora(para central de riesgos)']=df['Codigo edad de mora(para central de riesgos)'].str.replace(' ','NO REGISTRA')
        df['AnÃ¡lisis Vector'][df['AnÃ¡lisis Vector']==' '] ='SIN IDENTIFICAR'
        df['Análisis Vector_PAGOS_PARCIAL'] = np.where(df['AnÃ¡lisis Vector'].str.contains("PAGO PARCIAL|PAGOS PARCIAL"),"1",'0')
        df['Análisis Vector_PAGO OPORTUNO'] = np.where(df['AnÃ¡lisis Vector'].str.contains("SIN PAGO|FINANCIAR"),"1",'0')
        df['Análisis Vector_SIN_IDENTIFICAR'] = np.where(df['AnÃ¡lisis Vector'].str.contains("SIN IDENTIFICAR"),"1",'0')
        df['Análisis Vector_SIN_PAGO'] = np.where(df['AnÃ¡lisis Vector'].str.contains("SIN PAGO|FINANCIAR"),"1",'0')
        df['Análisis Vector_suspension'] = np.where(df['AnÃ¡lisis Vector'].str.contains("SUSPENSIO"),"1",'0')
        df['Análisis Vector_indeterminado'] = np.where(df['AnÃ¡lisis Vector'].str.contains("PAGO OPORTUNO Y NO OPORTUNO"),"1",'0') 
        df['Análisis Vector_pago_no_oport'] = np.where(df['AnÃ¡lisis Vector'].str.contains("PAGO NO OPORTUNO"),"1",'0')
        df['Análisis Vector_otro_caso'] = np.where(df['AnÃ¡lisis Vector'].str.contains("NUEVO|FACTURAS AJUSTADAS|PROBLEMAS RECLAMACION"),"1",'0')
        df['Vector Cualitativo # SuscripciÃ³n'][df['Vector Cualitativo # SuscripciÃ³n']==' '] = df["Vector Cualitativo # SuscripciÃ³n"].mode()[0]
        df['Fecha Ult Gestion']=pd.to_datetime(df['Fecha Ult Gestion'],format='%Y-%m-%d') 
        ###PARSE DATES AND CREATE NEW FEATURES
        df['Fecha de Asignacion']=pd.to_datetime(df['Fecha de Asignacion'],format='%Y-%m-%d %H:%M:%S')
        df['Fecha Ult pago']=pd.to_datetime(df['Fecha Ult pago'],format ='%Y-%m-%d %H:%M:%S',errors = "coerce")
        df['Fecha de cuenta de cobro mas antigua']=pd.to_datetime(df['Fecha de cuenta de cobro mas antigua'],format ='%Y-%m-%d %H:%M:%S',errors = "coerce")
        df["Dias_ult_pago"] = (df['Fecha Ult pago']).dt.day
        df["dia_semana_ult_pago"] = (df['Fecha Ult pago']).dt.weekday
        df["mes_ult_pago"]=df["Fecha Ult pago"].dt.month
        df["semana_ult_pago"]=df["Fecha Ult pago"].dt.week
        df["trimestre_ult_pago"] = df["Fecha Ult pago"].dt.quarter
        df["año_ult_pago"] = df["Fecha Ult pago"].dt.year
        df["DIAS_desde_ult_pago"] = (df["Fecha Ult Gestion"] - df["Fecha Ult pago"]).dt.days
        df["Fecha estado corte"]=pd.to_datetime(df["Fecha estado corte"],format ='%Y-%m-%d %H:%M:%S',errors = "coerce")
        df["dias_ult_pago_cobro"] = (df["Fecha Ult pago"]-df["Fecha estado corte"]).dt.days
        df["dias_ult_pago_fac_ant"] = (df["Fecha Ult pago"]-df["Fecha de cuenta de cobro mas antigua"]).dt.days
        df['Fecha de Asignacion_mes']=df["Fecha de Asignacion"].dt.month
        df['Fecha de Instalacion']=pd.to_datetime(df['Fecha de Instalacion'],format ='%Y-%m-%d %H:%M:%S',errors = "coerce")
        df['antiguedad_mes']=(dt.datetime.now()-df['Fecha de Instalacion']).dt.days/365
        df['Fecha Retiro']=pd.to_datetime(df['Fecha Retiro'].str.replace('4732','2020'),format='%Y-%m-%d',errors = "coerce")
        df['Fecha Vencimiento Sin Recargo']=pd.to_datetime(df['Fecha Vencimiento Sin Recargo'],format='%Y-%m-%d')
        df['dias_desde_ult_gestion']=(dt.datetime.now()-df['Fecha Ult Gestion']).dt.days
        ## Group labels
        df['Descripcion subcategoria']=df['Descripcion subcategoria']\
                .str.replace('Consumos EPM Telco|INALAMBRICOS NO JAC|unica|COMERCIAL|ENTERPRISE|MONOPRODUCTO|PYME|------------------------------|LINEA BUZON','NO REGISTRA')\
                .str.replace('ESTRATO MEDIO ALTO|MEDIO ALTO','ESTRATO 4')\
                .str.replace('ESTRATO ALTO|ALTO','ESTRATO 6')\
                .str.replace('ESTRATO MEDIO-BAJO|MEDIO BAJO','ESTRATO 2')\
                .str.replace('ESTRATO MEDIO|MEDIO','ESTRATO 3')\
                .str.replace('ESTRATO MEDIO-BAJO|MEDIO BAJO','ESTRATO 2')\
                .str.replace('BAJO BAJO|ESTRATO BAJO-BAJO|ESTRATO BAJO|BAJO','ESTRATO 1')
        df['Descripcion subcategoria'][df['Descripcion subcategoria']=='-'] ='NO REGISTRA' ## No registra
        df['TipificaciÃ³n Cliente'][df['TipificaciÃ³n Cliente']==' '] = df["TipificaciÃ³n Cliente"].mode()[0] ## Reemplazo con la moda
        df['Dias Suspension'][df['Dias Suspension']==' ']=0
        df['Dias Suspension']=df['Dias Suspension'].astype('int')
        ## Group labels
        df['Descripcion producto']=df['Descripcion producto'].str.replace('-','').str.strip().str.upper()\
        .str.replace('TELEVISION UNE|TELEVISION INTERACTIVA|TV CABLE|TV INTERACTIVA|UNE TV|TELEVISION SIN SEÃƑÂ‘AL|TELEVISION SIN SEÃƑÂ‘AL|TV CABLE SIN SEÃƒÂ‘AL','TELEVISION')\
        .str.replace('INTERNET BANDA ANCHA|SEGUNDA CONEXION INTERNET|BANDA ANCHA|INTERNET EDATEL|INTERNET INSTANTANEO|CABLE MODEM|INTERNET DEDICADO 11|ADSL BASICO','INTERNET')\
            .str.replace('UNE MOVIL|COLOMBIAMOVIL BOGOTA|TIGO|ETB','UNEMOVIL')\
                .str.replace('TOIP|TELEFONICA  TELECOM|TELECOM|TO_SINVOZ','TELEFONIA')\
                    .str.replace('LÃƑÂ­NEA BÃƑÂ¡SICA','LINEA BASICA')
        df['Descripcion categoria']=df['Descripcion categoria'].str.replace("[^a-zA-Z ]+", "NO REGISTRA")
        df['Descripcion producto']=df['Descripcion producto'].str.replace('-','').str.strip()\
            .str.replace('TELEVISION UNE|Television Interactiva|TV CABLE |TV INTERACTIVA|UNE TV|TELEVISIONSIN SEÃƒÂ‘AL','TELEVISION')\
                .str.replace('Internet Banda Ancha|Internet EDATEL|CABLE MODEM','INTERNET').str.replace('UNE MOVIL','UNEMOVIL')\
                    .str.replace('UNE MOVIL|COLOMBIAMOVIL BOGOTA','UNEMOVIL')\
                        .str.replace('TOIP','TELEFONIA')
        df['Descripcion producto']=df['Descripcion producto'].str.strip().str.replace('-','')\
        .str.replace('TELEVISION UNE|Television Interactiva|TV CABLE |TV INTERACTIVA|UNE TV','TELEVISION')\
            .str.replace('Internet Banda Ancha','INTERNET').str.replace('UNE MOVIL','UNEMOVIL')
        conteo3=df['Descripcion producto'].value_counts().iloc[:7].index.tolist()
        df['Descripcion producto_resumen']=df.apply(
        lambda row: row['Descripcion producto']  if (row['Descripcion producto'] in conteo3)
        else 'OTRO PRODUCTO',axis=1)
        df['Descripcion producto_resumen']=df['Descripcion producto_resumen'].str.strip()
        df['Tipo Contactabilidad'][df['Tipo Contactabilidad']==' '] ='NO REGISTRA'
        df['Indicador BI'][df['Indicador BI']==' '] ='NO REGISTRA'
        ## Create variable 
        df['antiguedad_mes']=df['antiguedad_mes'].astype(int)
        col         = 'antiguedad_mes'
        condi = [ df[col] < 12, df[col].between(12, 24, inclusive = True),df[col]>24 ]
        seg_     = [ "SEGMENTO YOUNG", 'SEGMENTO MASTER','SEGMENTO LEGEND'] 
        df["Hogar"] = np.select(condi, seg_, default=np.nan)

        df['CalificaciÃ³n A Nivel De SuscripciÃ³n'][df['CalificaciÃ³n A Nivel De SuscripciÃ³n']==' ']=df['CalificaciÃ³n A Nivel De SuscripciÃ³n'].mode()[0]
        df['CalificaciÃ³n A Nivel De SuscripciÃ³n']=df['CalificaciÃ³n A Nivel De SuscripciÃ³n'].astype('int')
        df['Califica_suscr_class']=pd.cut(df['CalificaciÃ³n A Nivel De SuscripciÃ³n'],bins=5,labels=["A","B","C","D","E"]).astype(str)

        df['Tipo De Documento'][df['Tipo De Documento']=='13'] ='NO REGISTRA'
        df['Tipo De Documento']=df['Tipo De Documento'].fillna('NO REGISTRA')
        df['Tipo De Documento'][df['Tipo De Documento']=='1'] ='CC'
        df['Tipo De Documento'][df['Tipo De Documento']==' '] ='NO REGISTRA'
        df['Tipo De Documento'][df['Tipo De Documento']=='C'] ='NO REGISTRA'
        df['Tipo De Documento']=df['Tipo De Documento'].str.replace('3 Cedula Extranjeria|3|1CE','CE')\
                                                        .str.replace('1 Cedula','CC')\
                                                        .str.replace('2 Nit|2',' Nit')\
                                                        .str.replace('4 Tarjeta de Identidad|4',' TI')
        #### Create, clean & group variables
        df['Banco 1'][df['Banco 1']==' '] ='NO REGISTRA'
        df['Banco 2'][df['Banco 2']==' '] ='NO REGISTRA'
        df['Banco 1'].fillna('NO REGISTRA',inplace=True)
        df['Banco 2'].fillna('NO REGISTRA',inplace=True)
        df['Banco 1']=df['Banco 1'].str.upper().str.strip()
        df['Banco 2']=df['Banco 2'].str.upper().str.strip()
        df['Banco 1']=df['Banco 1'].str.replace('BANCO COLPATRIA','COLPATRIA')\
                                    .str.replace('COLPATRIA ENLINEA','COLPATRIA EN LINEA')\
                                    .str.replace('GANA GANA','GANA')\
                                    .str.replace('GANA GANA','GANA')
        df["Banco 1_virtual"] =\
                np.where(df["Banco 1"].str.contains("LINEA|PSE|BOTON",regex = True,na = False),"1","0")
        df["Banco 2_Virtual"] =\
                np.where(df["Banco 2"].str.contains("LINEA|PSE|BOTON",regex = True,na = False),"1","0")
        conteo_banco=df['Banco 1'].value_counts().iloc[:10].index.tolist()
        df['Banco 1_Cl']=df.apply(
            lambda row: row['Banco 1']  if (row['Banco 1'] in conteo_banco)
            else 'OTRO BANCO',axis=1)
        conteo_banco2=df['Banco 2'].value_counts().iloc[:10].index.tolist()
        df['Banco 2_Cl']=df.apply(
            lambda row: row['Banco 2']  if (row['Banco 2'] in conteo_banco2)
            else 'OTRO BANCO',axis=1)

        df['Causal'][df['Causal']==' '] ='NO REGISTRA'
        df['Causal_Cl']=df['Causal']\
        .str.replace('FACTURA MAYOR A LA CAPACIDAD DE PAGO|CLIENTE SE ACOGE PRODUCTO MINIMO VITAL|PRIORIDAD INGRESOS A LA CANASTA BASICA|INDISPONIBILIDAD DE MEDIOS DE PAGO POR EMERGENCIA SANITARIA|NO TIENE DINERO|INCONVENIENTES ECONOMICOS|INCONVENIENTES ECONOMICOS|CONTINGENCIA COVID-19|DESEMPLEADO|INDEPENDIENTE SIN INGRESOS DURANTE CUARENTENA|DISMINUCIÃ“N INGRESOS / INCONVENIENTES CON NÃ“MINA',
                    'DISMINUCIÓN DE INGRESOS')\
        .str.replace('OLVIDO DE PAGO|FUERA DE LA CIUDAD|DEUDOR SE OLVIDO DEL PAGO|OLVIDO DEL PAGO / ESTA DE VIAJE',
                    'OLVIDO')\
        .str.replace('PAGA CADA DOS MESES|PAGO BIMESTRAL','PAGO BIMESTRAL')\
        .str.replace('INCONFORMIDAD EN EL VALOR FACTURADO|INCONFORMIDAD POR CAMBIO DE DOMICILIO|INCOMFORMIDAD POR CAMBIO DE DOMICILIO|PQR PENDIENTE|TIENE RECLAMO PENDIENTE','INCONFORMIDAD')\
        .str.replace('OTRA PERSONA ES LA ENCARGADA DEL PAGO','OTRA PERSONA ES LA ENCARGADA DEL PAGO').str.strip()\
        .str.replace('PROBLEMAS FACTURACIÓN|INCONSISTENCIAS EN CARGOS FACTURADOS|RECLAMACIÃ“N EN TRÃMITE|NO LE LLEGA LA FACTURA / LLEGO DESPUES DE LA FECHA DE VENCIMIENTO|LLEGO LA FACTURA DESPUES DE LA FECHA DE VENCIMIENTO|NO LLEGO FACTURA',
                    'FACTURA')\
        .str.replace('SE NIEGA A RECIBIR INFORMACION',
                    'RENUENTE')\
        .str.replace('INCONVENIENTES CON CANALES DE PAGO|NO HAY PROGRAMACION DEL PAGO|INCONVENIENTES CON EL CANAL DE RECAUDO|NO HAY PROGRAMACION DEL PAGO|INCONVENIENTES CON LA ENTIDAD BANCARIA',
                    'INCONVENIENTES CON PAGO')\
        .str.replace('REALIZARA RETIRO DEL SERVICIO|REALIZARA RETIRO / CANCELACION SERVICIO',
                    'REALIZARA RETIRO')
        conteo_Causa=df['Causal_Cl'].value_counts().iloc[:12].index.tolist()
        df['Causal_Cl']=df.apply(
            lambda row: row['Causal_Cl']  if (row['Causal_Cl'] in conteo_Causa)
            else 'OTRA CAUSA',axis=1)

        conteo_Corte=df['Descripcion estado de corte'].value_counts().iloc[:12].index.tolist()
        df['Descripcion estado de corte_Cl']=df.apply(
            lambda row: row['Descripcion estado de corte']  if (row['Descripcion estado de corte'] in conteo_Corte)
            else 'OTRA MOTIVO',axis=1)
        df['Descripcion estado de corte_conexión'] = np.where(df['Descripcion estado de corte'].str.contains("CONEXION"),"1",'0')
        df['Descripcion estado de corte_suspención'] = np.where(df['Descripcion estado de corte'].str.contains("SUSPENSION"),"1",'0')
        df['Descripcion estado de corte_retiro'] = np.where(df['Descripcion estado de corte'].str.contains("RETIRO"),"1",'0')
        df['Valor Total Cobrar']=df['Valor Total Cobrar'].astype('float64')
        df['Valor Vencido']=df['Valor Vencido'].astype('float64')
        df['Valor Factura']=df['Valor Factura'].astype('float64')
        df['Valor Intereses de Mora']=df['Valor Intereses de Mora'].astype('float64')
        df['Valor financiado']=df['Valor financiado'].astype('float64')
        ## DROPING VARIABLES
        df.drop(['Causal','Codigo edad de mora(para central de riesgos)','Codigo edad de mora(para central de riesgos)',
         'Estado Adminfo','Celular con mejor Contactabilidad','Archivo Convergente','Usuario','Vector de Pago'],axis=1,inplace=True)
        anis=['TelÃ©fono Ãºltima gestiÃ³n','Email','Telefono con mejor Contactabilidad','Email',
            'Ultimo Celular Grabado','Ultimo Telefono Grabado','Ultimo Email Grabado','Celular con mejor Contactabilidad']
        df.dropna(subset = ["Direccion de instalacion"], inplace=True)
        df['llave']=df['Identificacion']+"_"+df['Direccion de instalacion']
        df=df.sort_values('Fecha de Asignacion',ascending=True)
        ## Elimino los duplicados presnetados en la combinación de dichas variables
        df=df[~df[['llave','# servicio suscrito/abonado','Fecha de Asignacion','Valor Total Cobrar','Valor Vencido','Descripcion localidad']].duplicated()]
        df.sort_values(by=['Identificacion','# servicio suscrito/abonado','Fecha de Asignacion'],ascending=[True,True,True]).drop_duplicates('# servicio suscrito/abonado',keep='last',inplace=True)

        ### Cuidado con esos pendientes por gestionar
        ## Cantidad de servicios
        cant_serv=df.groupby(['Identificacion']).agg({'Descripcion producto':'nunique','Direccion de instalacion':'nunique'})\
        .reset_index().sort_values('Descripcion producto',ascending=False)\
        .rename(columns={'Descripcion producto':'cantidad_ser_dir','Direccion de instalacion':'serv_dir'})
        df=pd.merge(df,cant_serv,on='Identificacion')
        df=df[~df.duplicated()]
        # Creo dicha variabel para evitar que hayan duplicados el mismo día
        df['llave_2']=df['Identificacion']+"_"+(df['Fecha de Asignacion'].astype('str'))
        #
        conteo=df.groupby(['Identificacion','Fecha de Asignacion','Fecha de Asignacion_mes']).agg({'Identificacion':'nunique'}).rename(columns={'Identificacion':'cantidad_mes'}).reset_index()
        conteo.sort_values('Fecha de Asignacion',ascending=True,inplace=True)
        conteo=conteo[~conteo['Identificacion'].duplicated(keep='last')]
        conteo['llave_2']=conteo['Identificacion']+"_"+(conteo['Fecha de Asignacion'].astype('str'))


        #Se crea con el fin de identificar y quedarme con las claves de cada uno
        consolidar=pd.merge(df,conteo['llave_2'],on='llave_2')
        #Creo variables dummies para identificar en una misma cantidad de servicios
        cer1=pd.concat([pd.get_dummies(consolidar['Descripcion producto_resumen']),consolidar],axis=1) # concateno
        cer1['llave_2']=cer1['Identificacion']+"_"+(cer1['Fecha de Asignacion'].astype('str'))

        cer=cer1.groupby(['Identificacion']).agg({
                                        'Descripcion producto_resumen':np.array,'Descripcion producto_resumen':'sum',
                                        'TELEFONIA':'sum','INTERNET':'sum','TELEVISION':'sum','UNEMOVIL':'sum',
                                        'LARGA DISTANCIA UNE':'sum','PAQUETE':'sum','OTRO PRODUCTO':'sum','LINEA BASICA':'sum',
                                        "Valor Vencido":"sum","Valor Total Cobrar":"sum",
                                        "Valor financiado":"sum",
                                        "Valor Intereses de Mora":"sum"}).reset_index().\
                                        rename(columns={'Valor Vencido':'valor vencido_sum',
                                                        'Valor Factura':'Valor Factura_sum',
                                                        'Valor financiado':'Valor financiado_sum',
                                                        'Valor Total Cobrar':'Valor Total Cobrar_sum',
                                                        'Descripcion producto_resumen':'Total servicio',
                                                        'Valor Intereses de Mora':'Valor Intereses de Mora_sum'})
        cer.drop(['Total servicio'],axis=1,inplace=True)
        data=pd.merge(consolidar,cer,on='Identificacion')
        data=data.sort_values(['Fecha de Asignacion','Identificacion'],ascending=[True,True]).drop_duplicates('Identificacion',keep='last')
        ### Base de datos de la salida
        out.sort_values(['Identificacion Del Cliente','Fecha_Gestion'],ascending=[True,True]).drop_duplicates(keep='last',inplace=True)
        out.drop(['Unnamed: 19'],axis=1,inplace=True)
        ## Cruce de bases de datos de salida
        full=pd.merge(data,out[['Identificacion Del Cliente','Efectivo Pago','Fecha_Pago']],
              left_on='Identificacion',right_on='Identificacion Del Cliente')
        full=full[~full.duplicated()]
        full=full.sort_values(['Identificacion','Efectivo Pago'],ascending=[True,True]).drop_duplicates(['Identificacion'],keep='first')
        full['llave_exp']=full['Identificacion']+full['# servicio suscrito/abonado']

        
        full['valor vencido_sum'][full['valor vencido_sum'] < 0] = 0
        full['ratio_vlr_vencido_cobro']=full['valor vencido_sum']/full['Valor Total Cobrar_sum']
        full.drop(['llave_2','Direccion de instalacion','Banco 1','Banco 2'],axis=1,inplace=True)
        
        ### Exporto y envio a la carpeta para trabajarlo
        seg['FECHA DE GESTION']=pd.to_datetime(seg['FECHA DE GESTION'],format='%Y-%m-%d %H:%M:%S')
        seg=seg.sort_values(['IDENTIFICACIÃ³N','FECHA DE GESTION']).drop_duplicates('IDENTIFICACIÃ³N',keep='last')


        vir['Identificación']=vir['Identificación'].astype('str')
        fulll=pd.merge(full,seg[['IDENTIFICACIÃ³N','FECHA DE GESTION','CLASE DE GESTION',
                         'LINEA/AGENCIA/ABOGADO','CAUSAL','CICLO','OTRA GESTION',
                         'SE DEJO MENSAJE EN BUZON', 'DEUDOR REALIZA PROMESA DE PAGO TOTAL',
                         'NO CONTESTAN / OCUPADO', 'DEUDOR REALIZA PROMESA DE PAGO PARCIAL',
                         'NO HUBO ACUERDO', 'SE ENVIA CUPON DE PAGO','SE DEJO MENSAJE CON TERCERO',
                         'OTRA GESTION_sum', 'Total_segui','Cantidad_de_cobros_diff_mes', 'Cantidad_recontactos_mes',
                        'class_Cantidad_de_cobros_diff_mes','class_Cantidad_recontactos_mes']],
               left_on='Identificacion',right_on='IDENTIFICACIÃ³N',how='left').\
                merge(vir,left_on='Identificacion',right_on='Identificación',how='left')
        #libero memoria
        del cer
        del cer1
        fulll["Efectivo Pago"] = (fulll["Efectivo Pago"]=="Efectivo").astype(int)
        fulll.drop(['Valor financiado_sum','Fecha_Pago','Valor Intereses de Mora_sum','Valor Total Cobrar','Valor Total Cobrar_sum','Valor Intereses de Mora','Agencia B2B Convergente','Codigo Fraude','CAUSAL','LINEA/AGENCIA/ABOGADO',
         'Celular','Valor financiado','# servicio suscrito/abonado','Fecha Ult pago','Fecha estado corte','Codigo Departamento','Centrales de riesgos','dias_desde_ult_gestion',
         'Valor Honorarios','Dias_ult_pago','dia_semana_ult_pago','mes_ult_pago','semana_ult_pago','Marca','Marca Funcional','Reportado a central de riesgos','Marca Score','Autopago',
         'trimestre_ult_pago','año_ult_pago','DIAS_desde_ult_pago','dias_ult_pago_cobro','Primera Mora','CICLO','Codigo Categoria','Subsegmento',
         'dias_ult_pago_fac_ant','Fecha de cuenta de cobro mas antigua','Fecha estado corte','Fecha estado corte','Descripcion Gestion Resultado'],axis=1,inplace=True)

        dd=fulll.copy()


        dd['class_Cantidad_recontactos_mes']=dd['class_Cantidad_recontactos_mes'].fillna('0')
        dd['class_Cantidad_de_cobros_diff_mes'].fillna('0',inplace=True)
        # dd['CalificaciÃ³n Servicio Suscrito'][dd['CalificaciÃ³n Servicio Suscrito']==' '] = np.nan
        # dd['CalificaciÃ³n Servicio Suscrito']=dd['CalificaciÃ³n Servicio Suscrito'].astype(float)
        dd['Fecha de Asignacion']=pd.to_datetime(dd['Fecha de Asignacion'],format='%Y-%m-%d') 
        dd['Fecha Ult Gestion']=pd.to_datetime(dd['Fecha Ult Gestion'],format='%Y-%m-%d')
        dd['Fecha Actualizacion']=pd.to_datetime(dd['Fecha Actualizacion'],format='%Y-%m-%d') 
        dd['Fecha Vencimiento Sin Recargo']=pd.to_datetime(dd['Fecha Vencimiento Sin Recargo'],format='%Y-%m-%d') 
        # dd['Fecha de cuenta de cobro mas antigua']=pd.to_datetime(dd['Fecha de cuenta de cobro mas antigua'],format='%Y-%m-%d') 
        dd['FECHA DE GESTION']=pd.to_datetime(dd['FECHA DE GESTION'],format='%Y-%m-%d %H:%M:%S') 
        dd['Fecha Debido Cobrar']=pd.to_datetime(dd['Fecha Debido Cobrar'],format='%Y-%m-%d %H:%M:%S', errors='coerce')
        dd['Score Contactabilidad'][dd['Score Contactabilidad']==' '] =np.nan
        dd['Score Contactabilidad']=dd['Score Contactabilidad'].fillna(dd['Score Contactabilidad'].median())
        dd['Score Contactabilidad']=dd['Score Contactabilidad'].astype('float')
        dd['Tiene Compromiso'] = (dd['Tiene Compromiso']=="S").astype(int)
        # dd['CalificaciÃ³n Servicio Suscrito'][dd['CalificaciÃ³n Servicio Suscrito']==' '] =0
        # dd['CalificaciÃ³n Servicio Suscrito']=dd['CalificaciÃ³n Servicio Suscrito'].astype(float)
        dd['Financiado'] = (dd["Financiado"]=="SI").astype(int)
        dd['Obligaciones con celular']= (dd['Obligaciones con celular']=="S").astype(int)
        dd['Inscrito Factura Web']= (dd['Inscrito Factura Web']=="S").astype(int)
        dd['Real reportado en central de riesgos']= (dd['Real reportado en central de riesgos']=="S").astype(int)
        dd['Tipo Habito de Pago'][dd['Tipo Habito de Pago']==' '] ='NO REGISTRA'
        dd['CalificaciÃ³n IdentificaciÃ³n'][dd['CalificaciÃ³n IdentificaciÃ³n']==' '] =dd["CalificaciÃ³n IdentificaciÃ³n"].mode()[0]
        dd["CalificaciÃ³n IdentificaciÃ³n"]=dd["CalificaciÃ³n IdentificaciÃ³n"].astype(float)
        dd['CLASE DE GESTION'][dd['CLASE DE GESTION']==' ']='NO REGISTRA'
        ### Clasificaciones
        dd['Class_Total valor pendiente suscripcion']=pd.qcut(dd['Total valor pendiente suscripcion'].astype(float), 5,
                                                      labels=["A", "B", "C","D","E"]).astype('str')
        dd['Total valor pendiente suscripcion']=dd['Total valor pendiente suscripcion'].astype(float)
        dd['Valor Pendiente']=dd['Valor Pendiente'].astype(float)
        dd['# de Dias De Mora']=dd['# de Dias De Mora'].astype(float)
        dd['Dias sin Gestion']=dd['Dias sin Gestion'].astype(float)
        dd['antiguedad_mes']=dd['antiguedad_mes'].astype(float)
        dd['Minimo Cuentas con Saldo SuscripciÃ³n']=dd['Minimo Cuentas con Saldo SuscripciÃ³n'].astype(float)
        dd['Maximo Cuentas con Saldo SuscripciÃ³n']=dd['Maximo Cuentas con Saldo SuscripciÃ³n'].astype(float)
        dd['Total_segui']=dd['Total_segui'].astype(float)
        ### OULIERS
        qtil9_vlrvencido=dd['valor vencido_sum'].quantile(0.95)
        qtil9_vlfac=dd['Valor Factura'].quantile(0.90)
        qtil9_total=dd['Total valor pendiente suscripcion'].quantile(0.90)
        qtil9_total_ven=dd['Valor Vencido'].quantile(0.90)
        qtil_75_dia=dd['# de Dias De Mora'].quantile(0.75)
        qtil_75_dia_ges=dd['Dias sin Gestion'].quantile(0.80)
        qtil_mes=dd['antiguedad_mes'].quantile(0.95)
        qtil_min_cuentas=dd['Minimo Cuentas con Saldo SuscripciÃ³n'].quantile(0.99)
        qtil_max_cuentas=dd['Maximo Cuentas con Saldo SuscripciÃ³n'].quantile(0.99)
        qtil_sus=dd['Dias Suspension'].quantile(0.85)
        qtil_segui=dd['Total_segui'].quantile(0.95)
        dd['valor vencido_sum']= np.where(dd["valor vencido_sum"] > qtil9_vlrvencido, qtil9_vlrvencido ,dd["valor vencido_sum"])
        dd['Valor Factura'] = np.where(dd['Valor Factura'] > qtil9_vlfac, qtil9_vlfac,dd["Valor Factura"])
        dd['Valor Factura'] = np.where(dd['Valor Factura'] < 0, dd["Valor Factura"].quantile(0.5),dd["Valor Factura"])
        dd['Total valor pendiente suscripcion']=np.where(dd['Total valor pendiente suscripcion'] > qtil9_total, qtil9_total,dd["Total valor pendiente suscripcion"])
        dd['Valor Vencido']=np.where(dd['Valor Vencido'] > qtil9_total_ven, qtil9_total_ven,dd["Valor Vencido"])
        dd['Valor Vencido']=np.where(dd['Valor Vencido'] < dd['Valor Vencido'].quantile(0.1), dd['Valor Vencido'].quantile(0.3),dd["Valor Vencido"])
        dd['# de Dias De Mora']=np.where(dd['# de Dias De Mora'] > qtil_75_dia, qtil_75_dia,dd['# de Dias De Mora'])
        dd['Dias sin Gestion']=np.where(dd['Dias sin Gestion'] > qtil_75_dia_ges, qtil_75_dia_ges,dd['Dias sin Gestion'])
        dd['ratio_vlr_vencido_cobro'].fillna(dd['ratio_vlr_vencido_cobro'].median(),inplace=True)
        dd['CalificaciÃ³n Servicio Suscrito'][dd['CalificaciÃ³n Servicio Suscrito']==' '] = np.nan
        dd['CalificaciÃ³n Servicio Suscrito']=dd['CalificaciÃ³n Servicio Suscrito'].fillna(dd['CalificaciÃ³n Servicio Suscrito'].median())
        dd['antiguedad_mes']=np.where(dd['antiguedad_mes'] > qtil_mes, qtil_mes,dd['antiguedad_mes'])
        dd['Minimo Cuentas con Saldo SuscripciÃ³n']=np.where(dd['Minimo Cuentas con Saldo SuscripciÃ³n'] > qtil_min_cuentas, qtil_min_cuentas,dd['Minimo Cuentas con Saldo SuscripciÃ³n'])
        dd['Maximo Cuentas con Saldo SuscripciÃ³n']=np.where(dd['Maximo Cuentas con Saldo SuscripciÃ³n'] > qtil_max_cuentas, qtil_max_cuentas,dd['Maximo Cuentas con Saldo SuscripciÃ³n'])
        dd['Dias Suspension']=np.where(dd['Dias Suspension'] > qtil_sus, qtil_sus,dd['Dias Suspension'])
        ### Drop 
        dd.drop(['Descripcion Mejor Codigo Gestion Mes','Codigo de Gestion Resultado Visita','AnÃ¡lisis Vector',
         'Fecha de Instalacion','DÃ­a Pago 3','Descripcion localidad',
         'Fecha Ingreso Fraude','Maxima fecha Ult Gestion','Usuario Grabador',
         'DÃ­a Pago 1','DÃ­a Pago 2','Ultimo Codigo de Gestion Agrupado','# de SuscripciÃ³n',
         'fecha de importacion',
         'Fecha de Asignacion_mes','Descripcion producto','Fecha Financiacion','Codigo estado de corte','Descripcion estado de corte'],axis=1,inplace=True)

        dd.ratio_vlr_vencido_cobro.fillna(dd.ratio_vlr_vencido_cobro.median(),inplace=True)
        dd['retiro']=np.where(dd['Fecha Retiro'].isna(),0,1)
        dd.drop(['Nivel de riesgo experian','Fecha Retiro','Nivel de Riesgo','Indicador BI','Tipo Contactabilidad',
         'Gestion comercial','Estrategia','Usuario Fraudulento','Tipo de Reporte a Central de Riesgos','Banco 2_Cl'],axis=1,inplace=True)

        dd.ratio_vlr_vencido_cobro.fillna(dd.ratio_vlr_vencido_cobro.median(),inplace=True)
        dd['Efectivo Pago']=dd['Efectivo Pago'].astype(str)
        dd['Class_Total valor pendiente suscripcion']=dd['Class_Total valor pendiente suscripcion'].astype('str')
        dd['Califica_suscr_class']=dd['Califica_suscr_class'].astype('str')


        dd['# de Dias De Mora'].fillna(0,inplace=True)
        breaks3 = jenkspy.jenks_breaks(dd['# de Dias De Mora'], nb_class=8)
        dd['class_# de Dias De Mora'] = pd.cut(dd['# de Dias De Mora'] , bins=breaks3, include_lowest=True).astype(str)
        breaks2 = jenkspy.jenks_breaks(dd['ratio_vlr_vencido_cobro'], nb_class=5)
        dd['class_ratio_vlr_vencido_cobro_class'] = pd.cut(dd['ratio_vlr_vencido_cobro'] , bins=breaks2, include_lowest=True).astype(str)
        dd['Total'].fillna(0,inplace=True)
        dd['Total_clasificacion_cant_virtuales'] = pd.cut(x=dd['Total'],
                             bins=[-1,0,1,2,3,6,10,17,30,1000], 
                             labels=["0","1","2","3","4-6","7-10", "11-17","18-30", ">30"]).astype(str).fillna('0')
        ### Divido 
        sin_seg=dd[dd['IDENTIFICACIÃ³N'].isna()]
        sin_seg.drop(sin_seg[sin_seg.columns[79:139]].columns,axis=1,inplace=True)
        # con seguimiento
        dd=dd[~dd['IDENTIFICACIÃ³N'].isna()]

        grupo=dd.groupby(['Efectivo Pago','Descripcion departamento', 'sistema origen',
        'Vector Cualitativo # SuscripciÃ³n', 'TipificaciÃ³n Cliente',
        'Perfil Digital', 'Descripcion subcategoria', 'Descripcion categoria', 'Estado del Cliente',
        'Tipo Habito de Pago', 'Tipo Producto Servicio Suscrito', 'Analisis De Habito','Hogar',
        'Califica_suscr_class', 'Banco 1_Cl','Descripcion estado de corte_Cl','class_Cantidad_de_cobros_diff_mes',
        'class_Cantidad_recontactos_mes', 'Class_IVR',
        'Class_sms','Class_Total valor pendiente suscripcion','Total_clasificacion_cant_virtuales',
                  'class_ratio_vlr_vencido_cobro_class','class_# de Dias De Mora']).size().reset_index(name='frecuency')
        # dic_reg=pd.crosstab(grupo['Descripcion Regional'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_des_dep=pd.crosstab(grupo['Descripcion departamento'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_vec_cua=pd.crosstab(grupo['Vector Cualitativo # SuscripciÃ³n'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_sis_origen=pd.crosstab(grupo['sistema origen'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_tipi_clien=pd.crosstab(grupo['TipificaciÃ³n Cliente'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_per_dig=pd.crosstab(grupo['Perfil Digital'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_desc_sub=pd.crosstab(grupo['Descripcion subcategoria'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_desc_sus=pd.crosstab(grupo['Tipificacion suscripcion'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_ant_clie=pd.crosstab(grupo['Antiguedad Cliente'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_desc_cat=pd.crosstab(grupo['Descripcion categoria'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_est_cliente=pd.crosstab(grupo['Estado del Cliente'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_hab=pd.crosstab(grupo['Tipo Habito de Pago'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_sus_tipo=pd.crosstab(grupo['Tipo Producto Servicio Suscrito'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ana_habi=pd.crosstab(grupo['Analisis De Habito'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ana_hogar=pd.crosstab(grupo['Hogar'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_cali=pd.crosstab(grupo['Califica_suscr_class'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ban=pd.crosstab(grupo['Banco 1_Cl'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_corte=pd.crosstab(grupo['Descripcion estado de corte_Cl'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_pend_sus=pd.crosstab(grupo['Class_Total valor pendiente suscripcion'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_sms=pd.crosstab(grupo['Class_sms'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ivr=pd.crosstab(grupo['Class_IVR'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_CE=pd.crosstab(grupo['class_CE'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_mora=pd.crosstab(grupo['class_# de Dias De Mora'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ratio=pd.crosstab(grupo['class_ratio_vlr_vencido_cobro_class'],grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()


        #dd['Descripcion Regional2']=dd['Descripcion Regional'].replace(dic_reg)
        dd['Descripcion departamento2']=dd['Descripcion departamento'].replace(dic_des_dep)
        dd['Vector Cualitativo # SuscripciÃ³n2']=dd['Vector Cualitativo # SuscripciÃ³n'].replace(dic_vec_cua)
        dd['sistema origen2']=dd['sistema origen'].replace(dic_sis_origen)
        dd['TipificaciÃ³n Cliente2']=dd['TipificaciÃ³n Cliente'].replace(dic_tipi_clien)
        dd['Perfil Digital2']=dd['Perfil Digital'].replace(dic_per_dig)
        dd['Descripcion subcategoria2']=dd['Descripcion subcategoria'].replace(dic_desc_sub)
        # dd['Tipificacion suscripcion2']=dd['Tipificacion suscripcion'].replace(dic_desc_sus)
        # dd['Antiguedad Cliente2']=dd['Antiguedad Cliente'].replace(dic_ant_clie)
        dd['Descripcion categoria2']=dd['Descripcion categoria'].replace(dic_desc_cat)
        # dd['Estado del Cliente2']=dd['Estado del Cliente'].replace(dic_est_cliente)
        dd['Tipo Habito de Pago2']=dd['Tipo Habito de Pago'].replace(dic_hab)
        dd['Tipo Producto Servicio Suscrito2']=dd['Tipo Producto Servicio Suscrito'].replace(dic_sus_tipo)
        dd['Analisis De Habito2']=dd['Analisis De Habito'].replace(dic_ana_habi)
        dd['Hogar2']=dd['Hogar'].replace(dic_ana_hogar)
        dd['Califica_suscr_class2']=dd['Califica_suscr_class'].replace(dic_cali)
        dd['Banco 1_Cl2']=dd['Banco 1_Cl'].replace(dic_ban)
        dd['Descripcion estado de corte_Cl2']=dd['Descripcion estado de corte_Cl'].replace(dic_corte)
        dd['Class_Total valor pendiente suscripcion2']=dd['Class_Total valor pendiente suscripcion'].replace(dic_pend_sus)
        dd['Class_sms2']=dd['Class_sms'].replace(dic_sms)
        dd['Class_IVR2']=dd['Class_IVR'].replace(dic_ivr)
        # dd['class_CE2']=dd['class_CE'].replace(dic_CE)
        dd['class_# de Dias De Mora2']=dd['class_# de Dias De Mora'].replace(dic_mora)
        dd['class_ratio_vlr_vencido_cobro_class2']=dd['class_ratio_vlr_vencido_cobro_class'].replace(dic_ratio)
        dd['Class_sms2'].fillna(0.5,inplace=True)
        dd['Class_IVR2'].fillna(0.5,inplace=True)
        #dd['class_CE2'].fillna(0.5,inplace=True)
        dic_reco=pd.crosstab(grupo['class_Cantidad_de_cobros_diff_mes'].astype(str),grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_reco_mes=pd.crosstab(grupo['class_Cantidad_recontactos_mes'].astype(str),grupo['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dd['class_Cantidad_recontactos_mes2']=dd['class_Cantidad_recontactos_mes'].replace(dic_reco_mes)
        dd['class_Cantidad_de_cobros_diff_mes2']=dd['class_Cantidad_de_cobros_diff_mes'].replace(dic_reco)
        dd['class_Cantidad_de_cobros_diff_mes2'].fillna('0',inplace=True)
        dd['Estandar']=dd[dd.filter(like='2').columns.drop(['Banco 2_Virtual','12', '20', '21', '22', '23'])].sum(axis=1)
        labels=["Deficiente", "Malo",'Regular',"Bueno","Muy bueno"]
        breaks = jenkspy.jenks_breaks(dd['Estandar'], nb_class=5)
        dd['cut_break'] = pd.cut(dd['Estandar'] , bins=breaks, labels=labels, include_lowest=True)
        ## comienzo con el seguimiento
        grupo_2=sin_seg.groupby(['Efectivo Pago','Descripcion departamento', 'sistema origen',
       'Vector Cualitativo # SuscripciÃ³n',
       'Perfil Digital', 'Descripcion subcategoria',
        'Descripcion categoria', 'Estado del Cliente',
        'Tipo Habito de Pago',
       'Analisis De Habito', 'Descripcion producto_resumen',
       'Hogar', 'Califica_suscr_class', 'Banco 1_Cl', 'Causal_Cl',
       'Descripcion estado de corte_Cl','Class_Total valor pendiente suscripcion','Total_clasificacion_cant_virtuales',
                  'class_ratio_vlr_vencido_cobro_class','class_# de Dias De Mora']).size().reset_index(name='frecuency')
        # dic_reg=pd.crosstab(grupo_2['Descripcion Regional'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_des_dep=pd.crosstab(grupo_2['Descripcion departamento'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_vec_cua=pd.crosstab(grupo_2['Vector Cualitativo # SuscripciÃ³n'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_sis_origen=pd.crosstab(grupo_2['sistema origen'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_dias_mora=pd.crosstab(grupo_2['class_# de Dias De Mora'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_per_dig=pd.crosstab(grupo_2['Perfil Digital'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_desc_sub=pd.crosstab(grupo_2['Descripcion subcategoria'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_desc_sus=pd.crosstab(grupo_2['Tipificacion suscripcion'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_ant_clie=pd.crosstab(grupo_2['Antiguedad Cliente'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_desc_cat=pd.crosstab(grupo_2['Descripcion categoria'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_est_cliente=pd.crosstab(grupo_2['Estado del Cliente'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_hab=pd.crosstab(grupo_2['Tipo Habito de Pago'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # dic_sus_tipo=pd.crosstab(grupo_2['Tipo Producto Servicio Suscrito'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ana_habi=pd.crosstab(grupo_2['Analisis De Habito'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ana_hogar=pd.crosstab(grupo_2['Hogar'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_cali=pd.crosstab(grupo_2['Califica_suscr_class'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_ban=pd.crosstab(grupo_2['Banco 1_Cl'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_corte=pd.crosstab(grupo_2['Descripcion estado de corte_Cl'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        dic_pend_sus=pd.crosstab(grupo_2['Class_Total valor pendiente suscripcion'],grupo_2['Efectivo Pago']).apply(lambda r: r/r.sum(), axis=1)['1'].to_dict()
        # sin_seg['Descripcion Regional2']=sin_seg['Descripcion Regional'].replace(dic_reg)
        sin_seg['Descripcion departmento2']=sin_seg['Descripcion departamento'].replace(dic_des_dep)
        sin_seg['Vector Cualitativo # SuscripciÃ³n2']=sin_seg['Vector Cualitativo # SuscripciÃ³n'].replace(dic_vec_cua)
        sin_seg['sistema origen2']=sin_seg['sistema origen'].replace(dic_sis_origen)
        sin_seg['class_# de Dias De Mora2']=sin_seg['class_# de Dias De Mora'].replace(dic_dias_mora)
        sin_seg['Perfil Digital2']=sin_seg['Perfil Digital'].replace(dic_per_dig)
        sin_seg['Descripcion subcategoria2']=sin_seg['Descripcion subcategoria'].replace(dic_desc_sub)
        # sin_seg['Tipificacion suscripcion2']=sin_seg['Tipificacion suscripcion'].replace(dic_desc_sus)
        # sin_seg['Antiguedad Cliente2']=sin_seg['Antiguedad Cliente'].replace(dic_ant_clie)
        sin_seg['Descripcion categoria2']=sin_seg['Descripcion categoria'].replace(dic_desc_cat)
        sin_seg['Estado del Cliente2']=sin_seg['Estado del Cliente'].replace(dic_est_cliente)
        sin_seg['Tipo Habito de Pago2']=sin_seg['Tipo Habito de Pago'].replace(dic_hab)
        # sin_seg['Tipo Producto Servicio Suscrito2']=dd['Tipo Producto Servicio Suscrito'].replace(dic_sus_tipo)
        sin_seg['Analisis De Habito2']=sin_seg['Analisis De Habito'].replace(dic_ana_habi)
        sin_seg['Hogar2']=sin_seg['Hogar'].replace(dic_ana_hogar)
        sin_seg['Califica_suscr_class2']=sin_seg['Califica_suscr_class'].replace(dic_cali)
        sin_seg['Banco 1_Cl2']=sin_seg['Banco 1_Cl'].replace(dic_ban)
        sin_seg['Descripcion estado de corte_Cl2']=sin_seg['Descripcion estado de corte_Cl'].replace(dic_corte)
        sin_seg['Class_Total valor pendiente suscripcion2']=sin_seg['Class_Total valor pendiente suscripcion'].replace(dic_pend_sus)
        labels=["Deficiente", "Malo",'Regular',"Bueno","Muy bueno"]
        sin_seg['Estandar']=sin_seg[sin_seg.filter(like='2').columns.drop(['Banco 2_Virtual'])].sum(axis=1)
        breaks5 = jenkspy.jenks_breaks(sin_seg['Estandar'], nb_class=5)
        sin_seg['cut_break'] = pd.cut(sin_seg['Estandar'] , bins=breaks5, labels=labels, include_lowest=True)
        ### leo el txt
        hoy=pd.read_csv(r'C:\Users\scadacat\Desktop\Ejecable perfiles\495EMTELCO20210617.txt',sep = "|", ## separación del archivo CSV
                        encoding = "utf-8",dtype=str)
        salida1=pd.merge(hoy,dd[['Identificacion','Ciclo_x','Descripcion departamento','Estandar','Perfil Digital','Banco 1_Cl','cut_break']],left_on='Nit Deudor',right_on='Identificacion')
        salida2=pd.merge(hoy,sin_seg[['Identificacion','Ciclo_x','Descripcion departamento','Estandar','Perfil Digital','Banco 1_Cl','cut_break']],left_on='Nit Deudor',right_on='Identificacion')
        temp=pd.concat([salida1,salida2],axis=0)
        temps=pd.concat([temp,hoy[~hoy['Nit Deudor'].isin(temp['Identificacion'])]],axis=0)
        temps['cut_break']=temps['cut_break'].astype('str')
        temps.sort_values('cut_break',ascending=False,inplace=True)
        temps.fillna('No hallado en IGC',inplace=True)
        temps['cut_break']=pd.Categorical(categories=["Muy bueno", "Bueno", "Regular","Malo","Deficiente","No hallado en IGC"],values=temps['cut_break'],ordered=True)
        temps.sort_values('cut_break',inplace=True)
        temps.to_csv(r'C:\Users\scadacat\Desktop\Ejecable perfiles\data_por_ejecutar.csv',sep='|',encoding='utf-8',index=False)

        return print("OK")
# %%
button1 = tk.Button(text='Click aquí para descargar (Recuerda actualizar los datos)',command=profiling, bg='brown',fg='white')
canvas1.create_window(150, 150, window=button1)
root.mainloop()
# %%
