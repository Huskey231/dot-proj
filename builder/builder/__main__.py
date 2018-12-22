import os
import sys
from builder.build import make


def main():
    env = os.environ.get('DOT_PROJ_BUILD', '')
    print(make(env))
    return 0


if __name__ == '__main__':
    sys.exit(main())
