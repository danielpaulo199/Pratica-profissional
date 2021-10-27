from re import A


list = ['#back green', '#back red', 'abacaxi', 'a melao']

x = "a"

matches = []
for find in list:
    if x in find and find[0] != "#":
        matches.append(find)

print(matches)
