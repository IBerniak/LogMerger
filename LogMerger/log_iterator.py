'''
Provides tools to iterate through jsonl log file and sort it by timestamp
'''
import re


class LineRepresentation(str):
    '''
    String child class with a changed behavior of a comparison
    Instances of this class compares by expected timestamp pattern
    '''

    _pattern = r'\d\d\d\d-(\d\d|\d)-(\d\d|\d) (\d|\d\d):\d\d:\d\d'

    def __gt__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            > re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False

    def __ge__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            >= re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False

    def __lt__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            < re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False

    def __le__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            <= re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False

    def __eq__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            == re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False

    def __ne__(self, other):
        if (
            re.search(self._pattern, self.__str__())[0]
            != re.search(self._pattern, other.__str__())[0]
        ):
            return True
        else:
            return False


class LogFileIterator:
    '''
    Provides open, close and iter methods.
    Iter method yields instances of LineRepresentation class to define
    a behavior for the correct comparing
    '''

    def __init__(self, path_to_file):
        self._path = path_to_file

    def open(self):
        self._file = open(self._path)

    def close(self):
        self._file.close()

    def __iter__(self):
        for line in self._file:
            yield LineRepresentation(line)
