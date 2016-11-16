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

    def incr(self):
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
        self.incr()

    def set_total_time(self, total_time):
        self.total_time = total_time

    def parse_response(self, response):
        self.html_transferred += len(response.content)

    def incr(self):
        self.process_bar.incr()

    def cal_status(self):
        result = {}

        result['concurrency'] = self.concurrency
        result['time_taken_for_tests'] = self.total_time
        result['complete_requests'] = sum(map(len, self.status_counter.values()))
        result['failed_requests'] = len(self.errors)
        result['html_transferred'] = self.html_transferred
        result['request_per_second'] = self.total_request / self.total_time
        result['time_per_request'] = result['complete_requests'] / self.total_time
        result['transfer_rate'] = self.html_transferred / self.total_time / 1024

        request_durations = [duration for status_code, duration_list in self.status_counter.items() for duration in
                             duration_list]
        request_durations.sort()
        mid = len(request_durations) // 2
        end = len(request_durations)
        step = max(len(request_durations) // 10, 1)
        precent_value = request_durations[mid:end:step][:-1] + [request_durations[-1]]

        result['duration_distribution'] = precent_value

        return result

    def show(self):
        result = self.cal_status()
        output = """
Concurrency Level:      {concurrency}
Time taken for tests:   {time_taken_for_tests} seconds
Complete requests:      {complete_requests}
Failed requests:        {failed_requests}
HTML transferred:       {html_transferred} bytes
Requests per second:    {request_per_second} [#/sec] (mean)
Time per request:       {time_per_request} [ms] (mean)
Transfer rate:          {transfer_rate} [Kbytes/sec] received
""".format(**result)
        output += """
Percentage of the requests served within a certain time (ms)
"""
        for index, value in enumerate(result['duration_distribution']):
            output += '{}% {} ms\n'.format(50 + 10 * index, value)


if __name__ == "__main__":
    import time

    pb = ProcessBar(200)
    for i in range(200):
        time.sleep(0.01)
        pb.incr()
