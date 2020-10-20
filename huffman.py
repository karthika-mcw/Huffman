#!/usr/local/bin/python3
import sys
import argparse
import shutil
from collections import OrderedDict

binary_code = { '\n' : "", '\t' : "", '/' : "", 'A' : "", 'B' : "", 'C' : "", 'D' : "", 'E' : "", 'F' : "", 'G' : "", 'H' : "", 'I' : "", 'J' : "", 'K' : "", 'L' : "", 'M' : "", 'N' : "", 'O' : "", 'P' : "", 'Q' : "", 'R' : "", 'S' : "", 'T' : "", 'U' : "", 'V' : "", 'W' : "", 'X' : "", 'Y' : "", 'Z' : "", 'a' : "", 'b' : "", 'c' : "", 'd' : "", 'e' : "", 'f' : "", 'g' : "", 'h' : "", 'i' : "", 'j' : "", 'k' : "", 'l' : "", 'm' : "", 'n' : "", 'o' : "", 'p' : "", 'q' : "", 'r' : "", 's' : "", 't' : "", 'u' : "", 'v' : "", 'w' : "", 'x' : "", 'y' : "", 'z' : "", '0' : "", '1' : "", '2' : "", '3' : "", '4' : "", '5' : "", '6' : "", '7' : "", '8' : "", '9' : "", '~' : "", '`' : "", '!' : "", '@' : "", '#' : "", '$' : "", '%' : "", '^' : "", '&' : "", '*' : "", '(' : "", ')' : "", '-' : "", '_' : "", '+' : "", '=' : "", '  ' : "", '[' : "", ']' : "", '{' : "", '}' : "", '\'': "", '<' : "", '>' : "", '\\' : "", '|' : "", '\"' : "", ';' : "", ':' : "", '.' : "", ',' : "", '?' : ""}

class Node:
	def __init__(self, char, count):
		self.left = None
		self.right = None
		self.char = char
		self.count = count
		self.isleaf = 1
		self.binary = ""

	def form(self,first,second):
		self.left = first
		self.right = second
		self.isleaf = 0

def set_binary(self):
	if self.left:
		self.left.binary = self.binary+'0'	#add 0 to binary on moving left
		if(self.left.isleaf):
			binary_code[self.left.char] = self.left.binary
		set_binary(self.left)
	if self.right:
		self.right.binary = self.binary+'1'	#	add 1 to binary on moving right
		if(self.right.isleaf):
			binary_code[self.right.char] = self.right.binary
		set_binary(self.right)

def encode(input_file, output_file):
	frequency = { 'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0, 'E' : 0, 'F' : 0, 'G' : 0, 'H' : 0, 'I' : 0, 'J' : 0, 'K' : 0, 'L' : 0, 'M' : 0, 'N' : 0, 'O' : 0, 'P' : 0, 'Q' : 0, 'R' : 0, 'S' : 0, 'T' : 0, 'U' : 0, 'V' : 0, 'W' : 0, 'X' : 0, 'Y' : 0, 'Z' : 0, 'a' : 0, 'b' : 0, 'c' : 0, 'd' : 0, 'e' : 0, 'f' : 0, 'g' : 0, 'h' : 0, 'i' : 0, 'j' : 0, 'k' : 0, 'l' : 0, 'm' : 0, 'n' : 0, 'o' : 0, 'p' : 0, 'q' : 0, 'r' : 0, 's' : 0, 't' : 0, 'u' : 0, 'v' : 0, 'w' : 0, 'x' : 0, 'y' : 0, 'z' : 0, '0' : 0, '1' : 0, '2' : 0, '3' : 0, '4' : 0, '5' : 0, '6' : 0, '7' : 0, '8' : 0, '9' : 0, '~' : 0, '`' : 0, '!' : 0, '@' : 0, '#' : 0, '$' : 0, '%' : 0, '^' : 0, '&' : 0, '*' : 0, '(' : 0, ')' : 0, '-' : 0, '_' : 0, '+' : 0, '=' : 0, ' ' : 0, '[' : 0, ']' : 0, '{' : 0, '}' : 0, '\n' : 0, '\'' : 0, '<' : 0, '>' : 0, '\\' : 0, '|' : 0, '\"' : 0, ';' : 0, ':' : 0, '.' : 0, ',' : 0, '?' : 0, '/' : 0, '\t' : 0}
	binary_code_r = {}
	priority_queue = []
	with open(input_file) as f:
		for line in f:
			for word in line:
				frequency[word] = frequency[word]+1;
	a = sorted(frequency.items(), key=lambda x: x[1])
	frequency =OrderedDict(a)
	for i in frequency:
		if(frequency[i] > 0):
			n = Node(i,frequency[i])
			priority_queue.append(n) #Create nodes for all existing(count > 0) nodes to priority_queue
	priority_queue.reverse()
	first = priority_queue.pop()
	second = priority_queue.pop()
	while 1:
		parent = Node(first.char+second.char, first.count+second.count)
		priority_queue.append(parent)	#add parent to priority_queue as well
		priority_queue.sort(key=lambda priority_queue: priority_queue.count, reverse=True)
		parent.form(first,second) #forms parent from first and second
		first = priority_queue.pop()
		if not priority_queue:	#breaks when only one node is left
			break
		second = priority_queue.pop()

	set_binary(first)
	for i in binary_code:
		binary_code_r[binary_code[i]] = i #reverse of binary_code for decrypt purpose
	fs = open(output_file,'w+')
	count = len(binary_code_r)*2+1
	fs.write(str(count+1)) #separate encodeded information from encoded text
	fs.write("\n")
	for i in binary_code_r:
		fs.write(i)
		fs.write("\n")
		fs.write(binary_code_r[i])
		fs.write("\n")
	fs.close()
	fo = open(output_file,'a+')
	with open(input_file) as f:
		for line in f:
			for word in line:
				fo.write(binary_code[word])	#write the encoded value of each character
	fo.close()

def decode(input_file, output_file):
	file1 = open(input_file, 'r')
	Lines = file1.readlines()
	decoders = []
	itr=0
	binary_decode={}
	for line in Lines:
		decoders.append(line[:-1])
	key = ""
	margin = int(Lines[0]) #Margin is to separate encodeded information from encoded text
	for i in decoders:
		if ( itr < margin):
			if (itr<4):
				if itr==1:
					binary_decode[i] = "\n" #new line character decode info
			elif(itr%2==0):
				key = i
			else:
				binary_decode[key] = i #collect the encode encryption info of characters other that '\n'
			itr+=1
		else:
			break
	fo = open(output_file,'w+')
	current_word = ""
	itr = 0
	with open(input_file,'r') as f:
		for line in f:
			if (itr > margin-1):
				for word in line:
					current_word = current_word+word	#incremental read and addition of updating current_word
					if current_word in binary_decode.keys():	#check if current_word is in binary keys
						fo.write(binary_decode[current_word])	#write the decoded character
						current_word = ""	#start looking for next match
			itr+=1
	fo.close()

def get_options(args=sys.argv[1:]):
	parser = argparse.ArgumentParser(description="Huffman compression.")
	groups = parser.add_mutually_exclusive_group(required=True)
	groups.add_argument("-e", type=str, help="Encode files")
	groups.add_argument("-d", type=str, help="Decode files")
	parser.add_argument("-o", type=str, help="Write encoded/decoded file", required=True)
	options = parser.parse_args()
	return options


if __name__ == "__main__":
	options = get_options()
	if options.e is not None:
		encode(options.e, options.o)
	if options.d is not None:
		decode(options.d, options.o)
