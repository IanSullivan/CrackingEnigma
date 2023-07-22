def check_substring(longer_string, substring):
    if len(longer_string) < len(substring):
        return False

    for i in range(len(longer_string) - len(substring) + 1):
        if longer_string[i:i+len(substring)] == substring:
            return True

    return False


def shift_string(longer_string, smaller_string):
    idx = 0
    for i in range(20):
        print(longer_string[idx: len(smaller_string) + idx])
        idx += 1
        print(check_substring(smaller_string, longer_string[idx: len(smaller_string) + idx]))

longer_string = "bcdefghijabcdopqrstuvwxy"
smaller_string = "abcd"

shifted = shift_string(longer_string, smaller_string)
print("Shifted string:", shifted)