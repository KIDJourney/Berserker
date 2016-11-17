from __future__ import division
import sys
import os
from collections import defaultdict


class ProcessBar:
    """Process Bar
    show the request percent of benchmark
    """

    def __init__(self, goal, fill='=', blank='-', output_format='[{}>{}] {:.0f}%'):
        self.goal = goal
        self.current = 0
        self.fill = fill
        self.blank = blank
        self.format = output_format

    def _current_process(self):
        return self.current / self.goal

    def _finished(self):
        return int(self._current_process() * self.get_width())

    def _blanked(self):
        return self.get_width() - self._finished()

    def get_width(self):
        if hasattr(sys.stdout, 'istty') and sys.stdout.istty():
            return int(os.popen('stty size', 'r').read().split()[1])
        else:
            return 30

    def get_step(self):
        return self.goal // self.get_width()

    def show(self):
        sys.stdout.write('\r')
        output = self.format.format(self._finished() * self.fill, self._blanked() * self.blank,
                                    self._current_process() * 100)
        sys.stdout.write(output)
        sys.stdout.flush()

    def incr(self):
        """
        add current counter and show process.
        :return:
        """
        self.current = min(self.goal, self.current + 1)
        self.show()


class Results:
    """
    Class used to store, calculate, and display benchmark result
    """

    def __init__(self, concurrency, nums):
        """
        Init
        :param concurrency: concurrency nums
        :param nums: request nums
        :return:
        """
        self.status_counter = defaultdict(list)
        self.errors = []
        self.responses = []

        self.total_request = nums
        self.concurrency = concurrency
        self.process_bar = ProcessBar(nums)
        self.total_time = None
        self.html_transferred = 0

    def add_error_record(self, exc):
        self.errors.append(exc)
        self.incr()

    def add_status_record(self, response, duration):
        self.responses.append(response)
        self.status_counter[response.status_code].append(duration)
        self.html_transferred += len(response.content)
        self.incr()

    def set_total_time(self, total_time):
        self.total_time = total_time

    def incr(self):
        self.process_bar.incr()

    def cal_status(self):
        """
        generate statistical data of benchmark result
        :return: result dict
        """
        result = {}

        result['concurrency'] = self.concurrency
        result['request_nums'] = self.total_request
        result['time_taken_for_tests'] = self.total_time
        result['complete_requests'] = sum(map(len, self.status_counter.values()))
        result['failed_requests'] = len(self.errors)
        result['html_transferred'] = self.html_transferred
        result['request_per_second'] = self.total_request / self.total_time
        result['time_per_request'] = self.total_time / self.total_request
        result['transfer_rate'] = self.html_transferred / self.total_time / 1024

        request_durations = [duration for status_code, duration_list in self.status_counter.items() for duration in
                             duration_list]
        request_durations.sort()

        result['duration_distribution'] = request_durations

        return result

    def show(self):
        """
        display benchmark statistical data
        :return:
        """
        result = self.cal_status()
        output = """

Concurrency Level:      {concurrency}
Request Level:          {request_nums}
Time taken for tests:   {time_taken_for_tests:.2f} seconds
Complete requests:      {complete_requests}
Failed requests:        {failed_requests}
HTML transferred:       {html_transferred} bytes
Requests per second:    {request_per_second:.2f} [#/sec] (mean)
Time per request:       {time_per_request:.2f} [ms] (mean)
Transfer rate:          {transfer_rate:.2f} [Kbytes/sec] received
""".format(**result)
        output += """
Percentage of the requests served within a certain time (ms)
"""

        duration_d = result['duration_distribution']
        start = max(11 - len(duration_d), 6)
        show_percent = [i / 10 for i in range(start, 11)]

        for percent in show_percent:
            index = min(int(len(duration_d) * percent), len(duration_d) - 1)
            output += "{}% \t {:.2f}\n".format(int(percent * 100), duration_d[index] * 1000)

        print(output)


if __name__ == "__main__":
    import time

    pb = ProcessBar(1)
    for i in range(10):
        time.sleep(0.01)
        pb.incr()
