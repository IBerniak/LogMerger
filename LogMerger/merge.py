import heapq
import log_iterator
import argparse
import time
from datetime import datetime
from pathlib import Path


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

    with open(output_path, 'w') as output:
        log_1 = log_iterator.LogFileIterator(path_to_file_1)
        log_1.open()
        log_2 = open(path_to_file_2)

        print(
            f'\nMerging {filename_1} and {filename_2} is started at {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
        )
        for line in heapq.merge(log_1, log_2):
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

    _merge_log_files(path_to_file_1, path_to_file_2, output_path)

    print(f'Finished in {time.time() - t0:0f} sec')


if __name__ == '__main__':
    main()
