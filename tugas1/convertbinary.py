x = int(input())

binary = ''

while x > 0:
    binary = str(x % 2) + binary
    x = x // 2
    
print (binary)
