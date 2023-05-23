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
        
   
