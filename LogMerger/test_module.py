import unittest
import os
from pathlib import Path
from time import sleep
from datetime import datetime
from random import randint, random, shuffle
import shutil
import merge


class TestLogMerger(unittest.TestCase):

    _working_dir = Path(r'./TestLogDir')
    _full_log_path = Path(r'./TestLogDir/log_full.jsonl')
    _log_a_path = Path(r'./TestLogDir/log_a.jsonl')
    _log_b_path = Path(r'./TestLogDir/log_b.jsonl')
    _output_log_path = Path(r"./TestLogDir/log_c.jsonl")

    def setUp(self):
        '''
        Creates testing environment, such as jsonl log files
        '''
        levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR']
        messages = [
            'Leela created a man in L.A. tomorrow',
            'Amy played a fish at park yesterday',
            'Dr. Zoidberg killed a man on the Mars day after tomorrow',
            'Fry saw a fish at park day before yesterday',
            'Bender took a bottle of bear at park day after tomorrow',
        ]

        os.mkdir(self._working_dir)
        with open(self._full_log_path, "w") as log:
            print('Creating testing environment...\nIt may take up to 3 min...'')
            for i in range(50):
                level = levels[randint(0, 3)]
                message = messages[randint(0, 4)]
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                line = (
                    '{'
                    + f"'log_level': '{level}', 'timestamp': '{timestamp}', \
                    'message': '{message}'"
                    + '}\n'
                )
                log.write(line)
                # In testing purpose to avoid identical timestamps not to shuffle lines
                sleep(random() * randint(1, 2) + 1)

        with open(self._full_log_path) as full_log:
            log_a = open(self._log_a_path, 'w')
            log_b = open(self._log_b_path, 'w')
            log_file_list = [log_a, log_b, log_a, log_b, log_a]

            for line in full_log:
                log_file_list[0].write(line)
                shuffle(log_file_list)

            log_a.close()
            log_b.close()

    def tearDown(self):
        '''
        Destroys the testing environment
        '''
        shutil.rmtree(self._working_dir)
        print('Testing environment is destroyed')

    def test_merge(self):
        '''
        Checks merging jsonl log files by timestamp
        '''

        merge._merge_log_files(
            self._log_a_path, self._log_b_path, self._output_log_path
        )

        with open(self._full_log_path) as full_log_file:
            full_log = full_log_file.read()

        with open(self._output_log_path) as output_log_file:
            output_log = output_log_file.read()

        self.assertEqual(output_log, full_log)
