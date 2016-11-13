import argparse
import sys
import requests

from gevent import monkey
from gevent.pool import Pool

monkey.patch_all()


def benchmark(url, concurrent, request_nums):
    pool = Pool(concurrent)
    result = []
    jobs = [pool.spawn(lambda goal, result: result.append(requests.get(goal)), url, result) for _ in
            range(request_nums)]
    pool.join()

    return result


def main():
    parser = argparse.ArgumentParser(description="Web Application Smoking Test. ")

    parser.add_argument('url',
                        help='Url to test.', nargs='?')
    parser.add_argument('-c', '--concurrency',
                        help='numbers of concurrent.', type=int, default=1)
    parser.add_argument('-n', '--requests',
                        help='numbers of requests.', type=int, default=1)
    parser.add_argument('-H', '--custom-header',
                        help='Add custom headers to every requests, format: key:value',
                        nargs='+')
    parser.add_argument('-C', '--custom-cookie',
                        help='Add custom cookies to every requests, format: key:value',
                        nargs='+')

    args = parser.parse_args()

    if args.url is None:
        parser.print_usage()
        sys.exit(0)

    print(args.custom_header)

    # print(benchmark(args.url, args.concurrency, args.requests))


if __name__ == "__main__":
    main()
