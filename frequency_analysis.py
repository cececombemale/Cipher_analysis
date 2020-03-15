
'''
list_of_words = ["awesomeness", "hearkened","aloneness","beheld","courtship","swoops",
"memphis", "attentional","pintsized","rustics","hermeneutics","dismissive","delimiting","proposes",
"between","postilion","repress","racecourse","matures","directions","pressed","miserabilia",
"indelicacy","faultlessly","chuted","shorelines","irony","intuitiveness","cadgy","ferries","catcher",
"wobbly","protruded","combusting","unconvertible","successors","footfalls","bursary","myrtle","photocompose"]
'''
letters = 'abcdefghijklmnopqrstuvwxyz'

most_common_order= ''
not_possible = ''

#comment this out later but it works. 
def count_letters_in_letterbase(list_of_words, not_possible):
	#gets the freqencies of all the letters in the letter base, including spaces
	
	#get spaces count by getting the number of words -1, there will always be 
	#a space after a word according to documentation by prof
	count = 0
	w_count = 0
	individual_letter = {}
	for i in list_of_words:
		w_count += 1
		c = len(i)
		count += c

	spaces = w_count -1


	count += spaces

	#make dictionary and could how many times each letter appears 
	#add spaces count to dictionary too
	for w in list_of_words:
		for l in w:
			if l not in individual_letter:
				individual_letter[l] = 1
			else:
				individual_letter[l] += 1

	individual_letter[" "] = spaces 

	for l in letters:
		if l not in individual_letter:
			individual_letter[l] = 0
			not_possible += l
	
	return individual_letter,not_possible

#this just counts how many of each letter in a particular message 
def get_message_letter_count(message):
	message_letter_count = dict()
	for l in message:
		if l not in message_letter_count:
			message_letter_count[l] = 1
		else:
			message_letter_count[l] += 1
	return message_letter_count

#make a list of the most common letters in our list of words from prof
def make_most_common(frequencies):

	#reverses the letter --> frequency dictionary to frequency --> letter
	freq_letter = dict()
	for key in frequencies.keys():
		if frequencies[key] not in freq_letter:
			freq_letter[frequencies[key]] = [key]

		else:
			freq_letter[frequencies[key]].append(key)

	#make list of tuples where the first index is frequency and second is 
	#letters that correspond to that frequency
	ordered_frequencies = []

	for key in freq_letter.keys():
		ordered_frequencies.append((key, freq_letter[key]))

	#sort the list from greatest to smallest according to frequency
	ordered_frequencies.sort(key = lambda x: x[0], reverse = True)
	
	#append most common letters to a list 
	most_common = ''
	for i in ordered_frequencies:
		for l in i[1]:
			most_common += l
	return most_common

#get the most common letters in a particular message we are attempting to 
#decrypt, and organize it in the order relative to the most common in our
#list of words 
def order_frequencies(message,most_common_order):
	letter_freq = get_message_letter_count(message)

	freq_letter = dict()

	#create an inverted dictionary, frequencies are keys and value
	#is list of letters w that frequency
	for key in letter_freq.keys():
		if letter_freq[key] not in freq_letter:
			freq_letter[letter_freq[key]] = [key]

		else:
			freq_letter[letter_freq[key]].append(key)

	#make a list that we can sort by frequency
	ordered_frequencies = []

	for key in freq_letter.keys():
		ordered_frequencies.append((key, freq_letter[key]))

	ordered_frequencies.sort(key = lambda x: x[0], reverse = True)

	for i in range(len(ordered_frequencies)):
		ordered_frequencies[i][1].sort(key=most_common_order.find, reverse = True)

	#put the message in most common order form 
	ordered_message = ''

	for i in ordered_frequencies:
		for l in i[1]:
			ordered_message += l
	return ordered_message 

#see how plausible the decryption is, if there is a letter from the not 
#possible list then immediately return 0, check the frequency of letters
#in the top 12 most frequent letters in our word list and compare to message
def plausability(message,most_common_order):
	order = order_frequencies(message,most_common_order)

	score = 0

	for l in not_possible:
		if l in order:
			return 0

	for l in most_common_order[:12]:
		if l in order[:12]:
			score += 1
	return score


#letter_frequencies = count_letters_in_letterbase(list_of_words)









