import threading
import logging
import time
import random
from selenium.webdriver.common.by import By
from seleniumwire import webdriver as sw_webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.parse


logging.basicConfig(filename='script_temp.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', encoding='utf-8')

def get_visit_time(min_time, max_time):
    visit_time = random.uniform(min_time, max_time)
    print(f"Сгенерированное время пребывания на сайте: {visit_time} секунд")
    return visit_time

def get_proxy():
    with open("C:/Users/Admin/Desktop/proxy.txt", "r") as file:
        proxies = file.readlines()
    proxy = random.choice(proxies).strip()
    return proxy

def visit_site(driver, visit_time, stop_flag):
    global start_time
    start_time = time.time()
    logging.info(f"Начало посещения сайта. Время пребывания: {visit_time} секунд")
    while time.time() - start_time < visit_time and not stop_flag.is_set():
        time.sleep(1)
    logging.info("Время пребывания на сайте истекло. Завершение текущего выполнения.")
    print("Время пребывания на сайте истекло")
    stop_flag.set()

def scroll_page(driver, stop_flag):
    for _ in range(1000):
        if stop_flag.is_set():
            break
        scroll_direction = random.choice(["up", "down"])
        if scroll_direction == "up":
            driver.execute_script("window.scrollBy(0, -500);")
        else:
            driver.execute_script("window.scrollBy(0, 500);")
        time.sleep(random.uniform(1, 3))

def find_element_with_navigation(search_queries_file, domain, search_engine, repetitions,
                                 min_interval, max_interval, min_visit_time, max_visit_time):
    for _ in range(repetitions):
        with open(search_queries_file, 'r', encoding='utf-8') as file:
            search_queries = file.readlines()

        for _ in range(repetitions):
            search_query = random.choice(search_queries).strip()
            ### в выдаче страница на первом месте
            # base_word =  domain.split('//')[1][:-1]
            # search_query_ = f'Минск "{base_word}" ' #+ last_page

            proxy = get_proxy()
            proxy_options = {
                'proxy': {
                    'http': f'http://{proxy}',
                    'https': f'https://{proxy}',
                    'no_proxy': 'localhost,127.0.0.1'
                }
            }

            if search_engine.lower() == "1":
                # путь к драйверу для Yandex.
                driver = sw_webdriver.Chrome(seleniumwire_options=proxy_options)
                base_url = "https://yandex.ru/search/?text="
            elif search_engine.lower() == "2":
                # путь к драйверу для Google.
                driver = sw_webdriver.Chrome(seleniumwire_options=proxy_options)
                base_url = "https://www.google.com/search?q="
            else:
                logging.error("Некорректная поисковая система")
                return

            page = 1
            found = False

            try:
                while not found:
                    driver.get(f'{base_url}{search_query}&start={page}')
                    try:
                        link = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, domain)))
                        link.click()
                        found = True
                    except:
                        if page > 30:
                            logging.warning(f"Домен {domain} не найден")
                            break
                        else:
                            page += 10  # Увеличиваем номер страницы на 10

                # Получаем ссылки из файла
                with open("C:/Users/Admin/Desktop/site_link.txt", "r", encoding='utf-8') as file:
                    logging.info("Ссылки из файла")
                    site_links = file.readlines()
                    print("Ссылки из файла site_link.txt:")

                    # Перебираем ссылки из файла и сравниваем с найденными ссылками на сайте
                    for site_link in site_links:
                        site_link = site_link.strip()

                        # Находим все элементы ссылок на странице
                        links = driver.find_elements(By.TAG_NAME, 'a')

                        # Получаем все атрибуты href ссылок на странице
                        page_links = [urllib.parse.unquote(link.get_attribute('href')) for link in links if
                                      link.get_attribute('href')]
                        logging.info(f"Ссылки на странице {page_links}")

                        # Словарь для хранения соответствия текста ссылки и её href
                        link_texts = {}

                        # Перебираем все найденные ссылки на странице
                        for page_link in page_links:
                            # Находим элемент ссылки на странице по атрибуту href
                            try:
                                link_element = driver.find_element(By.XPATH, f"//a[@href='{page_link}']")
                                link_text = link_element.text
                                # if link_text:
                                link_texts[page_link] = link_text.lower()
                            except Exception as e:
                                logging.error(f"Не удалось найти текст для ссылки {page_link}: {str(e)}")

                        link_found = False  # Переменная для отслеживания найденной ссылки

                        for page_link, link_text in link_texts.items():
                            if site_link == page_link:
                                logging.info(f"Найдена внутренняя ссылка: {site_link} с текстом: {link_text}")
                                print(f"Найдена внутренняя ссылка: {site_link} с текстом: {link_text}")

                                time.sleep(3)  # Делаем паузу между кликами по ссылкам

                                # Находим элемент ссылки на странице по тексту ссылки
                                try:
                                    # Ожидаем, пока элемент не станет кликабельным
                                    if link_text:
                                        try:
                                            link_element = WebDriverWait(driver, 5).until(
                                            EC.element_to_be_clickable((By.XPATH, f"//a[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ0123456789', 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789'), '{link_text.lower()}')]")))
                                        except:
                                            continue
                                    else:
                                        try:
                                            link_element = WebDriverWait(driver, 5).until(
                                                EC.element_to_be_clickable((By.XPATH, f"//a[@href='{site_link}']")))
                                        except:
                                            continue
                                    # Прокрутка страницы до элемента
                                    actions = ActionChains(driver)
                                    actions.move_to_element(link_element).perform()
                                    # Использование JavaScript для клика, если обычный клик не работает
                                    try:
                                        # Кликаем на найденную ссылку
                                        link_element.click()
                                        logging.info("Клик на ссылку")
                                    except Exception as e:
                                        try:
                                            driver.execute_script("arguments[0].click();", link_element)# Прокрутка страницы до элемента
                                        except:
                                            continue
                                    link_found = True
                                    break  # Прерываем цикл, так как нужная ссылка найдена
                                except Exception as e:
                                    logging.error(f"Произошла ошибка при клике на ссылку: {str(e)}")
                                    print(f"Произошла ошибка при клике на ссылку: {str(e)}")

                        if not link_found:
                            print(f"Ссылка {site_link} не найдена на странице")

                visit_time = get_visit_time(min_visit_time, max_visit_time)
                stop_flag = threading.Event()

                visit_thread = threading.Thread(target=visit_site, args=(driver, visit_time, stop_flag))
                scroll_thread = threading.Thread(target=scroll_page, args=(driver, stop_flag))

                visit_thread.start()
                scroll_thread.start()

                visit_thread.join()
                scroll_thread.join()

            except Exception as e:
                logging.error("Произошла ошибка: %s", e)
            finally:
                driver.quit()

            interval = random.uniform(min_interval, max_interval)
            print(f"Ожидание перед следующим запросом: {interval} секунд")
            time.sleep(interval)
            time.sleep(3)


        exit_choice = input("Хотите повторить скрипт? (да/нет): ")
        if exit_choice.lower() == "да":
            return find_element_with_navigation(search_queries_file, domain, search_engine, repetitions,
                                            min_interval, max_interval, min_visit_time, max_visit_time)
        else:
            return

def main():

    search_queries_file = input("Введите путь к файлу с запросами: ")

    domain = input("Введите домен без префикса: ")
    # domain = 'https://auto-car.by/'
    search_engine = input("Выберите поисковую систему (Yandex 1 или Google 2): ")
    # search_engine = 'Google'
    repetitions = int(input("Введите количество повторений: "))
    # repetitions = 1
    min_interval = int(input("Введите минимальное время между выполнениями скрипта (в секундах): "))
    # min_interval = 2
    max_interval = int(input("Введите максимальное время между выполнениями скрипта (в секундах): "))
    # max_interval = 5
    min_time = int(input("Введите минимальное время нахождения на сайте (в секундах): "))
    # min_time = 5
    max_time = int(input("Введите максимальное время нахождения на сайте (в секундах): "))
    # max_time = 10
    logging.basicConfig(filename='script.log', level=logging.INFO)
    find_element_with_navigation(search_queries_file, domain, search_engine, repetitions,
                                 min_interval, max_interval, min_time, max_time)
    logging.shutdown()

if __name__ == "__main__":
    main()







