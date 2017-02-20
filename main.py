IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP1 = [4, 1, 3, 5, 7, 2, 8, 6]

EP = [4, 1, 2, 3, 2, 3, 4, 1]

P4 = [2, 4, 3, 1]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]

SUB0 = [[1, 0, 3, 2],
        [3, 2, 1, 0],
        [0, 2, 1, 3],
        [3, 1, 3, 2]]

SUB1 = [[0, 1, 2, 3],
        [2, 0, 1, 3],
        [3, 0, 1, 0],
        [2, 1, 0, 3]]

def permute(permutation, values):
    '''
    Applies the supplied permutation table to the values supplied
    '''
    output = ''
    for i in range(len(permutation)):
        output += values[permutation[i] - 1]
    return output

def left_shift(values, amount):
    '''
    Simulates a left shift on a string representation of bits
    '''
    output = values
    for i in range(amount):
        output += output[0]
        output = output[1:]
    return output

def gen_subkeys(key):
    '''
    Creates the two subkeys from the supplied key

    Returns a tuple containing both keys
    '''
    key = permute(P10, key)

    left_sub = key[0:5]
    right_sub = key[5:]

    left_shift1_left = left_shift(left_sub, 1)
    left_shift1_right = left_shift(right_sub, 1)


    k1 = permute(P8, left_shift1_left + left_shift1_right)

    left_shift2_left = left_shift(left_shift1_left, 2)
    left_shift2_right = left_shift(left_shift1_right, 2)


    k2 = permute(P8, left_shift2_left + left_shift2_right)

    return k1, k2

def xor(a, b):
    '''
    Simulates an XOR on two strings representing a collection of bits
    '''
    output = ''
    for i in range(len(a)):
        if a[i] == b[i]:
            output += '0'
        else:
            output += '1'
    return output

def substitute(values):
    '''
    Performs substitution using the constant sub boxes

    Returns the strings filled out to 4 characters
    '''
    sub1, sub2 = values[:-4], values[4:]

    sub1_col = int(sub1[1:-1], 2)
    sub1_row = int(sub1[0] + sub1[3], 2)

    sub2_col = int(sub2[1:-1], 2)
    sub2_row = int(sub2[0] + sub2[3], 2)

    sub1, sub2 = SUB0[sub1_row][sub1_col], SUB1[sub2_row][sub2_col]

    return '{0:b}'.format(sub1).zfill(2), '{0:b}'.format(sub2).zfill(2)

def single_round(left, right, subkey):
    '''
    Takes in left half, right half and subkey for start of a single_round
    returns the modified right half of the key
    '''
    right_permute = permute(EP, right)

    xored_half = xor(right_permute, subkey)

    sub1, sub2 = substitute(xored_half)

    post_p4 = permute(P4, sub1 + sub2)

    mod_right = xor(left, post_p4)

    return mod_right

def crypt(plaintext, key, decrypt=False):
    '''
    Applies the cryptograhic algorithm to supplied plaintext
    using supplied key.

    Optional decrypt flag reverses the keys, allowing for a
    previously encrypted byte to be decrypted
    '''

    subkey_1, subkey_2 = gen_subkeys(key)

    if decrypt:
        # decrypt is done with keys in reverse order, so swap them
        subkey_1, subkey_2 = subkey_2, subkey_1

    plaintext = permute(IP, plaintext)

    left, right = plaintext[:4], plaintext[-4:]

    first_single_round_result = single_round(left, right, subkey_1).zfill(4)
    final_single_round_result = single_round(right, first_single_round_result, subkey_2).zfill(4)

    ciphertext = permute(IP1, final_single_round_result + first_single_round_result)
    return ciphertext

plain = '10100101'
key = '0010010111'

print('Encrypting {} with the Key {}'.format(plain, key))
ciphered = crypt(plain, key)
print('Encrypted: {}\nDecrypting {} with the Key {}'.format(ciphered, ciphered, key))
decrypted = crypt(ciphered, key, True)
print('Decrypted: {}'.format(decrypted))
