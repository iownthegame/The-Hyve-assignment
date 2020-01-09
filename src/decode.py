import binascii
import os
import sys

USE_TRIVIAL_IMPLEMENTATION = int(os.environ.get('USE_TRIVIAL_IMPLEMENTATION', '0'))

def read_binary_file():
    f_out = os.fdopen(sys.stdout.fileno(), 'wb')
    f_err = os.fdopen(sys.stderr.fileno(), 'wb')

    pair = []
    current_data = []

    # read byte from standard input
    byte = sys.stdin.buffer.read(1)

    while byte:
        # byte to hex
        hex_input = byte.hex()
        pair.append(hex_input)
        if len(pair) == 2:
            # process
            data = decode(pair, current_data)
            current_data += data

            # write to standard output
            for hex_output in current_data:
                # hex to bin
                bin_output = binascii.unhexlify(hex_output)
                f_out.write(bin_output)
            f_out.flush()

            # re-encode decoding data
            reencoded_data = []
            if USE_TRIVIAL_IMPLEMENTATION:
                for d in current_data:
                    reencoded_data += ['00', d]
            else:
                pass

            # write to standard error
            for hex_output in reencoded_data:
                bin_output = binascii.unhexlify(hex_output)
                f_err.write(bin_output)
            f_err.flush()

            pair = []

        # read byte from stdin
        byte = sys.stdin.buffer.read(1)

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
    read_binary_file()
