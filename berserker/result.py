import sys
import os
from collections import defaultdict


class ProcessBar:
    def __init__(self, goal, fill='=', blank='-', output_format='[{}>{}] {}%'):
        self.goal = goal
        self.current = 0
        self.fill = fill
        self.blank = blank
        self.format = output_format

    def _current_process(self):
        return 100 * self.current // self.goal

    def _finished(self):
        return self._current_process() * self.get_width() * self.fill

    def _blanked(self):
        return (100 - self._current_process()) * self.get_width() * self.blank

    def get_width(self):
        return int(os.popen('stty size', 'r').read().split()[1]) // 200

    def show(self):
        sys.stdout.write('\r')
        output = self.format.format(self._finished(), self._blanked(), self._current_process())
        sys.stdout.write(output)
        sys.stdout.flush()

    def inc(self):
        self.current = min(self.goal, self.current + 1)
        self.show()


class Results:
    def __int__(self, nums):
        self.status_counter = defaultdict(list)
        self.errors = []
        self.total_time = None
        self.process_bar = ProcessBar(nums)

    def add_error_record(self):


if __name__ == "__main__":
    import time

    pb = ProcessBar(200)
    for i in range(200):
        time.sleep(0.01)
        pb.inc()
