from flask import Flask, request, jsonify, render_template
import datetime
import numpy as np
import pandas as pd
from joblib import load

#Cargar el modelo
dt=load('modelo_rf.joblib')


#Generar el servidor (Back-end)
servidorWeb=Flask(__name__)


@servidorWeb.route("/index",methods=['GET'])
def formulario():
    return render_template('index.html')

@servidorWeb.route('/modelo',methods=['POST'])
def modelo():
    #Procesar datos de entrada
    contenido = request.files['file']
    test=pd.read_csv(contenido)
    #Utilizar el modelo
    resultado=dt.predict(test)
    #Regresar la salida del modelo
    time=resultado[0]*0.01
    dias=str(round(time/86400))
    horas=str(round((time%86400)/3600))
    minutos=str(round(((time%86400)%3600)/60))
    segundos=str(round(((time%86400)%3600)%60,2))
    return render_template("article.html", dias=dias, horas=horas, minutos=minutos, segundos=segundos)
    #return jsonify({"Dia":str(dias),"Hora":str(horas),"Minuto":str(minutos),"Segundos":str(segundos)})


if __name__=='__main__':
    servidorWeb.run(debug=False,host='0.0.0.0',port='8088')
