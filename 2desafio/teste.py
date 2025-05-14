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

while True:
    try:
        # Se o elemento de "nenhum voo encontrado" estiver presente
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "select-flight-not-found-card")))
        noflights = browser.find_element(By.CLASS_NAME, "select-flight-not-found-card")
        browser.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", noflights)
        
        print("Não tem voo")

        base_url = "https://www.smiles.com.br/mfe/emissao-passagem/?adults=1&cabin=ALL&children=0&departureDate={}&infants=0&isElegible=false&isFlexibleDateChecked=false&returnDate=&searchType=g3&segments=1&tripType=2&originAirport=GRU&originCity=&originCountry=&originAirportIsAny=false&destinationAirport=MIA&destinCity=&destinCountry=&destinAirportIsAny=false&novo-resultado-voos=true"
        
        dia_futuro = datetime.now() + timedelta(days=1)
        timestamp_ms = int(dia_futuro.timestamp() * 1000)  # milissegundos
        url = base_url.format(timestamp_ms)
        browser.get(url)

    except Exception as e:
        # Caso não exista esse aviso, seguimos para buscar os voos
        print(f"Erro: {e}")
        
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "header")))
        flights = browser.find_elements(By.CLASS_NAME, "header")
        time.sleep(5)

        for flight in flights:
            try:
                # Centralizar na tela
                browser.execute_script(
                    "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", flight)
                time.sleep(1)

                info = flight.find_element(By.CLASS_NAME, "info")

                empresa = info.find_element(By.CSS_SELECTOR, "p.company-and-seat > span.company").text
                print("Empresa aérea:", empresa)
                allFlights.append(empresa)
                qtdeFlights += 1
                
            except:
                print("Falha ao obter dados de um voo.")
        break

# Finaliza o script
print(f"\nTotal de voos encontrados: {qtdeFlights}")

# Espera para permitir ver os resultados
time.sleep(10)

# Fechar o navegador
browser.quit()

# RESPOSTA DO CHAT ==================

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import time

# Inicialização
browser = webdriver.Chrome()
wait = WebDriverWait(browser, 15)
url = "https://www.smiles.com.br/home"
browser.get(url)
browser.maximize_window()

# Seleciona "Só ida"
wait.until(EC.element_to_be_clickable((By.ID, "drop_flightType"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "opt_oneWay"))).click()

# Origem: GRU (São Paulo)
wait.until(EC.element_to_be_clickable((By.ID, "inp_flightOrigin_1"))).click()
wait.until(EC.element_to_be_clickable((By.ID, "opt_flight_2"))).click()

# Destino: MIA (Miami)
dest_input = wait.until(EC.element_to_be_clickable((By.ID, "inp_flightDestination_1")))
dest_input.send_keys("MIA")
time.sleep(2)  # Espera sugestões aparecerem
items = browser.find_elements(By.CLASS_NAME, "list-group-item")
for item in items:
    if "Miami" in item.text:
        item.click()
        break

# Seleciona a data de hoje
wait.until(EC.element_to_be_clickable((By.ID, "startDateId"))).click()
days = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "CalendarDay")))
today = str(datetime.today().day)
for day in days:
    if day.text == today and day.get_attribute("aria-disabled") == "false":
        day.click()
        break

# Clica em buscar
wait.until(EC.element_to_be_clickable((By.ID, "btn_search"))).click()

# Lida com popup de aviso
try:
    wait.until(EC.element_to_be_clickable((By.ID, "btn_sameDayInternational"))).click()
except:
    pass  # O botão nem sempre aparece

# Coleta de voos para os próximos 5 dias
allFlights = []
qtdeFlights = 0
base_url = "https://www.smiles.com.br/mfe/emissao-passagem/?adults=1&cabin=ALL&children=0&departureDate={}&infants=0&isElegible=false&isFlexibleDateChecked=false&returnDate=&searchType=g3&segments=1&tripType=2&originAirport=GRU&originCity=&originCountry=&originAirportIsAny=false&destinationAirport=MIA&destinCity=&destinCountry=&destinAirportIsAny=false&novo-resultado-voos=true"

for i in range(5):  # Próximos 5 dias
    dia_futuro = datetime.now() + timedelta(days=i)
    timestamp_ms = int(dia_futuro.timestamp() * 1000)
    url_dia = base_url.format(timestamp_ms)
    browser.get(url_dia)

    time.sleep(5)

    # Verifica se há voos
    try:
        noflights = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "select-flight-not-found-card")))
        print(f"[{dia_futuro.strftime('%d/%m/%Y')}] Nenhum voo encontrado.")
        continue
    except:
        pass  # Significa que há voos

    # Coleta os voos
    try:
        wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "header")))
        flights = browser.find_elements(By.CLASS_NAME, "header")

        for flight in flights:
            try:
                browser.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", flight)
                time.sleep(1)
                info = flight.find_element(By.CLASS_NAME, "info")
                empresa = info.find_element(By.CSS_SELECTOR, "p.company-and-seat span.company").text
                print(f"[{dia_futuro.strftime('%d/%m/%Y')}] Empresa aérea: {empresa}")
                allFlights.append((dia_futuro.strftime('%Y-%m-%d'), empresa))
                qtdeFlights += 1
            except:
                print(f"[{dia_futuro.strftime('%d/%m/%Y')}] Falha ao obter dados de um voo.")
    except:
        print(f"[{dia_futuro.strftime('%d/%m/%Y')}] Erro ao carregar os voos.")

print(f"\n✅ Total de voos encontrados: {qtdeFlights}")
time.sleep(10)
browser.quit()
