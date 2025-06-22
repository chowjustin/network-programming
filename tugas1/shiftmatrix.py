arr = []
for i in range(3):
    arr.append(list(map(int, input().split())))

shift = int(input())

def shiftmatrix(matrix, n):
    for _ in range(n): 
        top_left = matrix[0][0]
        top_middle = matrix[0][1]
        top_right = matrix[0][2]
        right_middle = matrix[1][2]
        bottom_right = matrix[2][2]
        bottom_middle = matrix[2][1]
        bottom_left = matrix[2][0]
        left_middle = matrix[1][0]

        matrix[0][1] = top_left
        matrix[0][2] = top_middle
        matrix[1][2] = top_right
        matrix[2][2] = right_middle
        matrix[2][1] = bottom_right
        matrix[2][0] = bottom_middle
        matrix[1][0] = bottom_left
        matrix[0][0] = left_middle

    for row in matrix:
        print(*row)

shiftmatrix(arr, shift)
