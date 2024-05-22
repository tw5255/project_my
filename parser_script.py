import tkinter as tk
import threading
from urllib.parse import urlparse
from time import time

from botparser import parse_website

root = tk.Tk()
root.title("Выполнение скрипта")

domainentry = tk.Entry(root, width=50)
domainentry.pack()
domainentry.insert(0, "Введите домен")

status_text = tk.StringVar()
status_text.set("Ожидание запуска")
status_label = tk.Label(root, textvariable=status_text)
status_label.pack()

def runscript():
    domain = domainentry.get()

    # Проверяем, является ли введенный домен допустимым URL-адресом
    if not is_valid_url(domain):
        status_text.set("Неверный ввод домена. Повторите попытку.")
        return

    # Убираем префикс "http://" или "https://" из домена, если он присутствует
    if domain.startswith("http://"):
        domain = domain[7:]
    elif domain.startswith("https://"):
        domain = domain[8:]

    # Обновляем статус, чтобы показать, что скрипт запущен
    status_text.set("Парсинг запущен")

    # Создаем новый поток для выполнения функции parse_website
    thread = threading.Thread(target=parse_website, args=(domain,))
    thread.start()

    # Добавляем событие в очередь событий для вывода сообщения после завершения потока
    root.after(1000, lambda: check_thread_status(thread))

def check_thread_status(thread):
    # Проверяем, жив ли поток
    if thread.is_alive():
        # Поток все еще выполняется, поэтому обновляем статус и планируем проверить его снова через секунду
        status_text.set("Парсинг продолжается...")
        root.after(1000, lambda: check_thread_status(thread))
    else:
        # Поток завершился, поэтому обновляем статус и выводим сообщение о завершении
        status_text.set("Парсинг завершен")
        outputtext.insert(tk.END, "Поздравляем, парсинг завершен, ссылки сохранены в файл links.txt на рабочем столе! "
                                              "Для выхода из програмы закройте это окно!")

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

button = tk.Button(root, text="Запустить скрипт", command=runscript)
button.pack()

outputtext = tk.Text(root, height=10, width=50)
outputtext.pack()

root.mainloop()



