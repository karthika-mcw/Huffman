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

def write_encode_info(binary_code,output_file):
	fs = open(output_file,'w+')
	count = len(binary_code)*2+1
	fs.write(str(count+1)) #separate encodeded information from encoded text
	fs.write("\n")
	for i in binary_code:
		fs.write(binary_code[i])
		fs.write("\n")
		fs.write(i)
		fs.write("\n")
	fs.close()

def get_frequency(input_file):
	frequency= {}
	with open(input_file) as f:
		for line in f:
			for word in line:
				if word in frequency.keys():
					frequency[word]=frequency[word]+1
				else:
					frequency[word] = 1
	return frequency

def get_priority_queue(frequency):
	priority_queue = []
	for i in frequency:
		if(frequency[i] > 0):
			n = Node(i,frequency[i])
			priority_queue.append(n) #Create nodes for all existing(count > 0) nodes to priority_queue
	return priority_queue

def form_tree(priority_queue):
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
	return first

def append_encoded_content(input_file,output_file,binary_code):
	fo = open(output_file,'a+')
	with open(input_file) as f:
		for line in f:
			for word in line:
				fo.write(binary_code[word])	#write the encoded value of each character
	fo.close()

def encode(input_file, output_file):
	frequency = get_frequency(input_file)
	a = sorted(frequency.items(), key=lambda x: x[1])
	frequency =OrderedDict(a)
	priority_queue = get_priority_queue(frequency)
	priority_queue.reverse()
	root = form_tree(priority_queue)
	set_binary(root)
	write_encode_info(binary_code,output_file)
	append_encoded_content(input_file,output_file,binary_code)

def write_output(input_file,output_file,binary_decode,margin):
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

def get_decode_info(input_file):
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
	return margin,binary_decode

def decode(input_file, output_file):
	margin,binary_decode = get_decode_info(input_file)
	write_output(input_file,output_file,binary_decode,margin)

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
