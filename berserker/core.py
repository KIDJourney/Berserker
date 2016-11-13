import argparse


def main():
    parser = argparse.ArgumentParser(description="Web Application Smoking Test. ")

    parser.add_argument('url',
                        help='Url to test.')
    parser.add_argument('-c', '--concurrent',
                        help='numbers of concurrent.')
    parser.add_argument('-n', '--requests',
                        help='numbers of request')

    args = parser.parse_args()

    print(args.url)


if __name__ == "__main__":
    main()