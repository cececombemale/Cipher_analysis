import random

list_of_words = ["awesomeness", "hearkened","aloneness","beheld","courtship","swoops",
"memphis", "attentional","pintsized","rustics","hermeneutics","dismissive","delimiting","proposes",
"between","postilion","repress","racecourse","matures","directions","pressed","miserabilia",
"indelicacy","faultlessly","chuted","shorelines","irony","intuitiveness","cadgy","ferries","catcher",
"wobbly","protruded","combusting","unconvertible","successors","footfalls","bursary","myrtle","photocompose"]

letters = 'abcdefghijklmnopqrstuvwxyz'

max_key_length = 24

letter_to_numbers = {" ": 0, "a": 1,"b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, 
"h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,"p": 16, "q": 17, "r": 18,
"s": 19, "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26}

numbers_to_letters = {0 : " ", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 
8: "h", 9: "i", 10: "j", 11: "k", 12: "l", 13: "m", 14: "n", 15: "o",16: "p", 17: "q", 18: "r",
19: "s", 20: "t", 21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 26: "z"}
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

	print(spacings)
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
	print(factors)
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
	print(factor_counts)
	return factor_counts

#return the common factors 
def most_common_factors(factor_counts):

	ordered_factors = []

	for k in factor_counts.keys():
		if k > max_key_length:
			continue
		ordered_factors.append((k, factor_counts[k]))

	ordered_factors.sort(key = lambda x: x[1])
	return ordered_factors 


def kasiski(c):
	#call all helper functions to give the most probable key lengths 
	#as an array 
	spacings = find_repeated_sequences(c)

	factors = factorize(spacings)

	counts = count_factors(factors)

	common = most_common_factors(counts)

	return common


def select_words():
	#select words from the list of words to create message to encrypt
	length = len(list_of_words)

	#randomly select the length of the message
	length_of_c = random.randint(100,500)

	#empty variable to append to 
	message = ""

	#for the length of the message, get random word from the list of words and 
	#add to the message and a space
	for i in range(length_of_c):
		word = random.randint(0,length-1)
		message += list_of_words[word] + " "

	#remove the last character in the message which is a space
	message = message[:-1]

	return message

def create_key():
	key = []

	#select a random key length
	t = random.randint(1,24)

	#create the key by using the scheduling algorithm he gave us,
	#need to figure out how to make this more complex for better testing 
	for i in range(1, t+1):
		key.append(1 + (i%t))

	return key

def create_cipher_from_message(key,message):

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


	#encrypt message 
	c = ""
	for i in range(len(message)):
		m = message[i]
		k = key[i]

		m_num = letter_to_numbers[m]

		m_num = m_num + k

		if m_num > 26:
			m_num = (m_num % 26) - 1

		c += numbers_to_letters[m_num]

	return c



message = select_words()


key = create_key()

print(len(key))


c = create_cipher_from_message(key,message)

print(message)

print()

print(c)

print(kasiski(c))




