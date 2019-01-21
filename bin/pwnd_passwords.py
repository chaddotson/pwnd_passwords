from argparse import ArgumentParser
from hashlib import sha1
import requests
from termgraph.termgraph import chart
from tqdm import tqdm


PWND_PASSWORDS_GET_URL = 'https://api.pwnedpasswords.com/range/{hash}'


def parse_args():
    """Parse command line arguments"""
    parser = ArgumentParser(description='Display password count from pwnedpasswords.comr')
    parser.add_argument('passwords', help='CSV list of passwords to test.', nargs='+', type=str)
    parser.add_argument('-f', '--format', help='Format, if raw specified.', type=str,
                        default='{password} - {count}')
    parser.add_argument('-r', '--raw', help='Display raw results', default=False, action='store_true')
    parser.add_argument('-v', '--verbose', help='Verbose logs', default=False, action='store_true')
    return parser.parse_args()


def get_all_pwns(passwords):
    results = {}
    for password in tqdm(passwords):
        results[password] = get_pwns(password)
    return results


def get_pwns(password):
    hash = sha1(password.encode()).hexdigest().upper()

    submit_hash, verify_hash = hash[:5], hash[5:]

    response = requests.get(
        url=PWND_PASSWORDS_GET_URL.format(hash=submit_hash)
    )

    # be lazy if failed to get pwns
    if not response.ok:
        return -1

    possible_matches = dict(map(lambda entry: entry.split(':'), response.text.split()))

    if verify_hash in possible_matches:
        return int(possible_matches[verify_hash])
    else:
        return 0


def make_chart(data):
    graph_args = {
        'stacked': False, 'width': 50, 'no_labels': False, 'format': '{}',
        'suffix': '', "vertical": False, 'different_scale': False
    }
    chart(colors=[], data=[*map(lambda item: [item], [*data.values()])], args=graph_args, labels=[*data.keys()])


def display_raw_data(data, fmt):
    for password, count in data.items():
        print(fmt.format(**locals()))


def cli():
    args = parse_args()

    print('Retrieving Pwnage:')
    results = get_all_pwns(args.passwords)

    print(flush=True)
    print('Results:')

    if args.raw:
        display_raw_data(results, args.format)
    else:
        make_chart(results)


if __name__ == '__main__':
    cli()
