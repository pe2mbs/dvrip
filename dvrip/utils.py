from inspect import currentframe, getfullargspec
from .errors import DVRIPDecodeError


def init(type, obj):  # pylint: disable=redefined-builtin # FIXME remove
	frame = currentframe().f_back
	for attr in type.__slots__:
		setattr(obj, attr, frame.f_locals[attr])

def pun(attrs):
	frame = currentframe().f_back
	return {attr: frame.f_locals[attr] for attr in attrs}

def eq(type, lhs, rhs):  # pylint: disable=redefined-builtin
	if not isinstance(rhs, type):
		return NotImplemented
	return all(getattr(lhs, attr) == getattr(rhs, attr)
	           for attr in type.__slots__)

def repr(obj):  # pylint: disable=redefined-builtin
	spec  = getfullargspec(type(obj).__init__)
	inits = []
	attrs = list(type(obj).__slots__)
	for pos in spec.args[1:]:
		if pos not in attrs: break
		attrs.remove(pos)
		inits.append('{!r}'.format(getattr(obj, pos)))
	for key in attrs:
		assert key in spec.args + spec.kwonlyargs
		inits.append('{}={!r}'.format(key, getattr(obj, key)))
	return '{}({})'.format(type(obj).__qualname__, ', '.join(inits))

def checkbool(json, description):
	if not isinstance(json, bool):
		raise DVRIPDecodeError('not a boolean in {}'
		                       .format(description))
	return json

def checkint(json, description):
	if not isinstance(json, int):
		raise DVRIPDecodeError('not an integer in {}'
		                       .format(description))
	return json

def checkstr(json, description):
	if not isinstance(json, str):
		raise DVRIPDecodeError('not a string in {}'.format(description))
	return json

def checkdict(json, description):
	if not isinstance(json, dict):
		raise DVRIPDecodeError('not a dictionary in {}'
		                       .format(description))
	return json

def checkempty(json, description):
	assert isinstance(json, dict)
	if json:
		raise DVRIPDecodeError('extra keys in {}'.format(description))
	return json

def popkey(json, key, description):
	assert isinstance(json, dict)
	value = json.pop(key, Ellipsis)
	if value is Ellipsis:
		raise DVRIPDecodeError('{} missing'.format(description))
	return value

def popint(json, key, description):
	return checkint(popkey(json, key, description), description)

def popstr(json, key, description):
	return checkstr(popkey(json, key, description), description)