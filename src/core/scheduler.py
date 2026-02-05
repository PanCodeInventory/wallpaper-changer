"""
定时任务调度器
"""

import schedule
import time
from datetime import datetime
from typing import Callable, Optional


class WallpaperScheduler:
    """壁纸定时调度器"""

    def __init__(self):
        self.running = False
        self.update_callback: Optional[Callable] = None

    def set_update_callback(self, callback: Callable):
        """设置更新回调函数"""
        self.update_callback = callback

    def schedule_daily(self, time_str: str):
        """
        每天定时更新

        Args:
            time_str: 时间字符串，格式 "HH:MM"
        """
        schedule.clear()
        schedule.every().day.at(time_str).do(self._update)

        print(f"Scheduled daily update at {time_str}")

    def schedule_hourly(self, hours: int = 1):
        """
        每隔几小时更新

        Args:
            hours: 间隔小时数
        """
        schedule.clear()
        schedule.every(hours).hours.do(self._update)

        print(f"Scheduled update every {hours} hour(s)")

    def schedule_custom(self, cron_expr: str):
        """
        自定义 cron 表达式

        Args:
            cron_expr: cron 表达式
        """
        # 注意：schedule 库不支持完整的 cron 表达式
        # 这里简化处理，仅支持基本调度
        print(f"Custom scheduling not fully implemented: {cron_expr}")
        self.schedule_hourly(1)

    def _update(self):
        """执行更新"""
        if self.update_callback:
            print(f"Executing scheduled update at {datetime.now()}")
            try:
                self.update_callback()
            except Exception as e:
                print(f"Error in scheduled update: {e}")
        else:
            print("No update callback set")

    def start(self):
        """启动调度器"""
        if not self.running:
            self.running = True
            print("Scheduler started")

    def stop(self):
        """停止调度器"""
        self.running = False
        schedule.clear()
        print("Scheduler stopped")

    def run_once(self):
        """立即执行一次更新"""
        print("Running manual update")
        self._update()

    def run(self):
        """运行调度循环"""
        self.start()
        try:
            while self.running:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            self.stop()

    def get_next_run_time(self) -> Optional[datetime]:
        """获取下次运行时间"""
        next_job = schedule.next_run()
        return next_job if next_job else None

    def get_jobs(self) -> list:
        """获取所有任务"""
        return schedule.jobs
