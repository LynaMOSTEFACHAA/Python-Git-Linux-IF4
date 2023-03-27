import subprocess
import dash
from dash import html,dcc
from dash.dependencies import Output, Input
import plotly.graph_objs as go
import pandas as pd
import os
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

#Récupérer la date et l'heure actuelles
output = subprocess.check_output(['bash', '/home/ubuntu/Python-Git-Linux-IF4/script.sh']).decode('utf-8').strip()

# Créer l'application Dash
app = dash.Dash(__name__)

# Définir une liste pour stocker les anciennes valeurs d'heure
try:
    with open('/home/ubuntu/Python-Git-Linux-IF4/time_series.txt', 'r') as f:
        time_series = f.read().splitlines()
except FileNotFoundError:
    time_series = []



# Définir la fonction pour mettre à jour les anciennes valeurs d'heure
def update_time_series():

    # Exécuter le script Bash pour obtenir la date et l'heure actuelles
    output = subprocess.check_output(['bash', '/home/ubuntu/Python-Git-Linux-IF4/script.sh']).decode('utf-8').strip()
    # Ajouter la date et l'heure à la liste de temps
    time_series.append(output.split('\n')[1])
    with open('/home/ubuntu/Python-Git-Linux-IF4/time_series.txt', 'w') as f:
        for time in time_series:
            f.write(time + '\n')

def update_time():
    output = subprocess.check_output(['bash', '/home/ubuntu/Python-Git-Linux-IF4/script.sh']).decode('utf-8').strip()
    now_time=output.split('\n')[1]
    return now_time
def update_date():
    output = subprocess.check_output(['bash', '/home/ubuntu/Python-Git-Linux-IF4/script.sh']).decode('utf-8').strip()
    now_date=output.split('\n')[0]
    return now_date

app.layout = html.Div(children=[
    html.H1('Date et heure actuelles'),
    html.H3(id="date"),
    html.H3(id="time"),
    html.Div(id='time-series'),
    html.Div(id='daily-report'),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000,  # en millisecondes, une nouvelle valeur par minute
        n_intervals=0
    )
])


def update_graph():

    #Prendre les 5 dernières valeurs de la liste
    df = pd.read_csv('/home/ubuntu/Python-Git-Linux-IF4/time_series.txt', header=None,names=['time'],skiprows=max(0 , len(time_series)-5))
    new_time_series=df['time'].tolist()
    # Créer le graphique
    trace=go.Scatter(x=list(range(len(time_series))), y=new_time_series, mode='lines+markers')
    layout=go.Layout(title='Time series',xaxis=dict(title='x (can replace by anything)'),yaxis=dict(title='Value'))
    fig=go.Figure(data=[trace],layout=layout)
    
    # Retourner le graphique
    return html.Div([
        dcc.Graph(figure=fig)
    ])


#Mettre à jour le daily report
def update_daily_report():
    # Vérifier l'heure actuelle
    now = datetime.datetime.now().time()
    if datetime.time(20, 0) <= now <= datetime.time(20, 10):
        # Exécuter le script Bash pour obtenir le daily report
        daily_report = subprocess.check_output(['bash', '/home/ubuntu/Python-Git-Linux-IF4/scriptReport.sh']).decode('utf-8')
        # Stocker le daily report dans un fichier texte
        with open('/home/ubuntu/Python-Git-Linux-IF4/daily_report.txt', 'w') as fichier:
            fichier.write(daily_report)
    else:
        # Lire le contenu du fichier texte
        if os.path.isfile('/home/ubuntu/Python-Git-Linux-IF4/daily_report.txt'):
            with open('/home/ubuntu/Python-Git-Linux-IF4/daily_report.txt', 'r') as fichier:
                daily_report = fichier.read()
        else:
            daily_report = 'No daily report available.'
    # Extraire les informations du daily report
    date = daily_report.split('\n')[0].split(': ')[1]
    day = daily_report.split('\n')[1].split(': ')[1]
    month = daily_report.split('\n')[2].split(': ')[1]
    week = daily_report.split('\n')[3].split(': ')[1]
    dayyear = daily_report.split('\n')[4].split(': ')[1]
    # Retourner le daily report
    return html.Div([
        html.Div([
            html.H3('Daily Report'),
            html.P('Date: ' + date),
            html.P('Jour: ' + day),
            html.P('Mois: ' + month),
            html.P('Semaine: ' + week),
            html.P("Jour de l'année: " + dayyear)
        ])
    ])

# Définir la fonction pour afficher l'heure actuelle
@app.callback(
    dash.dependencies.Output('time', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_time_display(n):
    return update_time()

# Définir la fonction pour afficher la date
@app.callback(
    dash.dependencies.Output('date', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_date_display(n):
    return update_date()

# Définir la fonction pour afficher les anciennes valeurs d'heure
@app.callback(Output('time-series', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_output(n):
    return update_graph()

# Définir la fonction pour afficher le daily report
@app.callback(Output('daily-report', 'children'),
              [Input('interval-component', 'n_intervals')])
def update_report_display(n):
    return update_daily_report()


# Exécuter l'application Dash
if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=update_time_series, trigger='interval', minutes=1)
    scheduler.start()
    app.run_server(debug=True, port=80, host='0.0.0.0')

