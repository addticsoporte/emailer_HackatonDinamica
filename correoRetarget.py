
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from smtplib import SMTP
import os
import pandas as pd
import pymysql
from datetime import datetime
from decouple import config
API_PASSWORD = config('PASSWORD')
MYSQL_PASSWORD = config('MYSQLPASS')

#Conexion a la base de datos.
connection = pymysql.connect(
    host = "localhost",
    user = "root",
    password = MYSQL_PASSWORD,
    db = "retargettingmysql"
)

cursor = connection.cursor()
hoy = datetime.today().strftime('%Y-%m-%d') #Obtener fecha actual

emisor = input('Ingrese su correo electronico: ')
asunto = input('Ingrese el asunto del correo electrónico: ')
cuerpo = input('Ingrese mensaje o cuerpo del correo electrónico: ')
archivo = input('Ingresar el nombre del archivo a enviar con su respectiva extension: ')

data = pd.read_csv("ProspectosSinTarjeta-20-10-2022 19-42-35.csv")
data_dict = data.to_dict('list')
emails =  data_dict['email']

for email in emails:
    mensaje = MIMEMultipart('plain')
    mensaje['From']=emisor
    mensaje['To']=email
    mensaje['subject']=asunto
    mensaje['body']=cuerpo
    tema = MIMEText(cuerpo,'html')
    mensaje.attach(tema)
    adjunto = MIMEBase('application','octect-scream')
    adjunto.set_payload(open(archivo,'rb').read())
    encode_base64(adjunto)
    adjunto.add_header('content-Disposition','attachment; filename="%s"'% os.path.basename(archivo))
    mensaje.attach(adjunto)
    smtp = SMTP(host='smtp.gmail.com',port=587)
    smtp.starttls()
    smtp.login(emisor,API_PASSWORD)
    smtp.sendmail(emisor,email,mensaje.as_string())
    smtp.quit()
    print('Correo enviado exitosamente a: ',email)

    #Registrar las campanias en una tabla de una base de datos. 
    sql = "INSERT INTO campania(fecha,tipoCanal,asunto,email,telefono,costo) VALUES('{}','email','{}','{}',' ',{})".format(hoy,asunto,email,0)
    cursor.execute(sql)
    connection.commit()
print('============================================')
print('= Programa ejecutado y finalizado correctamente =')
print('============================================')


