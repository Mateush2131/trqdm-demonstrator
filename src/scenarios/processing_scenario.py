#!/usr/bin/env python3
"""
Сценарий обработки данных.
"""

import time
import random
from tqdm import tqdm
from typing import Dict, Any, List, Generator
import math

from src.scenarios.base_scenario import BaseScenario
from src.utils.console import Colors, Style, print_progress_info

class DataProcessingScenario(BaseScenario):
    
    def __init__(self):
        super().__init__(
            "Обработка данных",
            "Ручное управление прогрессом и кастомные метрики"
        )
    
    def data_generator(self, count: int) -> Generator[int, None, None]:
        for i in range(count):
            time.sleep(random.uniform(0.01, 0.05))
            yield i * random.randint(1, 100)
    
    def complex_calculation(self, data: int) -> Dict[str, float]:
        time.sleep(random.uniform(0.05, 0.2))
        return {
            "value": data,
            "sqrt": math.sqrt(data if data > 0 else 1),
            "log": math.log(data + 1),
            "sin": math.sin(data),
            "cos": math.cos(data)
        }
    
    def run(self) -> Dict[str, Any]:
        with self:
            data_count = 100
            print(f"Генерация {data_count} элементов...")
            
            results = []
            processing_stats = {
                "min_time": float('inf'),
                "max_time": 0,
                "total_time": 0
            }
            
            with tqdm(
                total=data_count,
                desc="Обработка данных",
                unit="элемент",
                colour="magenta"
            ) as pbar:
                
                for i, data in enumerate(self.data_generator(data_count)):
                    start_time = time.time()
                    result = self.complex_calculation(data)
                    process_time = time.time() - start_time
                    
                    processing_stats["min_time"] = min(processing_stats["min_time"], process_time)
                    processing_stats["max_time"] = max(processing_stats["max_time"], process_time)
                    processing_stats["total_time"] += process_time
                    
                    results.append(result)
                    
                    pbar.set_postfix(
                        min=f"{processing_stats['min_time']*1000:.1f}ms",
                        max=f"{processing_stats['max_time']*1000:.1f}ms",
                        avg=f"{(processing_stats['total_time']/(i+1))*1000:.1f}ms"
                    )
                    
                    pbar.update(1)
            
            print(f"\n{Colors.GREEN}Обработка завершена{Style.RESET_ALL}")
            
            return {
                "processed_items": len(results),
                "avg_time_ms": (processing_stats['total_time']/len(results))*1000,
                "min_time_ms": processing_stats['min_time']*1000,
                "max_time_ms": processing_stats['max_time']*1000
            }