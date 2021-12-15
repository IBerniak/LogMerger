import heapq
import log_iterator
import argparse
import time
from datetime import datetime
from pathlib import Path
from typing import Iterable, Generator, Any


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge log files.')

    parser.add_argument(
        'path_to_log_file_1',
        metavar='<PATH TO LOG FILE 1>',
        type=str,
        help='path to log file 1',
    )

    parser.add_argument(
        'path_to_log_file_2',
        metavar='<PATH TO LOG FILE 2>',
        type=str,
        help='path to log file 2',
    )

    parser.add_argument(
        '-o',
        action='store',
        metavar='<PATH TO OUTPUT LOG FILE>',
        dest='path_to_output_file',
        help='specify output path',
    )

    return parser.parse_args()


def _merge_iterables(
    iterable_1: Iterable, iterable_2: Iterable
) -> Generator[Any, None, None]:
    '''
    Util generator function for merging do ordered iterables.
    Elements of iterables should be comparable!
    '''

    iterator_1 = iter(iterable_1)
    iterator_2 = iter(iterable_2)
    item_1 = next(iterator_1, None)
    item_2 = next(iterator_2, None)

    while item_1 is not None or item_2 is not None:
        if item_1 is None or (item_2 is not None and item_1 > item_2):
            yield item_2
            item_2 = next(iterator_2, None)
        else:
            yield item_1
            item_1 = next(iterator_1, None)

    return None


def _merge_log_files(
    path_to_file_1: Path, path_to_file_2: Path, output_path: Path
) -> None:
    '''
    Merges two log's files into one sorting by timestamp.
    Expected log file format is:
    {'log_level': 'smth', 'timestamp': '\d\d\d\d-\d\d?-\d\d? \d\d?:\d\d:\d\d',
    'message': 'some text here'}

    Params:
     path_to_file_1:
     path_to_file_2:
     output_path:

    Returns: None
    '''
    filename_1 = path_to_file_1.name
    filename_2 = path_to_file_2.name

    log_1 = log_iterator.LogFileIterator(path_to_file_1)
    log_1.open()
    log_2 = open(path_to_file_2)

    with open(output_path, 'w') as output:

        print(
            f'\nMerging {filename_1} and {filename_2} is started at',
            datetime.now().strftime('%H:%M:%S'),
        )

        for line in _merge_iterables(log_1, log_2):
            output.write(line)

        log_1.close()
        log_2.close()


def main() -> None:
    args = _parse_args()

    t0 = time.time()

    path_to_file_1 = Path(args.path_to_log_file_1)
    path_to_file_2 = Path(args.path_to_log_file_2)

    if args.path_to_output_file:
        output_path = Path(args.path_to_output_file)
    else:
        output_path = Path('./output_log.jsonl')

    try:
        _merge_log_files(path_to_file_1, path_to_file_2, output_path)
        print(f'Finished in {time.time() - t0:0f} sec')

    except FileNotFoundError:
        print('Invalid path(s)! Put valid paths to files and try again')

    except TypeError:
        print(
            'Invalid log record format!',
            'Each line of log file should contain a timestamp in the format',
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        )


if __name__ == '__main__':
    main()
