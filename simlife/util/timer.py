class Timer:
    def __init__(self, delay):
        self.__delay = delay
        self.__elapsed_seconds = 0

    def tick(self, elapsed_seconds):
        self.__elapsed_seconds += elapsed_seconds
        if self.__elapsed_seconds >= self.__delay:
            self.__elapsed_seconds -= self.__delay
            return True
        else:
            return False
