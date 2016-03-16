#!/usr/bin/env python

# $ sudo easy_install pip
# $ sudo pip install ssdeep

import os
import sys
import time
import ssdeep
import hashlib
import argparse

ap = argparse.ArgumentParser(
	prog = 'Hasher',
	usage = '%(prog)s [-a [algorithm]] [-s (ssdeep)] (-f file | -d directory | -l list)',
	description = 'Welcome to Hasher\n',
	epilog = 'For more information about Hasher contact milicjx',
	formatter_class = argparse.ArgumentDefaultsHelpFormatter)

ap.add_argument('-a', nargs = '?', const = 'sha256', default = 'sha256', help = 'Specify cryptographic hash function.')
ap.add_argument('-s', nargs = '?', const = 'false', default = 'false', choices = ['true','false'], help = 'Return ssdeep CTPH (fuzzy hash) value.')

arg_group = ap.add_mutually_exclusive_group(required = True)

arg_group.add_argument('-f', help = 'Return hash value for a single file.')
arg_group.add_argument('-d', help = 'Return hash values for files within the directory.')
arg_group.add_argument('-l', help = 'Return hash values for files within the list.')

args = ap.parse_args()

BLOCKSIZE = 131072

hash_name = args.a
h = hashlib.new(hash_name)

def main():

	pathArray = []
	fileArray = []

	def file(inFile):

		with open(inFile, 'rb') as afile: #read file as binary via 'rb' to prevent corruption
			buffer = afile.read(BLOCKSIZE)
			while len(buffer) > 0:
				h.update(buffer)
				buffer = afile.read(BLOCKSIZE)

			if args.s == 'true':
				print 'ssdeep:\t' + ssdeep.hash_from_file(args.f);

		print args.a + ':\t' + h.hexdigest()

	def directory(inDir):

		dirPath = os.path.abspath(inDir)

		for (path, dirnames, filenames) in os.walk(dirPath):
			pathArray.extend(os.path.join(path, name) for name in filenames)

		bulk_hash(pathArray)

	def listing(inList):

		with open(inList, 'rb') as alist:

			for textline in alist:
				line = textline.rstrip("\n")
				if os.path.isfile(line):
					fileArray.append(os.path.abspath(line))

				if os.path.isdir(line):
					for (path, dirnames, filenames) in os.walk(line):
						fileArray.extend(os.path.join(path, name) for name in filenames)

			bulk_hash(fileArray)

	def bulk_hash(array = []):

		for path in array:
			with open(path, 'rb') as afile:
				buffer = afile.read(BLOCKSIZE)
				while len(buffer) > 0:
					h.update(buffer)
					buffer = afile.read(BLOCKSIZE)

				if args.s == 'true':
					print 'ssdeep:\t' + ssdeep.hash_from_file(p);

			print args.a + ':\t' + h.hexdigest()


	if args.f is not None:
		if os.path.isfile(args.f):
			file(args.f)
		else:
			print 'File does not exist'

	elif args.d is not None:
		if os.path.isdir(args.d):
			directory(args.d)
		else:
			print 'Directory does not exist'

	else:
		if os.path.isfile(args.l):
			listing(args.l)
		else:
			print 'Invalid input argument'

	time.sleep(1)
	#print 'Available cores: ' + str(multiprocessing.cpu_count())

if __name__ == '__main__':
	main()
