#!/usr/bin/env python3
"""
Утилита для генерации и обработки тестовых файлов.
Создает файлы в storage/temp/ и сохраняет результаты в storage/processed/
"""

import os
import random
import string
import datetime
from typing import List, Tuple

class FileGenerator:
    """
    Генератор тестовых файлов.
    """
    
    def __init__(self, base_dir: str = "storage"):
        """
        Инициализация генератора.
        
        Args:
            base_dir: Базовая директория для хранения файлов
        """
        self.base_dir = base_dir
        self.temp_dir = os.path.join(base_dir, "temp")
        self.processed_dir = os.path.join(base_dir, "processed")
        self.generated_files: List[str] = []
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Создает все необходимые директории."""
        os.makedirs(self.temp_dir, exist_ok=True)
        os.makedirs(self.processed_dir, exist_ok=True)
    
    def _human_readable_size(self, size: int) -> str:
        """Конвертирует размер в человекочитаемый формат."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def show_storage_status(self):
        """Показывает статус хранилища."""
        print(f"\n📊 СТАТУС ХРАНИЛИЩА:")
        
        if os.path.exists(self.temp_dir):
            temp_files = [f for f in os.listdir(self.temp_dir) 
                         if os.path.isfile(os.path.join(self.temp_dir, f))]
            temp_size = sum(os.path.getsize(os.path.join(self.temp_dir, f)) 
                          for f in temp_files)
            print(f"   📁 Временные файлы (temp):")
            print(f"      Файлов: {len(temp_files)}")
            print(f"      Размер: {self._human_readable_size(temp_size)}")
        
        if os.path.exists(self.processed_dir):
            proc_files = [f for f in os.listdir(self.processed_dir) 
                         if os.path.isfile(os.path.join(self.processed_dir, f))]
            proc_size = sum(os.path.getsize(os.path.join(self.processed_dir, f)) 
                          for f in proc_files)
            print(f"   📁 Обработанные файлы (processed):")
            print(f"      Файлов: {len(proc_files)}")
            print(f"      Размер: {self._human_readable_size(proc_size)}")
    
    def generate_test_files(self, count: int = 20, 
                           extensions: List[str] = None) -> List[str]:
        """
        Генерация тестовых файлов во временную папку.
        """
        if extensions is None:
            extensions = ['.txt', '.log', '.dat', '.csv', '.tmp']
        
        generated = []
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"\n🔨 Генерация {count} тестовых файлов...")
        
        for i in range(1, count + 1):
            ext = random.choice(extensions)
            filename = f"test_file_{i:03d}_{timestamp}{ext}"
            filepath = os.path.join(self.temp_dir, filename)
            
            content = self._generate_content(i, timestamp)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.generated_files.append(filepath)
            generated.append(filepath)
            
            if i % 5 == 0:
                print(f"   Создано {i} файлов...")
        
        print(f"✅ Создано {count} файлов")
        return generated
    
    def _generate_content(self, file_num: int, timestamp: str) -> str:
        """Генерирует содержимое файла."""
        lines = []
        lines.append(f"ФАЙЛ #{file_num}")
        lines.append(f"Создан: {timestamp}")
        lines.append(f"Генератор: tqdm-demonstrator")
        lines.append("-" * 40)
        
        for i in range(random.randint(5, 15)):
            random_line = ''.join(random.choices(
                string.ascii_letters + string.digits + ' ' * 5,
                k=random.randint(20, 60)
            ))
            lines.append(random_line)
        
        lines.append("-" * 40)
        lines.append(f"КОНЕЦ ФАЙЛА #{file_num}")
        
        return '\n'.join(lines)
    
    def process_file(self, file_path: str) -> Tuple[bool, str]:
        """
        Обработка одного файла с сохранением результата.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            filename = os.path.basename(file_path)
            name_without_ext = os.path.splitext(filename)[0]
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            processed_filename = f"{name_without_ext}_processed_{timestamp}.txt"
            processed_path = os.path.join(self.processed_dir, processed_filename)
            
            processed_lines = []
            processed_lines.append("=" * 60)
            processed_lines.append(f"ОБРАБОТАННЫЙ ФАЙЛ")
            processed_lines.append("=" * 60)
            processed_lines.append(f"Оригинал: {filename}")
            processed_lines.append(f"Обработан: {timestamp}")
            processed_lines.append(f"Размер: {len(content)} символов")
            processed_lines.append(f"Строк: {len(content.splitlines())}")
            processed_lines.append("-" * 60)
            processed_lines.append(content)
            processed_lines.append("-" * 60)
            processed_lines.append("КОНЕЦ ОБРАБОТАННОГО ФАЙЛА")
            processed_lines.append("=" * 60)
            
            with open(processed_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(processed_lines))
            
            return True, processed_path
            
        except Exception as e:
            return False, str(e)
    
    def get_temp_files(self) -> List[str]:
        """Возвращает список временных файлов."""
        if not os.path.exists(self.temp_dir):
            return []
        return [f for f in os.listdir(self.temp_dir) 
                if os.path.isfile(os.path.join(self.temp_dir, f))]
    
    def get_processed_files(self) -> List[str]:
        """Возвращает список обработанных файлов."""
        if not os.path.exists(self.processed_dir):
            return []
        return [f for f in os.listdir(self.processed_dir) 
                if os.path.isfile(os.path.join(self.processed_dir, f))]
    
    def cleanup_temp(self):
        """Очищает временную папку."""
        if os.path.exists(self.temp_dir):
            files = os.listdir(self.temp_dir)
            for filename in files:
                filepath = os.path.join(self.temp_dir, filename)
                try:
                    if os.path.isfile(filepath):
                        os.remove(filepath)
                except Exception as e:
                    print(f"   Ошибка удаления {filename}: {e}")
            print(f"\n🧹 Временная папка очищена: {len(files)} файлов удалено")
        
        self.generated_files = []