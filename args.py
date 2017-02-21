import argparse

def parse_args():
    arg_parser = argparse.ArgumentParser()

    # Help messages for each option
    helps = {}
    helps['data'] = 'Data to calculate. [Default: ncku]'
    helps['file'] = 'Full path of data file.'
    helps['number'] = 'Enter location number.'
    helps['time'] = 'Enter time limitation.'

    arg_parser.add_argument(
        '-d', '--data', 
        choices=['nctu', 'nthu', 'thu', 'ncku', 'demo'],
        default='ncku',
        help=helps['data']
    ) 

    arg_parser.add_argument(
        '-f', '--file',
        help=helps['file'],
        metavar='FULL_FILE_PATH'
    )

    arg_parser.add_argument(
        '-n', '--number',
        help=helps['number'],
        default='3',
        dest='number'
    )
    
    arg_parser.add_argument(
        '-t', '--time',
        help=helps['time'],
        default='10',
        dest='time'
    )
    return arg_parser.parse_args()
