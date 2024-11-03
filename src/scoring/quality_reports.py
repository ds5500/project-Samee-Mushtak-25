import mos
import sop
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d', '--directory', help='Species directory containing all algorithm outputs')
args = parser.parse_args()

if not args.directory:
    raise RuntimeError("Directory is required")

print("SOP REPORT:")
sop.sop_report(glob.iglob(args.directory + '/*/*.clustal*'))
print("-------------------------------------------------------")
print("MOS REPORT:")
mos.mos_report(glob.iglob(args.directory + '/*/*.clustal*'))