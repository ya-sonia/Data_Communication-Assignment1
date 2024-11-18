import matplotlib.pyplot as plt
import numpy as np

# B8ZS (Scrambled AMI Encoding)
def b8zs_encoding(bits):
    encoded_bits = np.array([])  # To store encoded bits
    consecutive_zeros_count = 0
    current_level = 1
    scrambled_segments = []  # To track scrambled signal segments

    for bit in bits:
        if bit == '1':
            encoded_bits = np.append(encoded_bits, current_level)
            consecutive_zeros_count = 0
            current_level = -current_level  # Alternate polarity for '1'
        elif bit == '0':
            consecutive_zeros_count += 1
            if consecutive_zeros_count == 8:  # B8ZS substitution for 8 zeros
                encoded_bits = encoded_bits[:-7]  # Remove last 7 zeros

                # B8ZS substitution pattern: 000VB0VB
                substitution = [0, 0, 0, current_level, -current_level, 0, -current_level, current_level]
                encoded_bits = np.append(encoded_bits, substitution)
                scrambled_segments.append(substitution)  # Track scrambled segment
                consecutive_zeros_count = 0
            else:
                encoded_bits = np.append(encoded_bits, 0)

    return encoded_bits, scrambled_segments


# B8ZS Decoding
def b8zs_decoding(encoded_bits):
    decoded_bits = []
    i = 0
    while i < len(encoded_bits):
        if i + 7 < len(encoded_bits) and np.array_equal(
            encoded_bits[i:i + 8], [0, 0, 0, encoded_bits[i + 3], -encoded_bits[i + 3], 0, -encoded_bits[i + 3], encoded_bits[i + 3]]):
            decoded_bits.extend(['0'] * 8)  # Decode the B8ZS pattern back to 8 zeros
            i += 8
        else:
            if encoded_bits[i] == 1 or encoded_bits[i] == -1:
                decoded_bits.append('1')
            else:
                decoded_bits.append('0')
            i += 1

    return ''.join(decoded_bits)


# Plot the B8ZS Encoded Data and Scrambled Signal
def plot_b8zs(b8zs_data, scrambled_segments):
    plt.figure(figsize=(10, 6))

    # Plot B8ZS encoded data
    plt.step(np.arange(len(b8zs_data)), b8zs_data, where='post', color='grey', linewidth=4, label="B8ZS Encoded Data")

    # Plot scrambled signal segments
    for segment in scrambled_segments:
        segment_start = len(b8zs_data) - len(np.concatenate(scrambled_segments))
        plt.plot(np.arange(segment_start, segment_start + len(segment)), segment, color='blue', label="Scrambled Segment")

    plt.title('B8ZS Encoded Data with Scrambled Signal')
    plt.xlabel('Bit Index')
    plt.ylabel('Voltage Level')
    plt.axhline(0, color='red', linestyle='--')
    plt.ylim(-1.5, 1.5)  # Voltage levels for B8ZS
    for i in range(0, len(b8zs_data)):
        plt.axvline(i, color='black', linestyle='--', alpha=0.3)

    # Adding labels to the graph
    plt.legend(loc="upper right")
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
            bit = input(f"Bit {i + 1}: ")
            if bit in ['0', '1']:
                binary_data.append(bit)
                break
            else:
                print("Invalid input. Only binary values (0 or 1) are allowed.")

    # Encoding the data using B8ZS
    b8zs_data, scrambled_segments = b8zs_encoding(binary_data)
    print("Binary Data:", binary_data)
    print("B8ZS Encoded Data:", b8zs_data)

    # Check if scrambling occurred
    if scrambled_segments:
        print("Scrambled Signal Produced:")
        for segment in scrambled_segments:
            print(segment)
    else:
        print("No scrambling was necessary in the encoded data.")

    # Plotting the B8ZS encoded data along with scrambled segments
    plot_b8zs(b8zs_data, scrambled_segments)

    # Decoding the data if desired
    decode_choice = input("Do you want to decode the B8ZS encoded data? (yes/no): ").strip().lower()
    if decode_choice == 'yes':
        decoded_data = b8zs_decoding(b8zs_data)
        print("Decoded Data:", decoded_data)
    else:
        print("Decoding skipped.")
