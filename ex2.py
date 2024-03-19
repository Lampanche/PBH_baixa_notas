from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
from base64 import b64decode
from selenium.common.exceptions import TimeoutException


def wait_element_clikable(loc, wdw):

    wdw.until(EC.element_to_be_clickable(loc))

def wait_element(loc, wdw):
    return wdw.until(EC.presence_of_element_located(locator=loc))

def wait_element_loading(loc, wdw, callback):
    div_loading = ""
    
    try:
        div_loading = wdw.until(EC.visibility_of_element_located(locator=loc))
    except TimeoutException:
        div_loading = False
        return div_loading

    if(div_loading):
        callback(loc, wdw, callback)
    
    
def run_to_pbh(navegador):

    navegador.get("https://bhissdigital.pbh.gov.br/nfse/")

    navegador.maximize_window()

    form = navegador.find_element(By.ID, "form")

    linkOuth = form.find_element(By.TAG_NAME, "a")

    linkOuth.click()

def login_pbh(navegador,cnpj, password,wdw):

    wait_element((By.ID, "username"),wdw)

    inputUser = navegador.find_element("id", "username")
    inputUser.send_keys(cnpj)

    wait_element((By.ID, "password"), wdw)

    inputPassword = navegador.find_element("id", "password")
    inputPassword.send_keys(password)

    btnLogin = navegador.find_element(By.CSS_SELECTOR, ".default-btn")
    btnLogin.click()

def hover_to_search_nfse(navegador, actions):

    navegador.execute_script("javascript:window.document.getElementById('menu:bt_consulta_nfse_prestador').click();")

    """
    nav = navegador.find_element(By.XPATH, "//*[@id='nav']")

    listItensMenu = nav.find_elements(By.CLASS_NAME, "itemMenu")

    for div in listItensMenu:

        onmouseout = div.get_dom_attribute("onmouseout")

        if(onmouseout == "out(1);MM_swapImgRestore()"): 
            actions.move_to_element(div).perform()
            sleep(1)
            s1 = div.find_element(By.ID, "s1")
            listLinks = s1.find_elements(By.TAG_NAME,"a")
            for a in listLinks:
                href = a.get_dom_attribute("href")
                if(href == "javascript:window.document.getElementById('menu:bt_consulta_nfse_prestador').click();"):
                    a.click()
                    sleep(1)
                    break    
                else:
                    continue
            break    
        else:
            continue
    """

        
def search_advanced(navegador, wdw):

    divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

    if(not divLoading):

        navegador.execute_script("javascript:controlaAbasConsultaNfse('aba2');")

    #btn = navegador.find_element(By.ID, "topo_aba2")

    #linkBtn = btn.find_element(By.TAG_NAME, "a")

    #linkBtn.click()

#
def logout(navegador):
    div_id =  navegador.find_element(By.ID, "identificacao")
    link_logout = div_id.find_element(By.TAG_NAME, "a")
    link_logout.click()    

def nothing_record(navegador):

    verify_alert_nothing_record = navegador.find_elements(By.XPATH, "/html/body/div/div[1]/span[2]/span/div/div")

    if(verify_alert_nothing_record):
        alert_exist = navegador.find_element(By.XPATH, "/html/body/div/div[1]/span[2]/span/div/div")
        li = alert_exist.find_element(By.TAG_NAME, "li")
        msg_alert = li.text
        logout(navegador)
        sleep(1)
        navegador.quit()
        return msg_alert

def format_string_values_tax(str_value_no_format):

    index_str_slice = len(str_value_no_format) + 1
    str_format = str_value_no_format[3:index_str_slice]
    str_format_replace_1 = str_format.replace(".", "")
    str_format_replace_2 = str_format_replace_1.replace(",", ".")
    value_tax = float(str_format_replace_2)

    return value_tax
#

def verify_nfse_canceled(navegador):
    div_nfse_cancelada = navegador.find_elements(By.ID, "cancelada")
    return bool(div_nfse_cancelada)

def verify_iss_ret_and_creat_str(navegador):

    #Pega valor do iss     
    table_values = navegador.find_element(By.CLASS_NAME, "tableValores")
    tr_table_values = table_values.find_elements(By.TAG_NAME, "tr")
    tr_iss_ret = tr_table_values[2]
    list_td_iss_ret = tr_iss_ret.find_elements(By.TAG_NAME, "td")
    value_iss_ret = list_td_iss_ret[1].text

    #Formatando a string recebida => ISS RET
    value_iss = format_string_values_tax(value_iss_ret)

    #Pega o Nome do municipio
    div_04 = navegador.find_elements(By.CLASS_NAME, "box04")
    div_municipio = div_04[-1]
    tds_div_municipio = div_municipio.find_elements(By.TAG_NAME, "td")
    td_municipio = tds_div_municipio[0]
    list_p_td = td_municipio.find_elements(By.TAG_NAME, "p")
    p_municipio = list_p_td[1]
    municipio = p_municipio.text    

    #Formatando municipio
    index_Municipio = len(municipio) + 1
    str_municipio = municipio[10:index_Municipio]

    if(value_iss > 0):
        str_iss_ret = f". ISS RET {str_municipio} "
        return str_iss_ret 

def verify_value_ret_fed_and_creat_str(navegador):

    #Pega o valor do imposto federal retido
    table_values = navegador.find_element(By.CLASS_NAME, "tableValores")
    tr_table_values = table_values.find_elements(By.TAG_NAME, "tr")
    tr_fed_ret = tr_table_values[1]
    list_td_fed_ret = tr_fed_ret.find_elements(By.TAG_NAME, "td")
    value_fed_ret = list_td_fed_ret[1].text

    #Formatando a string recebida => RET FED    
    value_fed = format_string_values_tax(value_fed_ret)

    verify_exists_Cofins = navegador.find_elements(By.XPATH, "//*[@id='form:j_id167']")
    
    if(value_fed > 0 and verify_exists_Cofins):

        #Pega valor do COFINS
        content_cofins = navegador.find_element(By.ID, "form:j_id167")
        list_span_cofins = content_cofins.find_elements(By.TAG_NAME, "span")
        span_value_cofins = list_span_cofins[1]
        value_text_cofins = span_value_cofins.text
        
        #Formata a string recebida => COFINS
        value_cofins = format_string_values_tax(value_text_cofins)   

        if(value_cofins > 0):
            str_ret_fed = ". RET FED"
            return str_ret_fed

def verify_value_inss_and_creat_str(navegador):
    
    #Pega o valor do imposto federal retido
    table_values = navegador.find_element(By.CLASS_NAME, "tableValores")
    tr_table_values = table_values.find_elements(By.TAG_NAME, "tr")
    tr_fed_ret = tr_table_values[1]
    list_td_fed_ret = tr_fed_ret.find_elements(By.TAG_NAME, "td")
    value_fed_ret = list_td_fed_ret[1].text

    #Formatando a string recebida => RET FED    
    value_fed = format_string_values_tax(value_fed_ret)

    verify_exists_inss = navegador.find_elements(By.XPATH, "//*[@id='form:j_id176']")      

    if(value_fed > 0 and verify_exists_inss):

        #Pega o valor do INSS
        content_inss = navegador.find_element(By.ID, "form:j_id176")
        list_span_inss = content_inss.find_elements(By.TAG_NAME, "span")
        span_value_inss = list_span_inss[1]
        value_text_inss = span_value_inss.text
        
        #Formatando a string recebida => INSS
        value_inss = format_string_values_tax(value_text_inss)   

        if(value_inss > 0):
            str_ret_inss = ". RET INSS"
            return str_ret_inss


def search_nfse_period(navegador, date_start, date_end):

    input_period_start = navegador.find_element(By.ID, "form:dtCompetenciaInicial")
    input_period_start.click() #Temos que clicar antes, se não o sendKeys não envia o texto para o elemento.
    input_period_start.send_keys(date_start)
    input_period_start.send_keys(Keys.TAB)
    sleep(1)
    input_period_end = navegador.find_element(By.ID, "form:dtCompetenciaFinal")
    input_period_end.send_keys(date_end)
    input_period_end.send_keys(Keys.TAB)

    search_nfse = navegador.find_element(By.ID, "form:bt_procurar_NFS-e")
    search_nfse.click()
    sleep(1)

#
def click_links_page_initial_taker(navegador,dic, wdw):

    tbody = navegador.find_element(By.ID, "form:j_id166:listaNotas:tb")

    listTrsTbodyPage = tbody.find_elements(By.TAG_NAME, "tr")

    size_list_trs = len(listTrsTbodyPage) - 1

    i = 0

    while i <= size_list_trs:
        
        divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

        if(not divLoading):

            tbody_interator = navegador.find_element(By.ID, "form:j_id166:listaNotas:tb")
            list_tr_interator = tbody_interator.find_elements(By.TAG_NAME, "tr")
            list_td = list_tr_interator[i].find_elements(By.TAG_NAME, "td")
            td = list_td[1]
            link_nfse = td.find_element(By.TAG_NAME, "a")
            link_nfse.click()
            divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

        if(not divLoading):    

            wait_element((By.ID, "moldura"), wdw)
            nfse_c = verify_nfse_canceled(navegador)
            # Pegando o numero da nota e formata
            el_n_fse = navegador.find_element(By.CLASS_NAME, "numeroDestaque")
            numberNfse = el_n_fse.text
            index_number_nfse = len(numberNfse) + 1
            number_nfse_format = numberNfse[8:index_number_nfse]
            #
            el_provider = navegador.find_element(By.CLASS_NAME, "hh3")
            provider = el_provider.text
            provider_format = provider[0:31]
            provider_format_1 = provider_format.replace("/", "")
            provider_format_2 = provider_format_1.replace(":", "")
            #

            pdf = b64decode(navegador.print_page())

            if(nfse_c):

                with open (f"{dic}/{number_nfse_format} NFS-e CANCELADA - {provider_format_2}.pdf", "wb") as f:
                    f.write(pdf)
                    f.close()
                    #xml = navegador.find_element(By.XPATH, "/html/body/div/form/input[2]")
                    #xml.click()
                    sleep(1)
                    #returnPageLinks = navegador.find_element(By.XPATH, "//*[@id='form:j_id10']")
                    #returnPageLinks.click()
                    navegador.execute_script("window.location='javascript:history.go(-1)';A4J.AJAX.Submit('_viewRoot','form',event,{'similarityGroupingId':'form:j_id10','parameters':{'form:j_id10':'form:j_id10'} ,'actionUrl':'/nfse/pages/exibicaoNFS-e.jsf'} );return false;")
                    #wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
                    sleep(2)
                    navegador.execute_script("javascript:controlaAbasConsultaNfse('aba2');")
                    sleep(1)
            else:
                iss_ret = verify_iss_ret_and_creat_str(navegador) or ""
                ret_fed = verify_value_ret_fed_and_creat_str(navegador) or ""
                ret_inss = verify_value_inss_and_creat_str(navegador) or ""
                with open (f"{dic}/{number_nfse_format} NFS-e {provider_format_2}{iss_ret}{ret_fed}{ret_inss}.pdf", "wb") as f:
                    f.write(pdf)
                    f.close()
                    xml = navegador.find_element(By.XPATH, "/html/body/div/form/input[2]")
                    xml.click()
                    sleep(1)
                    #returnPageLinks = navegador.find_element(By.XPATH, "//*[@id='form:j_id10']")
                    #returnPageLinks.click()
                    navegador.execute_script("window.location='javascript:history.go(-1)';A4J.AJAX.Submit('_viewRoot','form',event,{'similarityGroupingId':'form:j_id10','parameters':{'form:j_id10':'form:j_id10'} ,'actionUrl':'/nfse/pages/exibicaoNFS-e.jsf'} );return false;")
                    #wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
                    sleep(2)
                    navegador.execute_script("javascript:controlaAbasConsultaNfse('aba2');")
                    sleep(1)
        i += 1

def click_btn_next_and_save_nfse_taker(navegador, dic, wdw):
    
    contentBtnsNext = navegador.find_element(By.ID, "form:j_id166:dtRick")
    allTds = contentBtnsNext.find_elements(By.TAG_NAME, "td")

    size_list_alltds = len(allTds) - 1

    list_pages = []

    t = 0 

    while t <= size_list_alltds:
        contentBtnsNext_interator = navegador.find_element(By.ID, "form:j_id166:dtRick")
        allTds_interator = contentBtnsNext_interator.find_elements(By.TAG_NAME, "td")
        value_text =  allTds_interator[t].text
        if(value_text):
            list_pages.append(allTds_interator[t])
        t += 1

    clicksBtnsNext = len(list_pages) - 2

    n = 0

    while n <= clicksBtnsNext:
        contentBtnsNext_interator_2 = navegador.find_element(By.ID, "form:j_id166:dtRick")
        allTds_interator_2 = contentBtnsNext_interator_2.find_elements(By.TAG_NAME, "td")
        tdBtnNext = allTds_interator_2[-2]
        tdBtnNext.click()
        wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
        click_links_page_initial_taker(navegador,dic, wdw)
        n += 1
    logout(navegador)
    navegador.quit()

def click_links_page_initial_provider(navegador, dic, wdw):

    tbody = navegador.find_element(By.ID, "form:j_id166:listaNotas:tb")

    listTrsTbodyPage = tbody.find_elements(By.TAG_NAME, "tr")

    size_list_trs = len(listTrsTbodyPage) - 1

    i = 0

    while i <= size_list_trs:

        divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

        if(not divLoading):

            tbody_interator = navegador.find_element(By.ID, "form:j_id166:listaNotas:tb")
            list_tr_interator = tbody_interator.find_elements(By.TAG_NAME, "tr")
            list_td = list_tr_interator[i].find_elements(By.TAG_NAME, "td")
            td = list_td[1]
            link_nfse = td.find_element(By.TAG_NAME, "a")
            link_nfse.click()
            divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

            if(not divLoading):    
                wait_element((By.ID, "moldura"), wdw)
                nfse_c = verify_nfse_canceled(navegador)
                # Pegando o numero da nota e formatando
                el_n_fse = navegador.find_element(By.CLASS_NAME, "numeroDestaque")
                numberNfse = el_n_fse.text
                index_number_nfse = len(numberNfse) + 1
                number_nfse_format = numberNfse[8:index_number_nfse]
                #
                list_spans = navegador.find_elements(By.CLASS_NAME, "cnpjPrincipal")
                span_taker = list_spans[-1]
                taker = span_taker.text
                taker_format = taker[0:31]
                taker_format_1 = taker_format.replace("/", "")
                taker_format_2 = taker_format_1.replace(":", "")      
                #

                pdf = b64decode(navegador.print_page())

                if(nfse_c):

                    with open (f"{dic}/{number_nfse_format} NFS-e CANCELADA - {taker_format_2}.pdf", "wb") as f:
                        f.write(pdf)
                        f.close()
                        xml = navegador.find_element(By.XPATH, "/html/body/div/form/input[2]")
                        xml.click()
                        sleep(1)
                        #returnPageLinks = navegador.find_element(By.XPATH, "//*[@id='form:j_id10']")
                        #returnPageLinks.click()
                        navegador.execute_script("window.location='javascript:history.go(-1)';A4J.AJAX.Submit('_viewRoot','form',event,{'similarityGroupingId':'form:j_id10','parameters':{'form:j_id10':'form:j_id10'} ,'actionUrl':'/nfse/pages/exibicaoNFS-e.jsf'} );return false;")
                        #wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
                        sleep(2)
                        navegador.execute_script("javascript:controlaAbasConsultaNfse('aba2');")
                        sleep(1)
                else:
                    iss_ret = verify_iss_ret_and_creat_str(navegador) or ""
                    ret_fed = verify_value_ret_fed_and_creat_str(navegador) or ""
                    ret_inss = verify_value_inss_and_creat_str(navegador) or ""
                    with open (f"{dic}/{number_nfse_format} NFS-e {taker_format_2}{iss_ret}{ret_fed}{ret_inss}.pdf", "wb") as f:
                        f.write(pdf)
                        f.close()
                        xml = navegador.find_element(By.XPATH, "/html/body/div/form/input[2]")
                        xml.click()
                        sleep(1)
                        #returnPageLinks = navegador.find_element(By.XPATH, "//*[@id='form:j_id10']")
                        #returnPageLinks.click()
                        navegador.execute_script("window.location='javascript:history.go(-1)';A4J.AJAX.Submit('_viewRoot','form',event,{'similarityGroupingId':'form:j_id10','parameters':{'form:j_id10':'form:j_id10'} ,'actionUrl':'/nfse/pages/exibicaoNFS-e.jsf'} );return false;")
                        #wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
                        sleep(2)
                        navegador.execute_script("javascript:controlaAbasConsultaNfse('aba2');")
                        sleep(1)
        i += 1

def click_btn_next_and_save_nfse_provider(navegador, dic, wdw):
    
    contentBtnsNext = navegador.find_element(By.ID, "form:j_id166:dtRick")
    allTds = contentBtnsNext.find_elements(By.TAG_NAME, "td")

    size_list_alltds = len(allTds) - 1

    list_pages = []

    t = 0 

    while t <= size_list_alltds:
        contentBtnsNext_interator = navegador.find_element(By.ID, "form:j_id166:dtRick")
        allTds_interator = contentBtnsNext_interator.find_elements(By.TAG_NAME, "td")
        value_text =  allTds_interator[t].text
        if(value_text):
            list_pages.append(allTds_interator[t])
        t += 1

    clicksBtnsNext = len(list_pages) - 2

    n = 0

    while n <= clicksBtnsNext:
        contentBtnsNext_interator_2 = navegador.find_element(By.ID, "form:j_id166:dtRick")
        allTds_interator_2 = contentBtnsNext_interator_2.find_elements(By.TAG_NAME, "td")
        tdBtnNext = allTds_interator_2[-2]
        tdBtnNext.click()
        wait_element((By.ID, "form:j_id166:listaNotas"), wdw)
        click_links_page_initial_provider(navegador,dic, wdw)
        n += 1
    logout(navegador)
    navegador.quit()
#

def search_provider_or_taker(navegador,type_search, date_start, date_end, dic, wdw):
    status = ''
    if(type_search == "Tomador"):
        wait_element((By.ID, "form:perfil:1"),wdw)
        select_tomador = navegador.find_element(By.ID, "form:perfil:1")
        select_tomador.click()
        divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

        if(not divLoading):

            search_nfse_period(navegador,date_start, date_end)
            sleep(1)
            msg_sem_nota = nothing_record(navegador)
            if(msg_sem_nota):
                return msg_sem_nota
            sleep(1)
            click_links_page_initial_taker(navegador,dic, wdw)
            sleep(1)
            click_btn_next_and_save_nfse_taker(navegador,dic, wdw)
            status = 'Terminei de baixar as notas de tomador'
            return status
        
    elif(type_search == "Prestador"):
        wait_element((By.ID, "form:perfil:0"), wdw)
        select_prestador = navegador.find_element(By.ID, "form:perfil:0")
        select_prestador.click()
        divLoading = wait_element_loading((By.ID, "ajaxLoadingModalBoxDiv"), wdw, callback = wait_element_loading)

        if(not divLoading):

            search_nfse_period(navegador,date_start, date_end)
            sleep(2)
            msg_sem_nota = nothing_record(navegador)
            if(msg_sem_nota):
                return msg_sem_nota
            click_links_page_initial_provider(navegador, dic, wdw)
            sleep(1)
            click_btn_next_and_save_nfse_provider(navegador,dic, wdw)
            status = 'Terminei de baixar as notas de prestador'
            return status





