#!/usr/bin/env python3
"""
Утилиты для работы с консолью.
"""

import os
import sys

# Цвета для вывода
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BLACK = '\033[90m'
    END = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    NORMAL = '\033[22m'
    RESET_ALL = '\033[0m'

# Для совместимости с colorama-стилем
Fore = Colors
Style = Colors

def clear_screen():
    """Очистка экрана терминала."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(text: str):
    """
    Печать заголовка с рамкой.
    
    Args:
        text: Текст заголовка
    """
    width = min(len(text) + 4, 80)
    print(f"{Colors.CYAN}{Colors.BOLD}┌{'─' * (width-2)}┐{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}│ {text:^{width-4}} │{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}└{'─' * (width-2)}┘{Colors.END}")

def print_menu(items: list):
    """
    Печать меню.
    
    Args:
        items: Список кортежей (название, описание)
    """
    for i, (title, desc) in enumerate(items, 1):
        print(f"  {Colors.YELLOW}{Colors.BOLD}{i}.{Colors.END} ", end="")
        print(f"{Colors.WHITE}{title}{Colors.END}")
        if desc:
            print(f"     {Colors.BLUE}{desc}{Colors.END}")
        print()

def wait_for_enter():
    """Ожидание нажатия Enter."""
    input(f"\n{Colors.GREEN}Нажмите Enter для продолжения...{Colors.END}")

def print_progress_info(iteration: int, total: int, elapsed: float, 
                        speed: float, **kwargs):
    """
    Печать дополнительной информации о прогрессе.
    
    Args:
        iteration: Текущая итерация
        total: Всего итераций
        elapsed: Прошедшее время
        speed: Скорость обработки
        **kwargs: Дополнительные параметры
    """
    percent = (iteration / total) * 100
    eta = (elapsed / iteration) * (total - iteration) if iteration > 0 else 0
    
    print(f"\n{Colors.MAGENTA}Детальная информация:{Colors.END}")
    print(f"  Выполнено: {iteration}/{total} ({percent:.1f}%)")
    print(f"  Прошло: {elapsed:.1f}с, Осталось: {eta:.1f}с")
    print(f"  Скорость: {speed:.2f} ед/с")
    
    if kwargs:
        print(f"  Дополнительно: {kwargs}")