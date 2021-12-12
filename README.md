# LogMerger

A tool for merging jsonl log files by timestamp.

Example line of an expected log file:
```
{"timestamp": "2021-02-26 09:03:36", "log_level": "INFO", "message": "World!"}
```

## Usage:

```bash
~$ cd path-to/LogMerger
LogMerger $ python3 merge.py path/to/first/log/file.jsonl path/to/second/log/file.jsonl [-o path/to/output/file]
```
The path to the output file is optional, if is not given the output file will be
created directly in the LogMerger directory with the name "output_log.jsonl"
If the given output file name already exists it will be overwritten!

## Creating example log files:

```bash
~$ cd path-to/LogGenerator
LogGenerator $ python3 log_generator.py path/to/output/directory [-f | --force]
```
If the given directory already exists it will fail without an -f or --force flag
The size each of two created files is 1 Gb!

## Testing:

```bash
LogMerger $ python3 -m unittest test_module
```

Black linter was used
