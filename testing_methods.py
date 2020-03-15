import random

list_of_words = ["awesomeness", "hearkened","aloneness","beheld","courtship","swoops",
"memphis", "attentional","pintsized","rustics","hermeneutics","dismissive","delimiting","proposes",
"between","postilion","repress","racecourse","matures","directions","pressed","miserabilia",
"indelicacy","faultlessly","chuted","shorelines","irony","intuitiveness","cadgy","ferries","catcher",
"wobbly","protruded","combusting","unconvertible","successors","footfalls","bursary","myrtle","photocompose"]

letter_to_numbers = {" ": 0, "a": 1,"b": 2, "c": 3, "d": 4, "e": 5, "f": 6, "g": 7, 
"h": 8, "i": 9, "j": 10, "k": 11, "l": 12, "m": 13, "n": 14, "o": 15,"p": 16, "q": 17, "r": 18,
"s": 19, "t": 20, "u": 21, "v": 22, "w": 23, "x": 24, "y": 25, "z": 26}

numbers_to_letters = {0 : " ", 1: "a", 2: "b", 3: "c", 4: "d", 5: "e", 6: "f", 7: "g", 
8: "h", 9: "i", 10: "j", 11: "k", 12: "l", 13: "m", 14: "n", 15: "o",16: "p", 17: "q", 18: "r",
19: "s", 20: "t", 21: "u", 22: "v", 23: "w", 24: "x", 25: "y", 26: "z"}


def select_words():
	#select words from the list of words to create message to encrypt
	length = len(list_of_words)

	#randomly select the length of the message
	length_of_c = random.randint(45,50)

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

	for i in range(1, t+1):
		key.append(random.randint(0,26))

	#create the key by using the scheduling algorithm he gave us,
	#need to figure out how to make this more complex for better testing 
	# for i in range(1, t+1):
	# 	key.append(1 + (i%t))

	return key
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
def create_cipher_from_message(key,message):

	# #turn message into list
	message = list(message)
	key = expand_key(key,message)
	#encrypt message 
	c = ""
	for i in range(len(message)):
		m = message[i]
		k = key[i]

		m_num = letter_to_numbers[m]

		m_num = m_num + k
		#print(m_num)

		#if m_num > 26:
	
			#print('before conversion', m_num)
		m_num = (m_num % 27)
			
			#print('after mod', m_num)
			#m_num -= 1
			#print("message as index", m_num)

		c += numbers_to_letters[m_num]

	return c





message = select_words()
print(message)

key = create_key()
print(len(key))

c = create_cipher_from_message(key,message)

print(c)




