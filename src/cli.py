import argparse
from .recorder import ExportMethod
arg = argparse.ArgumentParser(
    prog='timelesschesses',
    description='A chess replay renderer using Pygame and Python',
)

arg.add_argument(
    "--res","-res", default=700, nargs="?", help="resolution of the window (defaults to 700x700) also you can't config both x and y",action="store", type=int
)
arg.add_argument(
    "--putframes", "-pf", default="disk", nargs="?", help="where to put the frames (defaults to disk)",action="store", type=str, choices=["disk", "memory"]
)
arg.add_argument(
    "--output", "-o", default="output.avi", nargs="?", help="output file (defaults to output.avi)",action="store", type=str
)
arg.add_argument(
    "-fps","--fps", default=60, nargs="?", help="frames per second (defaults to 60)",action="store", type=int
)

arg.add_argument(
    "-pgn","--pgn", help="pgn file or pgn string, if pgn is stdin then it will read stdin until terminated by either ctrl-z or ctrl-d",action="store", type=str, default="stdin", required=True
)

b = arg.parse_args()

if b.putframes == "disk":
    method = ExportMethod.disk
elif b.putframes == "memory":
    method = ExportMethod.memory
else:
    assert False, "This should never happen"
    
import sys
from .game import main
import os

if b.pgn == "stdin":
    pgn = sys.stdin.read()
elif os.path.exists(b.pgn):
    with open(b.pgn, "r") as fp:
        pgn = fp.read()
else:
    pgn = b.pgn
main(
    res=(b.res, b.res),
    fps=b.fps,
    pgn=pgn,
    method = method,
    output=b.output
)
