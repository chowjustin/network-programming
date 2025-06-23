n = int(input())

sum = 0

while(n>0):
    temp = int(input())
    if(temp>=0):
        sum+=temp
    n-=1

print(sum)