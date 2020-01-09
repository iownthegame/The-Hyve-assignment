import binascii
import os

USE_TRIVIAL_IMPLEMENTATION = int(os.environ.get('USE_TRIVIAL_IMPLEMENTATION', '0'))

def read_binary_file(file_in, file_out):
    with open(file_in, "rb") as f_in:
        with open(file_out, "wb") as f_out:
            # read
            pair = []
            current_data = []

            byte = f_in.read(1)
            while byte:
                # bin to hex
                hex_input = binascii.hexlify(byte)
                # print('input', hex_input)
                pair.append(hex_input)
                if len(pair) == 2:
                    # process
                    data = decode(pair, current_data)
                    current_data += data
                    print('output', current_data)

                    # write to standard output
                    for hex_output in current_data:
                        # hex to bin
                        bin_output = binascii.unhexlify(hex_output)
                        f_out.write(bin_output)

                    # write to standard error
                    reencoded_data = []
                    if USE_TRIVIAL_IMPLEMENTATION:
                        for d in current_data:
                            reencoded_data += [0, d]
                    else:
                        pass

                    pair = []

                # read
                byte = f_in.read(1)

def decode(pair, current_data):
    p, q = pair
    p_int = int(p, 16)  # hex to integer
    # print('decode', p, q)
    # print('current_data', current_data)
    if p_int == 0:
        return [q]

    q_int = int(q, 16)  # hex to integer
    if q_int > p_int: # invalid
        return ['3F']

    if len(current_data) < p_int: # invalid
        return ['3F']

    """
    Read the last pi characters appended to the result string
    and take the first (from the left) qi characters.
    """
    start_idx = len(current_data) - p_int
    return current_data[start_idx:start_idx+q_int] # Read the last pi characters appended

if __name__ == "__main__":
    # read_binary_file('decode_input.bin', 'decode_output.bin')
    read_binary_file('test1.in', 'test1.out')
    read_binary_file('test2.in', 'test2.out')