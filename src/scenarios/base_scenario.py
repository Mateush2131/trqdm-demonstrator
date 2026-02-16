#!/usr/bin/env python3
"""
Базовый класс для всех сценариев.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import time

class BaseScenario(ABC):
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.start_time = 0
        self.end_time = 0
    
    def __enter__(self):
        self.start_time = time.time()
        print(f"\n=== Запуск сценария: {self.name} ===")
        print(f"Описание: {self.description}\n")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        print(f"\n=== Сценарий завершен за {duration:.2f}с ===\n")
    
    @abstractmethod
    def run(self) -> Dict[str, Any]:
        pass