import sys
digit_string = sys.argv[1]
result = 0
for digit in digit_string:
    result += int(digit)
print(result)