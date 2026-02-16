#!/usr/bin/env python3
"""
Менеджер хранилища - управление файлами.
"""

import os
import shutil
import zipfile
import datetime
from typing import List, Dict, Tuple

class StorageManager:
    
    def __init__(self, base_dir: str = "storage"):
        self.base_dir = base_dir
        self.directories = {
            "temp": os.path.join(base_dir, "temp"),
            "processed": os.path.join(base_dir, "processed"),
            "downloads": os.path.join(base_dir, "downloads"),
            "archive": os.path.join(base_dir, "archive"),
            "quarantine": os.path.join(base_dir, "quarantine")
        }
        self._ensure_directories()
    
    def _ensure_directories(self):
        for dir_path in self.directories.values():
            os.makedirs(dir_path, exist_ok=True)
    
    def _human_readable_size(self, size: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024.0:
                return f"{size:.1f} {unit}"
            size /= 1024.0
        return f"{size:.1f} TB"
    
    def get_directory_info(self, dir_key: str) -> Dict:
        dir_path = self.directories.get(dir_key)
        if not dir_path or not os.path.exists(dir_path):
            return {"exists": False, "files": [], "size": 0, "count": 0}
        
        files = []
        total_size = 0
        
        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename)
            if os.path.isfile(filepath):
                stat = os.stat(filepath)
                files.append({
                    "name": filename,
                    "path": filepath,
                    "size": stat.st_size,
                    "size_hr": self._human_readable_size(stat.st_size),
                    "modified": datetime.datetime.fromtimestamp(stat.st_mtime)
                })
                total_size += stat.st_size
        
        files.sort(key=lambda x: x["modified"], reverse=True)
        
        return {
            "exists": True,
            "path": dir_path,
            "files": files,
            "count": len(files),
            "size": total_size,
            "size_hr": self._human_readable_size(total_size)
        }
    
    def delete_file(self, filepath: str) -> Tuple[bool, str]:
        try:
            if os.path.exists(filepath):
                filename = os.path.basename(filepath)
                os.remove(filepath)
                return True, f"✅ Файл удален: {filename}"
            return False, "❌ Файл не найден"
        except Exception as e:
            return False, f"❌ Ошибка: {e}"
    
    def delete_all_in_directory(self, dir_key: str) -> Tuple[int, str]:
        dir_path = self.directories.get(dir_key)
        if not dir_path or not os.path.exists(dir_path):
            return 0, "❌ Директория не найдена"
        
        count = 0
        for filename in os.listdir(dir_path):
            filepath = os.path.join(dir_path, filename)
            if os.path.isfile(filepath):
                try:
                    os.remove(filepath)
                    count += 1
                except:
                    pass
        
        return count, f"✅ Удалено {count} файлов из {dir_key}"
    
    def move_file(self, filepath: str, target_dir_key: str) -> Tuple[bool, str]:
        if not os.path.exists(filepath):
            return False, "❌ Файл не найден"
        
        target_dir = self.directories.get(target_dir_key)
        if not target_dir:
            return False, "❌ Целевая директория не найдена"
        
        try:
            filename = os.path.basename(filepath)
            target_path = os.path.join(target_dir, filename)
            
            if os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                target_path = os.path.join(target_dir, f"{name}_{timestamp}{ext}")
            
            shutil.move(filepath, target_path)
            return True, f"✅ Файл перемещен"
        except Exception as e:
            return False, f"❌ Ошибка: {e}"
    
    def copy_file(self, filepath: str, target_dir_key: str) -> Tuple[bool, str]:
        if not os.path.exists(filepath):
            return False, "❌ Файл не найден"
        
        target_dir = self.directories.get(target_dir_key)
        if not target_dir:
            return False, "❌ Целевая директория не найдена"
        
        try:
            filename = os.path.basename(filepath)
            target_path = os.path.join(target_dir, filename)
            
            if os.path.exists(target_path):
                name, ext = os.path.splitext(filename)
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                target_path = os.path.join(target_dir, f"{name}_{timestamp}{ext}")
            
            shutil.copy2(filepath, target_path)
            return True, f"✅ Файл скопирован"
        except Exception as e:
            return False, f"❌ Ошибка: {e}"
    
    def create_archive(self, dir_key: str, archive_name: str = None) -> Tuple[bool, str]:
        dir_path = self.directories.get(dir_key)
        if not dir_path or not os.path.exists(dir_path):
            return False, "❌ Директория не найдена"
        
        files = [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
        if not files:
            return False, f"❌ Нет файлов для архивации"
        
        if not archive_name:
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"{dir_key}_archive_{timestamp}.zip"
        
        archive_path = os.path.join(self.directories["archive"], archive_name)
        
        try:
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for filename in files:
                    filepath = os.path.join(dir_path, filename)
                    zipf.write(filepath, filename)
            return True, f"✅ Архив создан"
        except Exception as e:
            return False, f"❌ Ошибка: {e}"
    
    def search_files(self, query: str) -> List[Dict]:
        results = []
        for key, dir_path in self.directories.items():
            if not os.path.exists(dir_path):
                continue
            
            for filename in os.listdir(dir_path):
                if query.lower() in filename.lower():
                    filepath = os.path.join(dir_path, filename)
                    if os.path.isfile(filepath):
                        stat = os.stat(filepath)
                        results.append({
                            "name": filename,
                            "path": filepath,
                            "directory": key,
                            "size": stat.st_size,
                            "size_hr": self._human_readable_size(stat.st_size),
                            "modified": datetime.datetime.fromtimestamp(stat.st_mtime)
                        })
        return results
    
    def get_storage_summary(self) -> Dict:
        summary = {}
        total_size = 0
        total_files = 0
        
        for dir_key in self.directories.keys():
            info = self.get_directory_info(dir_key)
            summary[dir_key] = {
                "path": info.get("path", ""),
                "count": info.get("count", 0),
                "size": info.get("size", 0),
                "size_hr": info.get("size_hr", "0 B")
            }
            total_files += info.get("count", 0)
            total_size += info.get("size", 0)
        
        summary["total"] = {
            "count": total_files,
            "size": total_size,
            "size_hr": self._human_readable_size(total_size)
        }
        
        return summary