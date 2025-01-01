case=input('camelCase:')
snake_case=print ('snake_case:', end='')
for letter in case :
    if letter.isupper():
        print('_'+letter.lower(),end='')
    else:
        print(letter,end="")
print()