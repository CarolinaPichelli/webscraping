import json  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

url = "https://www.smiles.com.br/home"

# Abrindo o navegador
browser = webdriver.Chrome()

# Acessando o site
browser.get(url)

# Tela cheia
browser.maximize_window()

# Selecionar um elemento
browser.find_element(By.ID, "drop_fligthType").click()
browser.find_element(By.ID, "opt_oneWay").click()
browser.find_element(By.ID, "inp_flightOrigin_1").click()
browser.find_element(By.ID, "opt_flight_2").click()
browser.find_element(By.ID, "inp_flightDestination_1").send_keys("MIA")

time.sleep(5)

# Iterando sobre as opções quando aparece MIA até achar Miami
items = browser.find_elements(By.CLASS_NAME, "list-group-item")
for item in items:
    if "Miami" in item.text:
        item.click()
        break

browser.find_element(By.ID, "startDateId").click()

days = browser.find_elements(By.CLASS_NAME, "CalendarDay")

today = str(datetime.today().day)

for day in days:
    if day.text == today and day.get_attribute('aria-disabled') == 'false':
        day.click()
        break

browser.find_element(By.ID, "btn_search").click()
time.sleep(3)
browser.find_element(By.ID, "btn_sameDayInternational").click()

# Começar a pegar as viagens
time.sleep(6)

# Coleta dos voos
allFlights = []  
qtdeFlights = 0

wait = WebDriverWait(browser, 15)

base_url = "https://www.smiles.com.br/mfe/emissao-passagem/?adults=1&cabin=ALL&children=0&departureDate={}&infants=0&isElegible=false&isFlexibleDateChecked=false&returnDate=&searchType=g3&segments=1&tripType=2&originAirport=GRU&originCity=&originCountry=&originAirportIsAny=false&destinationAirport=MIA&destinCity=&destinCountry=&destinAirportIsAny=false&novo-resultado-voos=true"

for i in range(10):
    proximoDia = datetime.now() + timedelta(days=i)
    timestamp_ms = int(proximoDia.timestamp() * 1000)
    url = base_url.format(timestamp_ms)
    print(f"\n[{proximoDia.strftime('%d/%m/%Y')}] ")

    browser.get(url)

    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "select-flight-not-found-card")))
        noflights = browser.find_element(By.CLASS_NAME, "select-flight-not-found-card")
        browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", noflights)
        print(f'Não tem voo no dia {i}')
    except:
        print("Mostrando voos: ")
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "header")))
        flights = browser.find_elements(By.CLASS_NAME, "header")
        time.sleep(5)

        try:
            btnMaisPassagens = WebDriverWait(browser, 5).until(
                EC.element_to_be_clickable((By.ID, "SelectFlightList-ida-more"))
            )
            btnMaisPassagens.click()
            print("Carregando todas as passagens do dia")
            time.sleep(1)
        except:
            print("Todas as passagens foram visualizadas")

        for flight in flights:
            try:
                browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", flight)
                time.sleep(1)

                info = flight.find_element(By.CLASS_NAME, "info")

                empresa = info.find_element(By.CSS_SELECTOR, "p.company-and-seat > span.company").text
                classe = info.find_element(By.CSS_SELECTOR, "p.company-and-seat > span.seat").text
                precoEl = flight.find_elements(By.CLASS_NAME, "miles")
                preco = precoEl[0].text if precoEl else "Não informado"

                horarios = info.find_elements(By.CLASS_NAME, "iata-code")
                hora_saida = horarios[0].text 
                hora_chegada = horarios[1].text 
                duracao = flight.find_element(By.CLASS_NAME, "scale-duration__time").text

                print(f'Empresa aérea: {empresa}')
                print(f'Classe: {classe}')
                print(f'Valor: {preco}')
                print(f'Duração: {duracao}')
                print(f'Horário de saída: {hora_saida}, Horário chegada: {hora_chegada}')
                qtdeFlights += 1

                allFlights.append({
                    "data_voo": proximoDia.strftime('%Y-%m-%d'),
                    "empresa": empresa,
                    "classe": classe,
                    "preco": preco,
                    "duracao": duracao,
                    "saida": hora_saida,
                    "chegada": hora_chegada
                })

            except:
                print("Erro ao coletar próxima passagem.")

with open("voos.json", "w", encoding="utf-8") as f:
    json.dump(allFlights, f, ensure_ascii=False, indent=2)

print(f"\nTotal de voos encontrados: {qtdeFlights}")
print("Dados salvos no arquivo voos.json.")

time.sleep(10)
browser.quit()
