#!/usr/bin/env python3
"""
Сценарий обработки файлов.
"""

import os
import time
import random
from tqdm import tqdm
from typing import Dict, Any, List

from src.scenarios.base_scenario import BaseScenario
from src.utils.file_generator import FileGenerator
from src.utils.console import Colors, Style

class FileProcessingScenario(BaseScenario):
    
    def __init__(self):
        super().__init__(
            "Обработка файлов",
            "Реальная обработка файлов с сохранением результатов в storage/processed/"
        )
        self.file_generator = FileGenerator()
    
    def run(self) -> Dict[str, Any]:
        with self:
            self.file_generator.show_storage_status()
            
            print(f"\n{Colors.YELLOW}ШАГ 1: Генерация тестовых файлов{Style.RESET_ALL}")
            test_files = self.file_generator.generate_test_files(
                count=20,
                extensions=['.txt', '.log', '.dat', '.csv', '.tmp']
            )
            
            print(f"\n{Colors.YELLOW}ШАГ 2: Обработка файлов{Style.RESET_ALL}")
            successful = 0
            failed = 0
            processed_paths = []
            
            with tqdm(
                total=len(test_files),
                desc="Обработка файлов",
                unit="файл",
                colour="green",
                bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
            ) as pbar:
                
                for file_path in test_files:
                    filename = os.path.basename(file_path)
                    pbar.set_description(f"Обработка {filename}")
                    
                    time.sleep(random.uniform(0.3, 0.8))
                    
                    success, result = self.file_generator.process_file(file_path)
                    
                    if success:
                        successful += 1
                        processed_paths.append(result)
                        pbar.set_postfix(успешно=successful, ошибок=failed)
                    else:
                        failed += 1
                        pbar.set_postfix(успешно=successful, ошибок=failed)
                        pbar.write(f"   ⚠️ Ошибка обработки {filename}: {result}")
                    
                    pbar.update(1)
            
            print(f"\n{Colors.YELLOW}ШАГ 3: Результаты{Style.RESET_ALL}")
            print(f"\n{Colors.GREEN}Обработано успешно: {successful}, ошибок: {failed}{Style.RESET_ALL}")
            
            print(f"\n{Colors.YELLOW}ШАГ 4: Очистка временных файлов{Style.RESET_ALL}")
            self.file_generator.cleanup_temp()
            
            self.file_generator.show_storage_status()
            
            return {
                "total": len(test_files),
                "successful": successful,
                "failed": failed,
                "success_rate": f"{(successful/len(test_files))*100:.1f}%"
            }