answer = input('Great Question of Life \n').strip()
answer = answer.lower()
if answer=='42' or answer=='forty-two' or answer=='forty two':
    print('yes')
else:
    print('no')