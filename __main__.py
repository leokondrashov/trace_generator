import argparse
import logging
import os
import sys

from generate import generate


def run(args):
    if args.cmd == 'generate':
        inv_df, mem_df, run_df = generate(args)

    return

def check_values(args):
    if args.num_of_funcs < 1:
        raise ValueError("Minimum number of functions is 1.")
    
    if args.invocation_step < 1:
        raise ValueError("Minimum invocation step is 1.")
    
    if args.invocation_step > 500:
        logging.warning("Invocation step is greater than 500 (high invocation rate detected). Please verify that AWS concurrency limit is raised to at least 1,000.")
    
    if args.stagger_duration < 1:
        raise ValueError("Minimum stagger seconds is 1.")
    
    if args.stabilisation_count < 0:
        raise ValueError("Minimum stabilisation is 0.")
    
    if args.execution_duration <= 0:
        raise ValueError("Execution duration must be greater than 0.")
    
    if args.wait_duration < 0:
        raise ValueError("Minimum wait seconds is 0.")
    
    if args.memory < 128 or args.memory > 10_240:
        # AWS Limit: 128MB to 10,240MB (https://docs.aws.amazon.com/lambda/latest/operatorguide/computing-power.html)
        raise ValueError("Memory must be between 128MB and 10,240MB due to AWS limit.")
    
    if not os.path.exists(args.output_path):
        try:
            os.makedirs(args.output_path)
        except OSError as e:
            raise RuntimeError(f"Failed to create the output folder: {e}")

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="cmd")

    gen_parser = subparser.add_parser('generate')

    gen_parser.add_argument(
        '-f',
        '--functions',
        required=True,
        type=int,
        metavar='integer',
        help='Number of functions to be deployed',
        dest='num_of_funcs'
    )

    gen_parser.add_argument(
        '-i',
        '--invocation',
        required=True,
        type=int,
        metavar='integer',
        help='Invocation size for a time unit',
        dest='invocation_step'
    )

    gen_parser.add_argument(
        '-s',
        '--sustain',
        required=True,
        type=int,
        metavar='integer',
        help='Hold the target invocation rate for this period',
        dest='sustain'
    )

    gen_parser.add_argument(
        '-stag',
        '--stagger',
        required=False,
        type=int,
        default=5,
        metavar='integer',
        help='Time interval between invocations of different functions',
        dest='stagger_duration'
    )

    gen_parser.add_argument(
        '-p',
        '--proportion',
        required=False,
        type=float,
        default=0,
        metavar='float',
        help='Intermediate step value as a proportion of the invocation step, used with `stabilisation` and `wait`',
        dest='intermediate_step_proportion'
    )

    gen_parser.add_argument(
        '-stab',
        '--stabilisation',
        required=False,
        type=int,
        default=0,
        metavar='integer',
        help='Number of repetitions to stabilise the invocation pattern, used with `proportion` and `wait`',
        dest='stabilisation_count'
    )

    gen_parser.add_argument(
        '-w',
        '--wait',
        required=False,
        type=int,
        default=5,
        metavar='integer',
        help='Time interval between invocations of the same function, used with `proportion` and `stabilisation`',
        dest='wait_duration'
    )

    gen_parser.add_argument(
        '-e',
        '--execution',
        required=False,
        type=int,
        default=1000,
        metavar='integer',
        help='Execution time of the functions in ms',
        dest='execution_duration'
    )

    gen_parser.add_argument(
        '-m',
        '--memory',
        required=False,
        type=int,
        default=1024,
        metavar='integer',
        help='Memory usage of the functions in MB',
        dest='memory'
    )

    gen_parser.add_argument(
        '-o',
        '--output',
        required=True,
        type=str,
        metavar='path',
        help='Output path for the resulting trace',
        dest='output_path'
    )

    args = parser.parse_args()

    if not args.cmd:
        parser.print_help()
        return 1
    
    check_values(args)

    return run(args)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
