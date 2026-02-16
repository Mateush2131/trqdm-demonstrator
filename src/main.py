#!/usr/bin/env python3
"""
Главный модуль программы.
Реализует меню выбора сценариев демонстрации.
"""

import sys
from typing import Optional

from src.utils.console import Colors, print_header, print_menu, clear_screen, wait_for_enter
from src.scenarios.file_scenario import FileProcessingScenario
from src.scenarios.network_scenario import NetworkDownloadScenario
from src.scenarios.processing_scenario import DataProcessingScenario
from src.utils.storage_manager import StorageManager
from src.utils.storage_console import StorageConsole

def main() -> int:
    """
    Главная функция программы.
    
    Returns:
        int: Код возврата (0 - успешно, 1 - ошибка)
    """
    try:
        while True:
            clear_screen()
            print_header("ДЕМОНСТРАТОР ВОЗМОЖНОСТЕЙ БИБЛИОТЕКИ TQDM")
            print(f"\n{Colors.BOLD}Выберите сценарий для демонстрации:{Colors.END}\n")
            
            menu_items = [
                ("Обработка файлов", "Базовый прогресс-бар, пакетная обработка"),
                ("Загрузка из сети", "Вложенные прогресс-бары, имитация загрузки"),
                ("Обработка данных", "Ручное управление прогрессом, кастомные метрики"),
                ("Управление хранилищем", "Просмотр, удаление, архивация файлов"),
                ("Выход", "Завершение программы")
            ]
            
            print_menu(menu_items)
            
            choice = input(f"\n{Colors.YELLOW}Введите номер пункта (1-5): {Colors.END}").strip()
            
            if choice == "1":
                scenario = FileProcessingScenario()
                scenario.run()
                wait_for_enter()
                
            elif choice == "2":
                scenario = NetworkDownloadScenario()
                scenario.run()
                wait_for_enter()
                
            elif choice == "3":
                scenario = DataProcessingScenario()
                scenario.run()
                wait_for_enter()
                
            elif choice == "4":
                storage_mgr = StorageManager()
                storage_console = StorageConsole(storage_mgr)
                storage_console.run()
                wait_for_enter()
                
            elif choice == "5":
                print(f"\n{Colors.GREEN}Программа завершена.{Colors.END}")
                break
                
            else:
                print(f"\n{Colors.RED}Неверный выбор. Пожалуйста, введите 1-5.{Colors.END}")
                wait_for_enter()
                
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Программа прервана пользователем.{Colors.END}")
        return 0
    except Exception as e:
        print(f"\n{Colors.RED}Критическая ошибка: {e}{Colors.END}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())