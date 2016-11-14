import argparse
import sys
import requests

from gevent import monkey
from gevent.pool import Pool

monkey.patch_all()

HTTP_VERBS = ["GET", "POST", "PUT", "DELETE", "HEAD"]


def benchmark(url, method='GET', concurrent=1, request_nums=1, options=None):
    if options is None:
        options = {}

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
    parser.add_argument('-m', '--method',
                        help='HTTP method used to request, support: {}'.format(','.join(HTTP_VERBS)),
                        default='GET')

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

    print(option)

    # print(benchmark(args.url, args.concurrency, args.requests))


if __name__ == "__main__":
    main()
