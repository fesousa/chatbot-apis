import json
import traceback
import os

import requests
from bs4 import BeautifulSoup

# módulos para envio de e-mail
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def info_get(event, context):    
    print(event)
    req = event['queryStringParameters']
    print(req)
    curso_urls = {
        'ia':'https://www.impacta.edu.br/mba/artificial-intelligence',
        'bigdata':'https://www.impacta.edu.br/mba/business-intelligence-e-analytics',
        'ux':'https://www.impacta.edu.br/mba/ux-design-digital-experience'
    }

    # nome do curso enviado
    curso = req['curso'].replace(' ', '').lower()

    #crawler para pegar informações
    r = requests.get(curso_urls[curso]).text
    info = BeautifulSoup(r, 'html.parser')(class_='content_destaque_sobre')[0].text

    #retornar informações no campo info, no formato JSON
    return {'statusCode': 200, "body":json.dumps({'info':info}), "headers": {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "OPTIONS,GET,POST"}}


def email_post(event, context):    
    req = json.loads(event['body'])
    print(req)
    
    u = os.getenv('USERMAIL')
    g = os.getenv('PWDMAIL')


    try:
        # configuração e envio de email
        message = MIMEMultipart()
        message['From'] = u
        message['To'] = req['email']
        message['Subject'] = 'Confirmação pré-matrícula'
        texto_mensagem = f'<h1>Olá! Sua pré-matrícula no curso de {req["curso"]} para o {req["semestre"]} semestre está confirmada</h1>'
        message.attach(MIMEText(texto_mensagem, 'html'))
        
        session = smtplib.SMTP(os.getenv("SERVERMAIL"), os.getenv("PORTMAIL")) 
        session.starttls()
        session.login(u, g)
        text = message.as_string()
        session.sendmail(u, req['email'], text)
        session.quit()
        # retorno de sucesso no formato JSON
        return {'statusCode': 200, "body":json.dumps({'status':'ok'}), "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"}}
    except Exception as ex:
        print(traceback.print_exc())
        # retorno de erro no formato JSON
        return {'statusCode': 200, "body":json.dumps({'status':'erro'}), "headers": {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST"}}
        
   
