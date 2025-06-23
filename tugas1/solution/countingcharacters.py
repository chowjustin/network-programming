text = input()
printed = set()

for char in text:
    if char not in printed:
        temp = text.count(char)
        print("%c=%d" % (char, temp))
        printed.add(char)