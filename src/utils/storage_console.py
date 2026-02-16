#!/usr/bin/env python3
"""
Консольный интерфейс для управления хранилищем.
"""

import os
from src.utils.console import Colors, clear_screen, print_header
from src.utils.storage_manager import StorageManager

class StorageConsole:
    
    def __init__(self, storage_manager: StorageManager):
        self.storage = storage_manager
        self.current_dir = None
        self.current_files = []
    
    def print_storage_summary(self):
        summary = self.storage.get_storage_summary()
        
        print(f"\n{Colors.BOLD}СВОДКА ПО ХРАНИЛИЩУ:{Colors.END}")
        print(f"{'─' * 60}")
        
        for key, data in summary.items():
            if key == "total":
                continue
            print(f"{Colors.CYAN}{key.upper():12}{Colors.END} "
                  f"📄 {data['count']:4} файлов  "
                  f"💾 {data['size_hr']:>8}")
        
        print(f"{'─' * 60}")
        print(f"{Colors.GREEN}ВСЕГО:{Colors.END}         "
              f"📄 {summary['total']['count']:4} файлов  "
              f"💾 {summary['total']['size_hr']:>8}")
    
    def list_directory(self, dir_key: str):
        info = self.storage.get_directory_info(dir_key)
        
        if info["count"] == 0:
            print(f"\n{Colors.YELLOW}Директория {dir_key} пуста{Colors.END}")
            self.current_dir = dir_key
            self.current_files = []
            return
        
        print(f"\n{Colors.BOLD}СОДЕРЖИМОЕ {dir_key.upper()}:{Colors.END}")
        print(f"{'─' * 90}")
        print(f"{'#':<4} {'Имя файла':<50} {'Размер':<10} {'Дата изменения':<20}")
        print(f"{'─' * 90}")
        
        for i, file in enumerate(info["files"], 1):
            name = file["name"]
            if len(name) > 48:
                name = name[:45] + "..."
            date = file["modified"].strftime("%Y-%m-%d %H:%M")
            print(f"{i:<4} {name:<50} {file['size_hr']:<10} {date:<20}")
        
        print(f"{'─' * 90}")
        print(f"Всего: {info['count']} файлов, {info['size_hr']}")
        
        self.current_dir = dir_key
        self.current_files = info["files"]
    
    def delete_file_interactive(self):
        if not self.current_files:
            print(f"\n{Colors.RED}Нет файлов для удаления{Colors.END}")
            return
        
        try:
            choice = input(f"\n{Colors.YELLOW}Введите номер файла (0 - отмена): {Colors.END}")
            if not choice.isdigit():
                return
            
            idx = int(choice)
            if idx == 0:
                return
            
            if 1 <= idx <= len(self.current_files):
                file = self.current_files[idx-1]
                confirm = input(f"Удалить {file['name']}? (y/n): ").lower()
                if confirm == 'y':
                    success, msg = self.storage.delete_file(file['path'])
                    print(f"{Colors.GREEN if success else Colors.RED}{msg}{Colors.END}")
                    if success:
                        self.list_directory(self.current_dir)
        except ValueError:
            pass
    
    def move_file_interactive(self):
        if not self.current_files:
            print(f"\n{Colors.RED}Нет файлов для перемещения{Colors.END}")
            return
        
        try:
            choice = input(f"\n{Colors.YELLOW}Введите номер файла: {Colors.END}")
            if not choice.isdigit():
                return
            
            idx = int(choice)
            if 1 <= idx <= len(self.current_files):
                file = self.current_files[idx-1]
                
                print(f"\n{Colors.CYAN}Куда переместить?{Colors.END}")
                targets = ["processed", "temp", "downloads", "archive", "quarantine"]
                for i, name in enumerate(targets, 1):
                    print(f"   {i}. {name}")
                
                target = input(f"{Colors.YELLOW}Выберите (1-5): {Colors.END}")
                if target.isdigit() and 1 <= int(target) <= 5:
                    target_key = targets[int(target)-1]
                    success, msg = self.storage.move_file(file['path'], target_key)
                    print(f"{Colors.GREEN if success else Colors.RED}{msg}{Colors.END}")
                    if success:
                        self.list_directory(self.current_dir)
        except ValueError:
            pass
    
    def copy_file_interactive(self):
        if not self.current_files:
            print(f"\n{Colors.RED}Нет файлов для копирования{Colors.END}")
            return
        
        try:
            choice = input(f"\n{Colors.YELLOW}Введите номер файла: {Colors.END}")
            if not choice.isdigit():
                return
            
            idx = int(choice)
            if 1 <= idx <= len(self.current_files):
                file = self.current_files[idx-1]
                
                print(f"\n{Colors.CYAN}Куда скопировать?{Colors.END}")
                targets = ["processed", "temp", "downloads", "archive", "quarantine"]
                for i, name in enumerate(targets, 1):
                    print(f"   {i}. {name}")
                
                target = input(f"{Colors.YELLOW}Выберите (1-5): {Colors.END}")
                if target.isdigit() and 1 <= int(target) <= 5:
                    target_key = targets[int(target)-1]
                    success, msg = self.storage.copy_file(file['path'], target_key)
                    print(f"{Colors.GREEN if success else Colors.RED}{msg}{Colors.END}")
        except ValueError:
            pass
    
    def archive_directory_interactive(self):
        print(f"\n{Colors.CYAN}Какую директорию архивировать?{Colors.END}")
        targets = ["temp", "processed", "downloads"]
        for i, name in enumerate(targets, 1):
            print(f"   {i}. {name}")
        
        choice = input(f"{Colors.YELLOW}Выберите (1-3): {Colors.END}")
        if choice.isdigit() and 1 <= int(choice) <= 3:
            target_key = targets[int(choice)-1]
            success, msg = self.storage.create_archive(target_key)
            print(f"{Colors.GREEN if success else Colors.RED}{msg}{Colors.END}")
    
    def search_files_interactive(self):
        query = input(f"\n{Colors.YELLOW}Введите текст для поиска: {Colors.END}").strip()
        if not query:
            return
        
        results = self.storage.search_files(query)
        if not results:
            print(f"\n{Colors.YELLOW}Ничего не найдено{Colors.END}")
            return
        
        print(f"\n{Colors.GREEN}Найдено {len(results)} файлов:{Colors.END}")
        print(f"{'─' * 80}")
        for i, file in enumerate(results, 1):
            date = file["modified"].strftime("%Y-%m-%d %H:%M")
            print(f"{i}. {file['name']}")
            print(f"   📁 {file['directory']}  💾 {file['size_hr']}  🕒 {date}")
    
    def run(self):
        while True:
            clear_screen()
            print_header("МЕНЕДЖЕР ХРАНИЛИЩА")
            self.print_storage_summary()
            
            print(f"\n{Colors.BOLD}ДЕЙСТВИЯ:{Colors.END}")
            print("   1. Просмотреть temp")
            print("   2. Просмотреть processed")
            print("   3. Просмотреть downloads")
            print("   4. Просмотреть archive")
            print("   5. Просмотреть quarantine")
            print("   " + "─" * 40)
            print("   6. Удалить файл")
            print("   7. Переместить файл")
            print("   8. Копировать файл")
            print("   9. Архивировать директорию")
            print("   10. Поиск файлов")
            print("   " + "─" * 40)
            print("   0. Очистить temp")
            print("   q. Выход")
            
            choice = input(f"\n{Colors.YELLOW}Выберите действие: {Colors.END}").lower()
            
            if choice == "q":
                break
            elif choice == "1":
                self.list_directory("temp")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "2":
                self.list_directory("processed")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "3":
                self.list_directory("downloads")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "4":
                self.list_directory("archive")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "5":
                self.list_directory("quarantine")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "6":
                self.delete_file_interactive()
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "7":
                self.move_file_interactive()
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "8":
                self.copy_file_interactive()
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "9":
                self.archive_directory_interactive()
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "10":
                self.search_files_interactive()
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")
            elif choice == "0":
                confirm = input(f"{Colors.RED}Очистить temp? (y/n): {Colors.END}")
                if confirm.lower() == 'y':
                    count, msg = self.storage.delete_all_in_directory("temp")
                    print(f"{Colors.GREEN}{msg}{Colors.END}")
                input(f"\n{Colors.GREEN}Нажмите Enter...{Colors.END}")