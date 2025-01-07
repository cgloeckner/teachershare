import os
import pathlib
import sys

from teachershare import run, get_students


def main() -> None:
    root = pathlib.Path(os.environ['HOME']) / 'media' / 'Students-Home'

    if len(sys.argv) > 1:
        # custom path
        root = pathlib.Path(sys.argv[1])
        print(f'Using custom root: {root}')
    
    student_homes = get_students(root)
    run(student_homes)


if __name__ == '__main__':
    main()
