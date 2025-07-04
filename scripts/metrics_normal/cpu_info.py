from psutil import cpu_count, cpu_percent


class CpuInfo:
    def __init__(self):
        self.__cpu_usage_total = cpu_percent(interval=0.1, percpu=False)
        self.__cpu_usage_each = cpu_percent(interval=0.2, percpu=True)

    def get_cpu_count_physical(self):
        return cpu_count(logical=False)

    def get_cpu_count_logical(self):
        return cpu_count(logical=True)

    def get_cpu_usage_total(self):
        return self.__cpu_usage_total

    def get_cpu_usage_each(self):
        return [(i, usage) for i, usage in enumerate(self.__cpu_usage_each, start=1)]
