# dateUtils.py


from datetime import timedelta


class DateUtils:
    @staticmethod
    def days_to_seconds(days: int):
        return int(timedelta(days=days).total_seconds())

    @staticmethod
    def seconds_to_minutes(seconds: int):
        return int(seconds / 60)
