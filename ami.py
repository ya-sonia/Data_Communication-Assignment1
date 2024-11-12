import matplotlib.pyplot as plt
import numpy as np  

# AMI Encoding
def ami_encoding(bits):
    encoded_bits = []
    current_level = 1 

    for bit in bits:
        if bit == '0':
            encoded_bits.append(0)
        elif bit == '1':
            encoded_bits.append(current_level)
            current_level = -current_level  

    return encoded_bits

# AMI Decoding
def ami_decoding(encoded_bits):
    decoded_bits = []
    current_level = 1 

    for level in encoded_bits:
        if level == 0:
            decoded_bits.append('0')
        else:
            decoded_bits.append('1') 
            current_level = -current_level 

    return ''.join(decoded_bits)

# Finding Longest Palindrome
def longestPalindrome(s):
    longest_palindrom = ''
    dp = np.zeros((len(s), len(s)), dtype=bool)  
    for i in range(len(s)):
        dp[i][i] = True
        longest_palindrom = s[i]
    for i in range(len(s)-1,-1,-1):
        for j in range(i+1,len(s)):  
            if s[i] == s[j]:
                if j-i ==1 or dp[i+1][j-1] is True:
                    dp[i][j] = True
                    if len(longest_palindrom) < len(s[i:j+1]):
                        longest_palindrom = s[i:j+1]                
    return longest_palindrom

# Plotting AMI Encoded Data
def plot(ami_data):
    plt.step(range(len(ami_data)), ami_data, where='post', color='grey', linewidth=4)
    plt.title('AMI Encoded Data')
    plt.xlabel('Bit Index')
    plt.ylabel('Voltage Level')
    plt.axhline(0, color='red')
    plt.ylim(-1.5, 1.5)  
    for i in range(0, len(ami_data)):
        plt.axvline(i, color='black', linestyle='--')
    plt.show()

if __name__ == '__main__':
    try:
        size = int(input("Enter the number of bits you want to input: "))
        if size <= 0:
            print("The size must be a positive integer.")
            exit()
    except ValueError:
        print("Invalid input. Please enter an integer value.")
        exit()

    binary_data = []
    print(f"Enter the binary data (0 or 1) for {size} bits:")
    for i in range(size):
        while True:
            bit = input(f"Bit {i+1}: ")
            if bit in ['0', '1']:
                binary_data.append(bit)
                break
            else:
                print("Invalid input. Only binary values  are allowed.")

    ami_data = ami_encoding(binary_data)
    print("Binary Data:", binary_data)
    print("AMI Encoded Data:", ami_data)

    # Finding the longest palindrome
    palindrome = longestPalindrome(''.join(binary_data))
    print("Longest palindrome in dataStream: ", palindrome)

    # Plotting the AMI encoded data
    plot(ami_data)

    # Decoding AMI
    decode_choice = input("Do you want to decode the AMI encoded signal? (yes/no): ").strip().lower()
    if decode_choice == "yes":
        decoded_data = ami_decoding(ami_data)
        print("Decoded Data:", decoded_data)
    else:
        print("Decoding skipped.")
