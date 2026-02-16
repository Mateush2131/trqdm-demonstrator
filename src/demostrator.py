#!/usr/bin/env python3
"""
Ядро программы-демонстратора.
Координирует работу всех сценариев и предоставляет единый интерфейс.
"""

import sys
import time
from typing import Dict, Any, Optional
from tqdm import tqdm

from src.scenarios.file_scenario import FileProcessingScenario
from src.scenarios.network_scenario import NetworkDownloadScenario
from src.scenarios.processing_scenario import DataProcessingScenario
from src.utils.console import print_header, print_menu, clear_screen, Colors

class TqdmDemonstrator:
    """
    Главный класс демонстратора.
    
    Отвечает за:
    - Инициализацию всех сценариев
    - Управление жизненным циклом программы
    - Сбор и отображение общей статистики
    - Обработку ошибок
    """
    
    def __init__(self):
        """Инициализация демонстратора."""
        self.scenarios = {
            "1": {
                "name": "Обработка файлов",
                "description": "Базовый прогресс-бар, пакетная обработка, настройка внешнего вида",
                "instance": FileProcessingScenario(),
                "color": Colors.GREEN
            },
            "2": {
                "name": "Загрузка из сети", 
                "description": "Вложенные прогресс-бары, имитация множественных загрузок",
                "instance": NetworkDownloadScenario(),
                "color": Colors.BLUE
            },
            "3": {
                "name": "Обработка данных",
                "description": "Ручное управление прогрессом, кастомные метрики, генераторы",
                "instance": DataProcessingScenario(),
                "color": Colors.MAGENTA
            }
        }
        self.results_history: Dict[str, list] = {
            "file": [],
            "network": [],
            "processing": []
        }
        self.session_start = time.time()
    
    def show_welcome(self):
        """Показывает приветственное сообщение."""
        clear_screen()
        print_header("ДЕМОНСТРАТОР БИБЛИОТЕКИ TQDM v1.0")
        print(f"\n{Colors.CYAN}Исследовательский проект: Визуализация прогресса в Python{Colors.END}")
        print(f"\n{Colors.YELLOW}Библиотека tqdm предоставляет быстрые и расширяемые")
        print("прогресс-бары для длительных операций.{Colors.END}\n")
        print("Данная программа демонстрирует ключевые возможности:\n")
        print(f"  {Colors.GREEN}• Базовые прогресс-бары и их настройка{Colors.END}")
        print(f"  {Colors.BLUE}• Вложенные прогресс-бары{Colors.END}")
        print(f"  {Colors.MAGENTA}• Ручное управление и кастомные метрики{Colors.END}")
        print(f"  {Colors.CYAN}• Работа с различными типами данных{Colors.END}\n")
        time.sleep(2)
    
    def show_menu(self) -> str:
        """
        Отображает меню выбора сценария.
        
        Returns:
            str: Выбранный пункт меню
        """
        clear_screen()
        print_header("ГЛАВНОЕ МЕНЮ")
        
        menu_items = []
        for key, scenario in self.scenarios.items():
            menu_items.append(
                f"{scenario['color']}{key}. {scenario['name']}{Colors.END}\n"
                f"   {Colors.WHITE}{scenario['description']}{Colors.END}"
            )
        
        menu_items.append(f"{Colors.RED}4. Выход{Colors.END}\n   Завершение работы программы")
        
        print("\n" + "\n\n".join(menu_items) + "\n")
        
        choice = input(f"{Colors.YELLOW}Выберите сценарий (1-4): {Colors.END}").strip()
        return choice
    
    def run_scenario(self, scenario_key: str) -> Optional[Dict[str, Any]]:
        """
        Запускает выбранный сценарий.
        
        Args:
            scenario_key: Ключ сценария
            
        Returns:
            Optional[Dict[str, Any]]: Результаты выполнения
        """
        if scenario_key not in self.scenarios:
            return None
        
        scenario_info = self.scenarios[scenario_key]
        scenario = scenario_info["instance"]
        
        clear_screen()
        print_header(f"СЦЕНАРИЙ: {scenario_info['name']}")
        print(f"\n{Colors.CYAN}{scenario_info['description']}{Colors.END}\n")
        
        try:
            # Показываем подсказки перед запуском
            print(f"{Colors.YELLOW}Что будет показано:{Colors.END}")
            self._show_scenario_hints(scenario_key)
            print(f"\n{Colors.GREEN}Нажмите Enter для запуска...{Colors.END}")
            input()
            
            # Запускаем сценарий
            results = scenario.run()
            
            # Сохраняем результаты
            self._save_results(scenario_key, results)
            
            # Показываем сводку
            self._show_scenario_summary(results)
            
            return results
            
        except KeyboardInterrupt:
            print(f"\n\n{Colors.YELLOW}Сценарий прерван пользователем{Colors.END}")
            return None
        except Exception as e:
            print(f"\n{Colors.RED}Ошибка при выполнении сценария: {e}{Colors.END}")
            return None
    
    def _show_scenario_hints(self, scenario_key: str):
        """
        Показывает подсказки о том, на что обратить внимание в сценарии.
        
        Args:
            scenario_key: Ключ сценария
        """
        hints = {
            "1": [
                "✓ Автоматическое создание прогресс-бара при оборачивании итератора",
                "✓ Изменение описания (desc) в процессе работы",
                "✓ Дополнительная информация справа (postfix)",
                "✓ Цветовое оформление и единицы измерения",
                "✓ Запись логов без поломки прогресс-бара"
            ],
            "2": [
                "✓ Два уровня вложенности: общий прогресс и по файлам",
                "✓ Параметр position для фиксации позиции баров",
                "✓ leave=False для автоматического скрытия завершенных баров",
                "✓ Обновление обоих баров одновременно",
                "✓ Имитация реальной загрузки с меняющейся скоростью"
            ],
            "3": [
                "✓ Ручное управление прогрессом через update()",
                "✓ Работа с генераторами, где неизвестен total",
                "✓ Множественные кастомные метрики в постфиксе",
                "✓ Детальная статистика по времени выполнения",
                "✓ Комбинирование с дополнительным выводом"
            ]
        }
        
        for hint in hints.get(scenario_key, []):
            print(f"  {hint}")
    
    def _save_results(self, scenario_key: str, results: Dict[str, Any]):
        """
        Сохраняет результаты выполнения.
        
        Args:
            scenario_key: Ключ сценария
            results: Результаты выполнения
        """
        category = {
            "1": "file",
            "2": "network", 
            "3": "processing"
        }.get(scenario_key, "other")
        
        self.results_history[category].append({
            "timestamp": time.time(),
            "results": results
        })
    
    def _show_scenario_summary(self, results: Dict[str, Any]):
        """
        Показывает сводку по результатам сценария.
        
        Args:
            results: Результаты выполнения
        """
        print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
        print(f"{Colors.BOLD}СВОДКА РЕЗУЛЬТАТОВ:{Colors.END}")
        print(f"{Colors.GREEN}{'='*50}{Colors.END}")
        
        for key, value in results.items():
            if isinstance(value, (int, float, str)):
                print(f"  {key}: {value}")
            elif isinstance(value, list) and len(value) < 5:
                print(f"  {key}: {value}")
            elif isinstance(value, dict):
                print(f"  {key}:")
                for k, v in value.items():
                    if isinstance(v, (int, float)):
                        print(f"    {k}: {v:.2f}" if isinstance(v, float) else f"    {k}: {v}")
        
        print(f"\n{Colors.YELLOW}Нажмите Enter для возврата в меню...{Colors.END}")
        input()
    
    def show_farewell(self):
        """Показывает прощальное сообщение и статистику сессии."""
        clear_screen()
        session_duration = time.time() - self.session_start
        
        print_header("ИТОГИ СЕССИИ")
        
        print(f"\n{Colors.CYAN}Время работы: {session_duration:.1f} секунд{Colors.END}")
        print(f"\n{Colors.BOLD}Выполнено сценариев:{Colors.END}")
        
        total_runs = 0
        for category, runs in self.results_history.items():
            count = len(runs)
            total_runs += count
            if count > 0:
                color = Colors.GREEN if category == "file" else Colors.BLUE if category == "network" else Colors.MAGENTA
                print(f"  {color}• {category.capitalize()}: {count} запусков{Colors.END}")
        
        if total_runs > 0:
            print(f"\n{Colors.YELLOW}Всего демонстраций: {total_runs}{Colors.END}")
        
        print(f"\n{Colors.GREEN}Спасибо за использование демонстратора!{Colors.END}")
        print(f"{Colors.CYAN}Исследование библиотеки tqdm завершено.{Colors.END}\n")
    
    def run(self):
        """
        Запускает основной цикл демонстратора.
        """
        self.show_welcome()
        
        while True:
            choice = self.show_menu()
            
            if choice == "4":
                self.show_farewell()
                break
            
            if choice in self.scenarios:
                self.run_scenario(choice)
            else:
                print(f"\n{Colors.RED}Неверный выбор. Нажмите Enter...{Colors.END}")
                input()


def main() -> int:
    """
    Точка входа в демонстратор.
    
    Returns:
        int: Код возврата
    """
    try:
        demonstrator = TqdmDemonstrator()
        demonstrator.run()
        return 0
    except Exception as e:
        print(f"\n{Colors.RED}Критическая ошибка: {e}{Colors.END}")
        return 1


if __name__ == "__main__":
    sys.exit(main())