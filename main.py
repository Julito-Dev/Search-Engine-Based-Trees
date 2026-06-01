import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), 'repl'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'model'))

from repl.REPL import REPL
if __name__ == "__main__":
    REPL().run()