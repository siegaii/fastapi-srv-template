"""雪花ID生成器模块"""

import time
import threading
from typing import Optional


class SnowflakeGenerator:
    """雪花ID生成器
    
    雪花ID结构（64位）：
    - 1位符号位（固定为0）
    - 41位时间戳（毫秒级，可使用约69年）
    - 10位机器ID（支持1024台机器）
    - 12位序列号（每毫秒可生成4096个ID）
    """
    
    def __init__(self, machine_id: int = 1, epoch: int = 1640995200000):
        """
        初始化雪花ID生成器
        
        Args:
            machine_id: 机器ID，范围0-1023
            epoch: 起始时间戳（毫秒），默认为2022-01-01 00:00:00 UTC
        """
        if machine_id < 0 or machine_id > 1023:
            raise ValueError("机器ID必须在0-1023范围内")
            
        self.machine_id = machine_id
        self.epoch = epoch
        self.sequence = 0
        self.last_timestamp = -1
        self.lock = threading.Lock()
        
        # 位移量
        self.machine_id_shift = 12
        self.timestamp_shift = 22
        
        # 最大值
        self.max_sequence = 4095  # 2^12 - 1
        
    def _get_timestamp(self) -> int:
        """获取当前时间戳（毫秒）"""
        return int(time.time() * 1000)
        
    def _wait_next_millis(self, last_timestamp: int) -> int:
        """等待下一毫秒"""
        timestamp = self._get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._get_timestamp()
        return timestamp
        
    def generate(self) -> int:
        """生成雪花ID"""
        with self.lock:
            timestamp = self._get_timestamp()
            
            # 时钟回拨检查
            if timestamp < self.last_timestamp:
                raise RuntimeError(f"时钟回拨检测到，拒绝生成ID。当前时间戳: {timestamp}, 上次时间戳: {self.last_timestamp}")
                
            # 同一毫秒内
            if timestamp == self.last_timestamp:
                self.sequence = (self.sequence + 1) & self.max_sequence
                if self.sequence == 0:
                    # 序列号用完，等待下一毫秒
                    timestamp = self._wait_next_millis(self.last_timestamp)
            else:
                # 新的毫秒，重置序列号
                self.sequence = 0
                
            self.last_timestamp = timestamp
            
            # 生成雪花ID
            snowflake_id = (
                ((timestamp - self.epoch) << self.timestamp_shift) |
                (self.machine_id << self.machine_id_shift) |
                self.sequence
            )
            
            return snowflake_id
            
    def parse(self, snowflake_id: int) -> dict:
        """解析雪花ID
        
        Args:
            snowflake_id: 雪花ID
            
        Returns:
            包含时间戳、机器ID、序列号的字典
        """
        timestamp = ((snowflake_id >> self.timestamp_shift) + self.epoch)
        machine_id = (snowflake_id >> self.machine_id_shift) & 1023
        sequence = snowflake_id & self.max_sequence
        
        return {
            'timestamp': timestamp,
            'machine_id': machine_id,
            'sequence': sequence,
            'datetime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp / 1000))
        }


# 全局雪花ID生成器实例
snowflake_generator = SnowflakeGenerator(machine_id=1)