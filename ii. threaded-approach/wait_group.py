from threading import Condition


class WaitGroup:

    wait_count = 0
    cv = Condition()

    # @classmethod
    def protect(func):
        def wrapper(self, *args, **kwargs):
            self.cv.acquire()
            func(self, *args, **kwargs)
            self.cv.release()
        return wrapper

    @protect
    def add(self, count):
        self.wait_count += count

    @protect
    def done(self):
        if self.wait_count > 0:
            self.wait_count -= 1
        if self.wait_count == 0:
            self.cv.notify_all()

    @protect
    def wait(self):
        while self.wait_count > 0:
            self.cv.wait()