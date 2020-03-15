import random

import frequency_analysis 

import sys

import itertools



list_of_words = ["awesomeness", "hearkened","aloneness","beheld","courtship","swoops",
"memphis", "attentional","pintsized","rustics","hermeneutics","dismissive","delimiting","proposes",
"between","postilion","repress","racecourse","matures","directions","pressed","miserabilia",
"indelicacy","faultlessly","chuted","shorelines","irony","intuitiveness","cadgy","ferries","catcher",
"wobbly","protruded","combusting","unconvertible","successors","footfalls","bursary","myrtle","photocompose"]

letters = 'abcdefghijklmnopqrstuvwxyz'

letters2 = ' abcdefghijklmnopqrstuvwxyz'

max_key_length = 24

letter_to_numbers = {" ": 0, "a": 1,"b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, 
"h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,"p": 16, "q": 17, "r": 18,
"s": 19, "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26}

numbers_to_letters = {0 : " ", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 
8: "h", 9: "i", 10: "j", 11: "k", 12: "l", 13: "m", 14: "n", 15: "o",16: "p", 17: "q", 18: "r",
19: "s", 20: "t", 21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 26: "z"}

#letters = 'abcdefghijklmnopqrstuvwxyz'

most_common_order= ''
not_possible = ''
def find_repeated_sequences(c):

	
	spacings = dict() #repeated sequences and how far away they are from eachother

	for seq_len in range(3,6): #looking for repeated sequences at least 
	#3 letters long and up to 6, unlikely that it will be higher than 5
		
		for s in range(len(c) - seq_len): #start looping throught the ciphertext to find
		#repeated sequences 
			sequence = c[s:s+seq_len] 

			for i in range(s + seq_len, len(c) - seq_len): #check if there are any
			#repeated sequences 
				if c[i: i+s] == sequence:
				#if there is then check if the sequence is in the dictionary, if it is then add
				#the spacing, if not then add sequence to dictionary 
					if sequence not in spacings:
							spacings[sequence] = []
					spacings[sequence].append(i-s)

	return spacings


def factorize(spacings):
	# returns the factors of each spacing 
	factors = []
	#iterate through the spacing lengths and find all factors for each spacing
	for k in spacings.keys():
		
		num = spacings[k]
		for n in num:
			if n < 2:
		#consider what we have to do for a length 1 key, not sure yet 
				return []
		#calculate factors and add them to list
			for i in range(2, n+1):
				if n % i == 0:
					factors.append(i)
	if 1 in factors:
		factors.remove(1)
	return factors


def count_factors(factors):
#create a dictionary where key is factor and value is the count of each factor
	factor_counts = dict()
	#add to dictionary if not in dictionary, or else increase count by 1
	for i in factors:
		if i not in factor_counts:
			factor_counts[i] = 1
		else:
			factor_counts[i] += 1
	return factor_counts

#return the common factors 
def most_common_factors(factor_counts):

	ordered_factors = []

	for k in factor_counts.keys():
		if k > max_key_length:
			continue
		ordered_factors.append((k, factor_counts[k]))

	ordered_factors.sort(key = lambda x: x[1], reverse = True)
	return ordered_factors 


def kasiski(c):
	#call all helper functions to give the most probable key lengths 
	#as an array 
	spacings = find_repeated_sequences(c)

	factors = factorize(spacings)

	counts = count_factors(factors)

	common = most_common_factors(counts)

	return common


def expand_key(key, message):
	#turn message into list
	message = list(message)
	
	#get inital key length so that we can make key the same length as 
	#message by repeating
	inital_key_length = len(key)
	
	#extend key 
	index = 0
	for i in range(len(message)):
		key.append(key[index])

		index += 1

		if index > inital_key_length-1:
			index = 0		
	#trim the end of the key off
	dif = len(key) - len(message)
	for i in range(dif):
		key.pop(-1)
	return key

def create_message_from_cipher(key,ciphertext):
	ciphertext = list(ciphertext)

	key = expand_key(key,ciphertext)
	#encrypt message 
	c = ""
	for i in range(len(ciphertext)):
		c1 = ciphertext[i]
		k = key[i]

		c_num = letter_to_numbers[c1]

		c_num = c_num - k

		#if c_num < 0:
		c_num = (c_num%27)
				
		c += numbers_to_letters[c_num]

	return c

#get the nth letters in the cipher text
def get_nth(n, kl, ciphertext):

	list_of_letters = []

	while (n -1) < len(ciphertext):
		list_of_letters.append(ciphertext[n-1])
		n += kl
	return list_of_letters

def decrypt_attempt(ciphertext,likely_key_length,most_common_order):

	scores = []
	for n in range(1, likely_key_length[0]+1):
		letters = get_nth(n,likely_key_length[0],ciphertext)

		s = []

		for k in range(0,27):
			attempted_d = create_message_from_cipher([k],letters)

			key_and_score = (k,frequency_analysis.plausability(attempted_d,most_common_order))
			s.append(key_and_score)
		s.sort(key = lambda x: x[1], reverse = True)

		#we will only attempt to decrypt with the most correct keys
		scores.append(s[:6])

	for c in itertools.product(range(6), repeat=likely_key_length[0]):

	 	pos_key = []

	 	for i in range(likely_key_length[0]):
	 		pos_key.append(scores[i][c[i]][0])

	 	possible_message = create_message_from_cipher(pos_key,ciphertext)
	 	possible_message = possible_message.split(" ")
	 	if len(possible_message) <3:
	 		return 0
	 	else:
	 		if possible_message[0] and possible_message[1] and possible_message[2] in list_of_words:
	 			return possible_message
	return 0
	 	

def crack_cipher(ciphertext,most_common_order, letters2):
	all_likely_key_length = kasiski(ciphertext)

	if all_likely_key_length == []:

		print("Sorry, we could not find the key length")

		sys.exit(1)

	l = []
	for i in all_likely_key_length:
		l.append(i[0])
	print("Kaiski thinks that the key length could be the following ", l)
	print()
	for key_length in all_likely_key_length:
		decrypt = decrypt_attempt(ciphertext,key_length,most_common_order)
		if decrypt != 0:
			return decrypt
	# for i in range(likely_key_length):
	# 	key = []

	# 	for j in range(4):
	# 		key.append(scores[i][(j+4)])



c = input("Please input the ciphertext: ")

print()

frequencies,not_possible = frequency_analysis.count_letters_in_letterbase(list_of_words,not_possible)

#print(frequencies)
most_common_order = frequency_analysis.make_most_common(frequencies)

m = crack_cipher(c,most_common_order,letters2)
m2 = ""
for i in m:
	m2 += i + " "

m2 = m2[:-1]

print(m2)





