text=input('Input:')
print("Output:",end="")
for letter in text:
    if not letter.lower() in ['a','e','u','o','i']:
        print(letter,end="")
print()
