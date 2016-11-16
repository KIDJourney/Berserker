import argparse
import sys
import requests
import time

from gevent import monkey
from gevent.pool import Pool
from berserker.result import Results
from berserker.helper import show_host_info, show_intro, check_url

monkey.patch_all()

HTTP_VERBS = ["GET", "POST", "PUT", "DELETE", "HEAD"]


def make_request(url, method, result, options):
    """request make wrapper
    accept request options and make request.
    call result.incr for every request.
    :param url: url to request
    :param method: http method from request module
    :param result: Result object
    :param options: request options
    :return: None
    """
    start = time.time()
    try:
        response = method(url, **options)
    except requests.RequestException as exc:
        result.add_error_record(exc)
    else:
        duration = time.time() - start
        result.add_status_record(response, duration)
    finally:
        # result trigger
        result.incr()


def benchmark(url, concurrent=1, request_nums=1, method='GET', options=None):
    """main process of benchmark
    Initialize gevent pool and result, run benchmark
    :param url: url to request
    :param concurrent: gevent concurrent nums
    :param request_nums: total request nums
    :param method: HTTP method
    :param options: http related option
    :return: Result object
    """
    if options is None:
        options = {}

    start_time = time.time()

    pool = Pool(concurrent)
    request_method = getattr(requests, method.lower())
    result = Results(concurrent, request_nums)

    try:
        jobs = [pool.spawn(make_request, url, request_method, result, options) for _ in range(request_nums)]
        pool.join()
    except KeyboardInterrupt:
        pass

    total_time = time.time() - start_time

    result.set_total_time(total_time)

    return result


def main():
    """entry point
    Accept cli arguments and do arguments check, then run benchmark
    :return:
    """
    parser = argparse.ArgumentParser(description="Web Application Smoking Test.")

    parser.add_argument('url',
                        help='Url to test.', nargs='?')
    parser.add_argument('-c', '--concurrency',
                        help='numbers of concurrent.', type=int, default=1)
    parser.add_argument('-n', '--requests',
                        help='numbers of requests.', type=int, default=1)
    parser.add_argument('-m', '--method',
                        help='HTTP method used to request, support: {}.'.format(','.join(HTTP_VERBS)),
                        default='GET')

    parser.add_argument('-H', '--custom-header',
                        help='Add custom headers to every requests, format: key:value.',
                        nargs='+')
    parser.add_argument('-C', '--custom-cookie',
                        help='Add custom cookies to every requests, format: key:value.',
                        nargs='+')

    args = parser.parse_args()

    if args.url is None:
        parser.print_usage()
        sys.exit(0)

    option = {}

    def _split(kv_dicts, kv_type):
        kv_dict = {}
        for kv in kv_dicts:
            _kv = kv.split(':')
            if len(_kv) != 2:
                print("{} is not valid {}, {} must be in key:value format.".format(kv, kv_type, kv_type))
                parser.print_usage()
                sys.exit(0)
            kv_dict.update({_kv[0]: _kv[1]})
        return kv_dicts

    if args.custom_header is not None:
        option['headers'] = _split(args.custom_header, 'header')

    if args.custom_cookie is not None:
        option['cookies'] = _split(args.custom_cookie, 'cookie')

    if not check_url(args.url):
        print("{} is not a valid url.".format(args.url))
        parser.print_usage()
        sys.exit(1)

    show_intro()
    show_host_info(args.url)
    benchmark_result = benchmark(url=args.url, concurrent=args.concurrency, request_nums=args.requests, options=option)
    benchmark_result.show()

    sys.exit(0)


if __name__ == "__main__":
    main()
