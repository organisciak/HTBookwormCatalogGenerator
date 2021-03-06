'''
Compare a sorted list of HT ids with lines in a sorted hathifile.

'''
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("hathifile", help="Sorted Hathifile",
			type=argparse.FileType('r'))
parser.add_argument("idlist", help="Sorted list of record ids to retrieve metadata for.",
			type=argparse.FileType('r'))
args = parser.parse_args()

logging.basicConfig(filename="select.log", level=logging.INFO)

count = 0
stripchars = ".:/,$"
for match in args.idlist:
    match = match.strip().translate(None, stripchars)
    logging.debug("Setting match as %s" % match)
    if len(match) == 0:
        continue
    while True:
        htline = args.hathifile.readline().strip()
        l = htline.translate(None, stripchars)
        if not l:
            break
        compare = l[:len(match)]

        count += 1
        if count % 100000 == 0:
            logging.info("%d Hathilines read, current match is %s, current hathiline is %s" % (count, match, compare))
        if match > compare:
            continue
        elif l.startswith(match):
            print htline
            break
        else:
            logging.error("Somehow we missing %s in the Hathifile." % match)
            break

