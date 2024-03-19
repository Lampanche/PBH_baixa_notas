import PySimpleGUI as sg
from ex2 import *
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
import sys
import os
import logging

os.environ['WDM_PROGRESS_BAR'] = str(0)
#local_bundle_exe = sys._MEIPASS

def format_return_date(date):
    list_itens_date = []
    str_date = ''
    zero = '0'

    for itens_date in date:
        array_format = []

        if(len(str(itens_date)) == 1):
            array_format.append(zero)
            array_format.append(str(itens_date))
            str_array_format = ''.join(array_format)
            list_itens_date.append(str_array_format)

        elif(len(str(itens_date)) > 1):
            list_itens_date.append(str(itens_date))
   
    month = list_itens_date[0]
    day = list_itens_date[1]
    list_itens_date[0] = day
    list_itens_date[1] = month

    str_date = ''.join(list_itens_date)
    return str_date

dic_entries_pbh = {
    "cnpj": "",
    "password": "",
    "type_notes": "",
    "data_inicial": "",
    "data_final": "",
    "diretorio": r""
    }

layout = [
    [sg.Text("Informe os dados da empresa que deseja baixar as notas.", text_color= '#DA70D6')],
    [sg.Text("CNPJ* Só Números", text_color= '#DA70D6'), sg.Input(key='-CNPJ-', size=(14,1)), sg.Text("Senha PBH", text_color= '#DA70D6'), sg.Input(key='-PASSWORD-', size=(15,1))],
    [sg.Checkbox("Prestador", key='prestador', enable_events= True), sg.Checkbox("Tomador", key='tomador', enable_events= True)],
    [sg.Text("Informe o período", text_color= '#DA70D6')],
    [sg.Button("Data inicial"), sg.Button("Data final")],
    [sg.Text("Insira o caminho da pasta", text_color= '#DA70D6')],
    [sg.Input(key='diretorio')],
    [sg.Button("Baixar")],
    [sg.Text('Status:') ,sg.Text(key='status', text_color='#00FF00')]
]
                     

janela = sg.Window(
    "PBH - Baixa nota",
    layout=layout
)

while True:

    event, value = janela.read()

    if event == sg.WIN_CLOSED:
        break

   
    dic_entries_pbh["cnpj"] = value['-CNPJ-']
    dic_entries_pbh["password"] = value['-PASSWORD-']

    print(value['prestador'])
    print(value['tomador'])

    if(value['prestador'] == True):
        dic_entries_pbh['type_notes'] = 'Prestador'

    if(value['tomador'] == True):
        dic_entries_pbh["type_notes"] = 'Tomador'

    if event == 'Data inicial':
        date = sg.popup_get_date()
        str_date = format_return_date(date)
        dic_entries_pbh["data_inicial"] = str_date
    elif event == 'Data final':
        date = sg.popup_get_date()
        str_date = format_return_date(date)
        dic_entries_pbh["data_final"] = str_date 
        janela['status'].update('')        

    dic_entries_pbh["diretorio"] = value['diretorio']

    print(dic_entries_pbh)

    if event == 'Baixar':

        service = Service(GeckoDriverManager(path=f'').install())
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        options.set_preference("browser.download.folderList", 2)
        options.set_preference("browser.download.manager.showWhenStarting", False)
        options.set_preference("browser.download.dir", dic_entries_pbh["diretorio"])
        options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/xml")

        navegador = webdriver.Firefox( service=service,options=options)

        actions = ActionChains(navegador)
        wdw = WebDriverWait(navegador, timeout=4)

        run_to_pbh(navegador)
        sleep(1)

        login_pbh(navegador,dic_entries_pbh["cnpj"], dic_entries_pbh["password"], wdw)
        sleep(2)

        hover_to_search_nfse(navegador, actions)
        sleep(2)

        search_advanced(navegador,wdw)
        sleep(2)

        status_baixa_notas = search_provider_or_taker(navegador,dic_entries_pbh["type_notes"], dic_entries_pbh["data_inicial"], dic_entries_pbh["data_final"], dic_entries_pbh["diretorio"], wdw)
        janela['status'].update(status_baixa_notas)



janela.close()