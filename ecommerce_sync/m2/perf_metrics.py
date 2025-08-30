import numpy as np
import time

class PerfMetrics:
    def __init__(self, name="Module"):
        self.name = name
        self.times = []

    def record(self, start, end):
        self.times.append(end - start)

    def summary(self):
        if not self.times:
            return f"{self.name}: no data"
        arr = np.array(self.times)
        avg = np.mean(arr)
        p95 = np.percentile(arr, 95)
        p99 = np.percentile(arr, 99)
        return (
            f"\n===== {self.name} 模块延迟统计 =====\n"
            f"请求数: {len(arr)}\n"
            f"平均: {avg:.3f}s\n"
            f"P95 : {p95:.3f}s\n"
            f"P99 : {p99:.3f}s\n"
        )
