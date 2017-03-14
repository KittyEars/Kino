def empty_environment():
	return []

# Stack overflow way of doing it http://stackoverflow.com/questions/1601269/how-to-make-a-completely-unshared-copy-of-a-complicated-list-deep-copy-is-not
def unshared_copy(inList):
	if isinstance(inList, list):
		return list( map(unshared_copy, inList) )
	return inList

def extend_environment(symbols, values, environment):
	newenvironment = unshared_copy(environment)
	newenvironment.insert(0,[symbols,values])
	return newenvironment

def apply_environment(environment, symbol):
	if environment == []:
		raise IndexError
	head = environment[0]
	symbols = head[0]
	values = head[1]
	
	try:
		return values[symbols.index(symbol)]
	except:
		return apply_environment(environment[1:],symbol)