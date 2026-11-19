try:
    import psutil

    def get_metrics():
        return {
            "cpu": psutil.cpu_percent(),
            "memory": psutil.virtual_memory().percent,
        }

except ImportError:
    def get_metrics():
        return {
            "cpu": 0.0,
            "memory": 0.0,
        }