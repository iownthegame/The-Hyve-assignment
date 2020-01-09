import binascii
import os
import sys

USE_TRIVIAL_IMPLEMENTATION = int(os.environ.get('USE_TRIVIAL_IMPLEMENTATION', '0'))

class InputStream:
    def __init__(self):
        pass

    def get_input(self):
        return sys.stdin.buffer.read(1)

class OutputStream:
    def __init__(self, fp):
        self.fp = fp

    def write(self, output):
        self.fp.write(output)

    def flush(self):
        self.fp.flush()

class Application:
    def __init__(self, pair=None, current_data=None):
        self.stdin_stream = InputStream()

        self.pair = pair if pair else []
        self.current_data = current_data if current_data else []

    def set_output_stream(self):
        self.stdout_stream = OutputStream(os.fdopen(sys.stdout.fileno(), 'wb'))
        self.stderr_stream = OutputStream(os.fdopen(sys.stderr.fileno(), 'wb'))

    def set_trivial(self, trivial):
        self.trivial = trivial

    def process(self):
        # read byte from standard input
        byte = self.stdin_stream.get_input()
        self.set_output_stream()

        while byte:
            # byte to hex
            hex_input = byte.hex()
            self.pair.append(hex_input)
            if len(self.pair) == 2:
                # process
                data = self.decode()
                self.current_data += data

                # write to standard output
                for hex_output in self.current_data:
                    # hex to bin
                    bin_output = binascii.unhexlify(hex_output)
                    self.stdout_stream.write(bin_output)
                self.stdout_stream.flush()

                # re-encode decoding data
                re_encoded_data = self.re_encode()

                # write to standard error
                for hex_output in re_encoded_data:
                    bin_output = binascii.unhexlify(hex_output)
                    self.stderr_stream.write(bin_output)
                self.stderr_stream.flush()

                self.pair = []

            # read byte from stdin
            byte = self.stdin_stream.get_input()

    def decode(self):
        """decode the incoming pair and get the output"""
        p, q = self.pair
        wrong_encode_output = '3F'

        """
        check if any invalid or incomplete pair is found
        """
        try:
            p_int = int(p, 16)
            q_int = int(q, 16)
        except ValueError:
            return [wrong_encode_output]

        if p_int < 0 or q_int < 0:
            return [wrong_encode_output]

        """
        the pair represents exactly one decoded byte (the value of qi)
        """
        if p_int == 0:
            return [q]

        """
        check if any invalid or incomplete pair is found
        """
        if q_int > p_int: # invalid pair index
            return [wrong_encode_output]

        if len(self.current_data) < p_int: # invalid data range
            return [wrong_encode_output]

        """
         the pair represents the sequence obtained by taking qi bytes
         starting from an offset of pi bytes behind in the decoded stream
        """
        start_idx = len(self.current_data) - p_int
        return self.current_data[start_idx:start_idx+q_int] # Read the last pi characters appended

    def re_encode(self):
        re_encoded_data = []

        """
        always uses pi = 0
        """
        if self.trivial or len(self.current_data) == 1:
            for d in self.current_data:
                re_encoded_data += ['00', d]
            return re_encoded_data

        """
        produces an output as short as you can manage
        """
        prev_data = [self.current_data[0]] #['61']
        re_encoded_data = ['00', self.current_data[0]] #['00', '61']
        i = 1
        j = 0
        start = -1
        while i < len(self.current_data):
            if start != -1 and i - start == len(prev_data):
                prev_data += self.current_data[start:i]
                length = i - start
                re_encoded_data += [hex(length)[2:].zfill(2), hex(length)[2:].zfill(2)]
                start = -1
                j = 0
                continue
            if self.current_data[i] == prev_data[j]:
                if start == -1:
                    start = i
                i += 1
                j += 1
            else:
                if start == -1:
                    prev_data += [self.current_data[i]]
                    re_encoded_data += ['00', self.current_data[i]]
                else:
                    prev_data += self.current_data[start:i]
                    length = i - start
                    re_encoded_data += [hex(length)[2:].zfill(2), hex(length)[2:].zfill(2)]
                start = -1
                i += 1
                j = 0
        if start != -1:
            length = i - start
            re_encoded_data += [hex(length)[2:].zfill(2), hex(length)[2:].zfill(2)]
        return re_encoded_data

def run():
    app = Application()
    app.set_trivial(USE_TRIVIAL_IMPLEMENTATION)
    app.process()

if __name__ == '__main__':
    run()
