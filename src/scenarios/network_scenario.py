#!/usr/bin/env python3
"""
Сценарий имитации сетевых загрузок.
"""

import time
import random
from tqdm import tqdm
from typing import Dict, Any, List, Tuple

from src.scenarios.base_scenario import BaseScenario
from src.utils.console import Colors, Style

class NetworkDownloadScenario(BaseScenario):
    
    def __init__(self):
        super().__init__(
            "Сетевые загрузки",
            "Демонстрация вложенных прогресс-баров"
        )
        
        self.files_to_download = [
            {"name": "document.pdf", "size": random.randint(100, 500)},
            {"name": "image.jpg", "size": random.randint(50, 200)},
            {"name": "video.mp4", "size": random.randint(1000, 5000)},
            {"name": "archive.zip", "size": random.randint(500, 2000)},
            {"name": "music.mp3", "size": random.randint(30, 100)},
        ]
    
    def simulate_chunk_download(self, chunk_size: int) -> float:
        speed = random.uniform(50, 200)
        time.sleep(chunk_size / speed)
        return speed
    
    def download_file(self, file_info: Dict[str, Any], 
                     overall_progress: tqdm) -> Tuple[bool, float]:
        
        file_name = file_info["name"]
        file_size = file_info["size"]
        chunk_size = 50
        chunks = (file_size + chunk_size - 1) // chunk_size
        speeds = []
        
        with tqdm(
            total=file_size,
            desc=f"  Загрузка {file_name}",
            unit="KB",
            unit_scale=True,
            leave=False,
            position=1,
            colour="blue"
        ) as file_progress:
            
            for chunk in range(chunks):
                current_chunk_size = min(chunk_size, file_size - chunk * chunk_size)
                speed = self.simulate_chunk_download(current_chunk_size)
                speeds.append(speed)
                
                file_progress.update(current_chunk_size)
                overall_progress.update(current_chunk_size)
                
                avg_speed = sum(speeds[-5:]) / len(speeds[-5:])
                file_progress.set_postfix(
                    скорость=f"{avg_speed:.1f} KB/s",
                    чанк=f"{chunk+1}/{chunks}"
                )
        
        return True, sum(speeds) / len(speeds)
    
    def run(self) -> Dict[str, Any]:
        with self:
            total_size = sum(f["size"] for f in self.files_to_download)
            
            print(f"Всего файлов: {len(self.files_to_download)}")
            print(f"Общий размер: {total_size} KB ({total_size/1024:.2f} MB)\n")
            
            download_results = []
            
            with tqdm(
                total=total_size,
                desc="Общий прогресс",
                unit="KB",
                unit_scale=True,
                colour="cyan",
                position=0
            ) as overall_progress:
                
                for file_info in self.files_to_download:
                    success, avg_speed = self.download_file(file_info, overall_progress)
                    
                    if success:
                        download_results.append({
                            "name": file_info["name"],
                            "size": file_info["size"],
                            "speed": avg_speed
                        })
                    
                    time.sleep(0.5)
            
            print(f"\n{Colors.GREEN}Загрузка завершена{Style.RESET_ALL}")
            
            return {
                "total_files": len(self.files_to_download),
                "total_size_kb": total_size,
                "successful": len(download_results)
            }