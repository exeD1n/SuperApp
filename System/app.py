# gui/app.py
import logging
import os
from pathlib import Path
import platform
import shutil
import subprocess
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog
from tkinter import ttk
import psutil
from ttkthemes import ThemedTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class App:
    def __init__(self, root):
        
        # Инициализация логгера
        log_file_path = os.path.join('Logs', 'txt.log')
        logging.basicConfig(filename=log_file_path, level=logging.INFO, filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

        # Добавьте обработчик для вывода логов в консоль (опционально)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(console_handler)
        
        self.root = root
        self.root.title("Главное меню")
        self.root.geometry("400x300")
        self.root.minsize(400, 300)
        self.root.set_theme("arc")

        self.performance_window = None
        self.processes_window = None

        container = tk.Frame(root)
        container.pack(fill="both", expand=True)

        button1 = tk.Button(container, text="Производительность ОС", command=self.log_button_click("Производительность ОС", self.show_performance))
        button2 = tk.Button(container, text="Просмотр процессов", command=self.log_button_click("Просмотр процессов", self.show_processes))
        button3 = tk.Button(container, text="Встроенный терминал", command=self.log_button_click("Встроенный терминал", self.open_terminal))
        button4 = tk.Button(container, text="Информация о каналах", command=self.log_button_click("Информация о каналах", self.show_channel_info))
        open_file_manager_button = tk.Button(container, text="Моя система", command=self.open_file_manager_window)

        
        mainmenu = tk.Menu(self.root)
        self.root.config(menu=mainmenu)

        utilities_menu = tk.Menu(mainmenu, tearoff=0)
        utilities_menu.add_command(label="Открыть файловый менеджер", command=self.open_file_manager)       
        utilities_menu.add_command(label="Выполнить поиск", command=self.execute_search)
        utilities_menu.add_command(label="О приложении", command=self.show_about)
        utilities_menu.add_separator()

        mainmenu.add_cascade(label='Утилиты', menu=utilities_menu)
        mainmenu.add_command(label='Справка', command=self.show_help)
        mainmenu.add_command(label='Выход', command=self.on_exit)

        button1.pack(pady=10, fill="both", expand=True)
        button2.pack(pady=10, fill="both", expand=True)
        button3.pack(pady=10, fill="both", expand=True)
        button4.pack(pady=10, fill="both", expand=True)
        open_file_manager_button.pack(pady=10, fill="both", expand=True)

    def open_file_manager_window(self):
        # Создаем окно FileManagerWindow при нажатии кнопки
        file_manager_root = tk.Tk()
        file_manager_window = FileManagerWindow(file_manager_root)
        file_manager_root.mainloop()

    def log_button_click(self, button_text, command_function):
        def wrapper():
            # Логирование нажатия кнопки в файл
            logging.info(f"Button Clicked: {button_text}")
            
            try:
                # Вызов оригинальной функции
                command_function()
            except Exception as e:
                # В случае ошибки также логируем ее
                logging.error(f"Error executing command for {button_text}: {str(e)}")

        return wrapper

    def return_to_main_menu(self):
        # Логирование нажатия кнопки "Вернуться в главное меню"
        logging.info("Button Clicked: Вернуться в главное меню")

        if self.performance_window:
            self.performance_window.destroy()
            self.performance_window = None
        if self.processes_window:
            self.processes_window.destroy()
            self.processes_window = None
        self.root.deiconify()

    def show_performance(self):
        self.root.withdraw()
        self.performance_window = PerformanceWindow(self.root, self.show_main_menu)

    def show_processes(self):
        self.root.withdraw()
        self.processes_window = ProcessesWindow(self.root, self.show_main_menu)

    def open_terminal(self):
        self.root.withdraw()
        root = tk.Tk()
        terminal_gui = TerminalGUI(root, self.show_main_menu)
        root.mainloop()

    def show_channel_info(self):
        root = tk.Tk()
        channel_info_app = ChannelInfoApp(root)
        root.mainloop()

    def open_file_manager(self):
        messagebox.showinfo("Утилиты", "Открыть файловый менеджер")

    def execute_search(self):
        messagebox.showinfo("Утилиты", "Выполнить поиск")

    def show_help(self):
        messagebox.showinfo("Справка", "Создатель: Лутаев Даниил Олегович\nГруппа: ИВТ26-у\nВерсия приложения: 1.0")

    def show_about(self):
        messagebox.showinfo("О приложении", "производительность ос:\nотображает информацию о загрузке процессора, использовании виртуальной памяти, доступной и общей оперативной памяти. обновляет данные в реальном времени.\n\nпросмотр процессов:\nпозволяет просматривать список активных процессов. дает возможность получить дополнительные сведения о выбранном процессе при двойном щелчке мыши. \n\nвстроенный терминал:\nпредоставляет интерфейс для выполнения команд в терминале. выводит результат выполнения команды в текстовое поле.\n\nинформация о каналах:\nотображает информацию о сетевых соединениях для каждого процесса.\n\nутилиты:\nоткрыть файловый менеджер: открывает файловый менеджер (проводник) на операционной системе (поддерживается как на windows, так и на linux).\nвыполнить поиск: открывает новое окно приложения, позволяя выполнить поиск по отрывку текста в файлах, отображает результаты с путями к найденным файлам.\nсправка: выводит информацию о приложении, включая создателя, группу и версию.\n\nвыход:\nзавершает выполнение приложения.")

    def show_main_menu(self):
        if self.performance_window:
            self.performance_window.destroy()
            self.performance_window = None
        if self.processes_window:
            self.processes_window.destroy()
            self.processes_window = None
        self.root.deiconify()

    def on_exit(self):
        if messagebox.askyesno("Выход", "Вы уверены, что хотите выйти из приложения?"):
            self.root.destroy()
            
    def open_file_manager(self):
        if platform.system() == "Windows":
            subprocess.run(["explorer"])
        elif platform.system() == "Linux":
            subprocess.run(["xdg-open", "."])
        else:
            messagebox.showinfo("Ошибка", "Не удалось определить операционную систему.")

    def execute_search(self):
        # Открываем диалоговое окно выбора директории
        directory = filedialog.askdirectory(title="Выберите директорию для поиска")

        # Если пользователь выбрал директорию, выполняем поиск
        if directory:
            # Получает ввод от пользователя (отрывок для поиска)
            search_query = simpledialog.askstring("Поиск", "Введите отрывок для поиска:")
            if search_query is not None:
                # Ищет все файлы в выбранной директории, содержащие отрывок в имени
                results = self.search_files(directory, search_query)

                # Выводит результаты в новом окне
                self.show_search_results(results)

    def search_files(self, directory, search_query):
        # Ищет все файлы в выбранной директории, содержащие отрывок в имени
        results = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if search_query.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    results.append((file, file_path))

        return results

    def show_search_results(self, results):
        # Выводит результаты в новом окне
        if results:
            result_text = "Результаты поиска:\n\n"
            for file, file_path in results:
                result_text += f"{file} - {file_path}\n"
            messagebox.showinfo("Поиск завершен", result_text)
        else:
            messagebox.showinfo("Поиск завершен", "Ничего не найдено.")
            
            
class ChannelInfoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Информация о каналах в ОС")

        self.processes_info = self.get_os_channels()

        label = tk.Label(self.master, text="Информация о каналах в операционной системе:")
        label.pack()

        self.canvas = tk.Canvas(self.master)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.master, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        for process in self.processes_info:
            button_text = f"PID: {process['pid']}, Имя: {process['name']}"
            button = tk.Button(self.frame, text=button_text, command=lambda info=process['pid']: self.show_connection_info(info))
            button.pack()

        # Кнопка для возвращения в главное меню
        return_button = tk.Button(self.master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        return_button.pack(pady=10, fill="both", expand=True)
        
    def get_os_channels(self):
        # Получаем информацию о процессах и их каналах через psutil
        processes_info = []
        for process in psutil.process_iter(['pid', 'name', 'connections']):
            process_info = {
                'pid': process.info['pid'],
                'name': process.info['name'],
                'connections': process.info['connections']
            }
            if process_info['connections']:
                processes_info.append(process_info)
        return processes_info

    def show_connection_info(self, pid):
        # Дополнительная информация о каналах для выбранного процесса
        connection_info = [conn for process in self.processes_info if process['pid'] == pid for conn in process['connections']]
        self.show_connection_window(connection_info)

    def show_connection_window(self, connection_info):
        # Отображаем окно с информацией о каналах
        connection_window = tk.Toplevel(self.master)
        connection_window.title("Дополнительная информация о каналах")

        for connection in connection_info:
            label_text = f"Тип: {connection.type}, Локальный адрес: {connection.laddr}, Удаленный адрес: {connection.raddr}"
            label = tk.Label(connection_window, text=label_text)
            label.pack()

    def return_to_main_menu(self):
        self.master.destroy()
        
# gui/terminal_gui.py
import tkinter as tk
from tkinter import scrolledtext
import subprocess
import platform

class TerminalGUI:
    def __init__(self, master, return_to_main_menu_callback):
        self.master = master
        self.return_to_main_menu_callback = return_to_main_menu_callback
        master.title("Графический терминал")

        # Создаем текстовое поле для вывода результатов
        self.output_text = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=20)
        self.output_text.pack(expand=True, fill=tk.BOTH)

        # Создаем поле для ввода команд
        self.input_entry = tk.Entry(master, width=50)
        self.input_entry.pack(expand=True, fill=tk.BOTH)

        # Создаем кнопку для выполнения команды
        self.run_button = tk.Button(master, text="Выполнить", command=self.execute_command)
        self.run_button.pack(expand=True, fill=tk.BOTH)

        # Создаем кнопку для возврата в главное меню
        self.return_button = tk.Button(master, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(expand=True, fill=tk.BOTH)

    def execute_command(self):
        # Получаем команду из поля ввода
        command = self.input_entry.get()

        try:
            # Проверяем платформу для корректного запуска команд
            if platform.system() == "Windows":
                process = subprocess.Popen(
                    command, shell=True, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True
                )
            else:
                # For Linux, split the command into a list for proper execution
                process = subprocess.Popen(
                    command.split(), shell=False, stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True
                )

            # Получаем результат выполнения команды
            output, error = process.communicate()

            # Очищаем текстовое поле вывода
            self.output_text.delete(1.0, tk.END)

            # Выводим результат в текстовое поле
            self.output_text.insert(tk.END, output)
            self.output_text.insert(tk.END, error)

        except Exception as e:
            # Handle exceptions and display the error message
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Error: {str(e)}")

    def return_to_main_menu(self):
        # Закрываем окно терминала
        self.master.destroy()

        # Возвращаемся в главное меню, вызывая колбэк
        if self.return_to_main_menu_callback:
            self.return_to_main_menu_callback()
            
class PerformanceWindow:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback

        self.performance_window = tk.Toplevel(master)
        self.performance_window.title("Производительность ОС")
        self.performance_window.geometry("400x200")

        self.label_memory = tk.Label(self.performance_window, text="Используемая виртуальная память:")
        self.label_cpu = tk.Label(self.performance_window, text="Общая загрузка процессора:")
        self.label_available_ram = tk.Label(self.performance_window, text="Доступная ОЗУ:")
        self.label_total_ram = tk.Label(self.performance_window, text="Всего ОЗУ:")

        self.label_memory.pack()
        self.label_cpu.pack()
        self.label_available_ram.pack()
        self.label_total_ram.pack()

        self.update_performance_data()

        # Кнопка для возвращения в главное меню
        self.return_button = tk.Button(self.performance_window, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(pady=10)

    def update_performance_data(self):
        memory_info = psutil.virtual_memory()
        cpu_percent = psutil.cpu_percent(interval=1)
        
        self.label_memory.config(text=f"Используемая виртуальная память: {memory_info.used / (1024 ** 3):.2f} GB")
        self.label_cpu.config(text=f"Общая загрузка процессора: {cpu_percent}%")
        self.label_available_ram.config(text=f"Доступная ОЗУ: {memory_info.available / (1024 ** 3):.2f} GB")
        self.label_total_ram.config(text=f"Всего ОЗУ: {memory_info.total / (1024 ** 3):.2f} GB")

        # Планируем обновление данных через 1 секунду
        self.performance_window.after(1000, self.update_performance_data)

    def return_to_main_menu(self):
        self.on_close_callback()

    def destroy(self):
        self.performance_window.destroy()

class ProcessesWindow:
    def __init__(self, master, on_close_callback):
        self.master = master
        self.on_close_callback = on_close_callback

        self.processes_window = tk.Toplevel(master)
        self.processes_window.title("Просмотр процессов")
        self.processes_window.geometry("500x300")

        self.process_listbox = tk.Listbox(self.processes_window, selectmode=tk.SINGLE, exportselection=False)
        self.process_listbox.pack(expand=True, fill=tk.BOTH)

        self.process_listbox.bind("<Double-Button-1>", self.on_double_click)

        # Кнопка для обновления данных
        self.refresh_button = tk.Button(self.processes_window, text="Обновить", command=self.update_processes_data)
        self.refresh_button.pack(pady=10)

        # Кнопка для возвращения в главное меню
        self.return_button = tk.Button(self.processes_window, text="Вернуться в главное меню", command=self.return_to_main_menu)
        self.return_button.pack(pady=10)

        self.update_processes_data()

    def update_processes_data(self):
        self.process_listbox.delete(0, tk.END)

        for process in psutil.process_iter(['pid', 'name', 'create_time']):
            if process.info['name'] != 'python.exe' and process.info['pid'] != os.getpid():
                process_name = process.info['name']
                create_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(process.info['create_time']))
                item_text = f"{process_name} (PID: {process.info['pid']}, Запущен: {create_time})"
                self.process_listbox.insert(tk.END, item_text)

    def on_double_click(self, event):
        selected_index = self.process_listbox.curselection()
        if selected_index:
            selected_process_info = self.process_listbox.get(selected_index)
            messagebox.showinfo("Детали процесса", selected_process_info)

    def return_to_main_menu(self):
        self.on_close_callback()

    def destroy(self):
        self.processes_window.destroy()
        
class FileManagerWindow:
    def __init__(self, master):
        self.master = master
        self.master.title("Файловый менеджер")
        self.master.geometry("600x400")

        # Define the root directory for the file manager
        self.root_directory = 'C:/path/to/SuperApp'

        # Set up the file system event handler
        self.event_handler = FileChangeHandler(self)
        self.observer = Observer()
        self.observer.schedule(self.event_handler, path=self.root_directory, recursive=True)
        self.observer.start()

        # Create a refresh button to manually update the file structure
        refresh_button = tk.Button(master, text="Refresh", command=self.print_directory_structure)
        refresh_button.pack()

        # Print the initial directory structure
        self.print_directory_structure()

    def print_directory_structure(self):
        print(f"Directory Structure (Starting from {self.root_directory}):")
        self._print_directory_structure(self.root_directory, "")

    def _print_directory_structure(self, directory, indent):
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            print(f"{indent}{item}")
            if os.path.isdir(item_path):
                self._print_directory_structure(item_path, indent + "  ")

    def __del__(self):
        self.observer.stop()
        self.observer.join()

class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, file_manager_window):
        self.file_manager_window = file_manager_window

    def on_any_event(self, event):
        if event.is_directory:
            return
        self.file_manager_window.print_directory_structure()