from flask import Flask
from flask import Flask, request, redirect
from flask import Flask, render_template_string
import pygsheets
import json
import datetime

app = Flask(__name__)

"""
git bash:
git remote add origin https://github.com/pedroccpimenta/RestUPubPriv.git

""" 

import socket
hostname=socket.gethostname()
print ("hostname:", hostname)

if (hostname=="DESKTOP-O5TUSN4" or hostname=='TP16G2-PCP') :
    servfile='./secrets/pcp-prof-0ca0856baee5.json'
    othu='https://restupubpriv.onrender.com/'

else:
    servfile='/etc/secrets/pcp-prof-0ca0856baee5.json'
    othu='http://127.0.0.1/5000'

with open(servfile, 'r') as fh:
    LOGIN_KEYWORD = json.loads(fh.read())['private_key']


titleico="<title>Landing page - Restaurantes</title><link rel='icon' type='image/png' href='./pics/Gemini_Generated_Image_7bex9w7bex9w7bex.png'>"
bodyfont='<body style="font-family: Roboto, sans-serif;">'

disclaimer="<table border=1 bgcolor=orange style='width:100%' cellspacing=0><tr><td>Os dados apresentados são fictícios e utilizados em contexto de ensino. Qualquer semelhança com a realidade é acidental e desprovida de intencionalidade.</table>"

desc={
    'landing':f'<h1>Críticas a restaurantes</h1>{disclaimer}<br>A tabela seguinte mostra os dados públicos deste caso de estudo - Nomes, moradas e localização (Lat, Lng) de restaurantes:<br>',
    'page1':f'<h1>Críticas a restaurantes</h1>{disclaimer}<br>A tabela seguinte mostra alguns dados dos restaurantes com as críticas recebidas:<br>',
}

agora = str(datetime.datetime.now())[0:19]
bottomline = f"<hr color=green><small><i>{agora} <i>(ppimenta [at] umaia [dot] pt)</i> | check at (<a href='{othu}' target='*'>{othu}</a>.)"

gc = pygsheets.authorize(service_file=servfile)
keyword=""


@app.route("/", methods=["GET", "POST"])
def page0():
    global keyword

    sh = gc.open('Críticas-Restaurantes')
    wks = sh.worksheet_by_title('Restaurante')
    #rea = wks.get_as_df('Restaurante')

    dados = wks.get_all_values(include_tailing_empty=False )
    colunas = dados[0]  # cabeçalhos
    print(colunas)
    linhas = dados[1:]  # linhas de dados

    tabela = '<table border="1"><tr>'
    for c in dados[0]: 
        tabela += f'<th>{c}</th>'
    tabela += '</tr>'

    print('linhas:', linhas)
    print('linhas:', linhas[0])
    print('linhas[0][1]:', linhas[0][1])
    print('len(linhas):', len(linhas))

    nl=0
    while len(linhas[nl])>0:
        tabela += '<tr>'
        for celula in linhas[nl]:
            tabela += f'<td>{celula}</td>'
        tabela += '</tr>'
        nl=nl+1

    tabela += '</table>'
    print(tabela)

    if request.method == "POST":

        keyword = request.form.get("keyword", "").strip().lower()
        if keyword == "pag1":
            return redirect("/page1")
        elif keyword == "pag2":
            return redirect("/page2")
        else:
            return f'''
                <!doctype html>{titleico}
                <title>Landing page - Restaurantes</title>
                {bodyfont}{desc['landing']}<center>{tabela}</center>
                <center>
                Para exemplo de como mapear estes dados, veja este <a href='https://colab.research.google.com/drive/1dKWR_aafquIL6_noIBheAl63O5e-RrIk' target='*'>Jupyter notebook</a>.
                </center>

                <form method="post">
                <input name="keyword" type="password" placeholder="Enter keyword">
                <input type="submit">
                </form>
                <p style='color:red'><b>{keyword}</b> - Unknown keyword</p>
                {bottomline}</body>
                </html>
    '''
    return f'''
        <!doctype html>{titleico}
        {bodyfont}{desc['landing']}<center>{tabela}</center>
        <center>
        Para exemplo de como mapear estes dados, veja este <a href='https://colab.research.google.com/drive/1dKWR_aafquIL6_noIBheAl63O5e-RrIk' target='*'>Jupyter notebook</a>.
        </center>

        <form method="post">
        <input name="keyword" type="password" placeholder="Enter keyword">
        <input type="submit">
        </form>
        {bottomline}</body>
        </html>
    '''

"""
    return render_template_string('''
        <h2>Dados da Planilha</h2>
        {{ tabela|safe }}
    ''', tabela=tabela)
"""



@app.route("/page1")
def pag1():
    global keyword
    if keyword!='pag1':
        return redirect("/")

    sh = gc.open('Críticas-Restaurantes')
    wrestaurante = sh.worksheet_by_title('Restaurante')
    restaurante = wrestaurante.get_all_values(include_tailing_empty=False )

    pcritica = sh.worksheet_by_title("Crítica").get_all_values(include_tailing_empty=False)
    critica=pcritica[1:]

    colunas = restaurante[0]  # cabeçalhos
    linhas = restaurante[1:]  # linhas de dados

    tabela = '<table border="1"><tr>'
    for c in colunas[0:4]: 
        tabela += f'<th>{c}</th>'
    tabela += f'<th>Críticas</th>'

    tabela += '</tr>'

    nl=0
    while len(linhas[nl])>0:
        tabela += '<tr>'
        for celula in linhas[nl][0:4]:
            tabela += f'<td>{celula}</td>'
            nlc=0
      
        tots =0
        ncs = 0
       
        lc = "<ul style='margin-top:0px;'>"
        print ("critica[nlc]:", critica[nlc])
        while len (critica[nlc])>0:
            if critica[nlc][0] == linhas[nl][0]:
                lc += f"<li>{critica[nlc][2]} ({critica[nlc][3]}⭐) {critica[nlc][4]}"
                tots+=int(critica[nlc][3])
                ncs+=1
            nlc=nlc+1
        lc +="</ul>"

        if ncs==0:
            tabela += "<td> (sem críticas) "
        else:
            tabela += f"<td>{lc}média das críticas:{tots/ncs:.1f}<small> ⭐</small></td>"


        tabela += '</tr>'
        nl=nl+1

    tabela += '</table>'
    print(tabela)    

    return f'''
        <!doctype html>{titleico}
        {bodyfont}{desc['page1']}<center>{tabela}</center><hr color=green>
        <a href=".">Landing page</a>
        {bottomline}</body>
        </html>
    '''

@app.route("/page2")
def page2():
    return f'''
        <!doctype html>{titleico}
        {bodyfont}
        <a href=".">Landing page</a>
        {bottomline}</body>
        </html>
    '''



if __name__ == "__main__":
    #app.run(port=5353, debug=True)
    app.run()
