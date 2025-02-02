import heapq
import os
from collections import Counter

class BinaryTree:
    """
    A class representing a node in the Huffman binary tree.
    Each node contains a value (character) and its frequency in the text.
    """
    def __init__(self, value, frequency):
        self.value = value  # Character value (None for internal nodes)
        self.frequency = frequency  # Frequency of the character
        self.left = self.right = None  # Left and right children

    def __lt__(self, other):
        """
        Comparison function for heap operations.
        Ensures the node with lower frequency has higher priority in the heap.
        """
        return self.frequency < other.frequency 

class HuffmanCode:
    """
    A class to implement Huffman Coding for compression and decompression of text files.
    """
    def __init__(self, path):
        self.path = path  # File path for input text
        self.__heap = []  # Min-heap to store Huffman tree nodes
        self.__code = {}  # Dictionary to store character-to-binary mapping
        self.__reversecode = {}  # Dictionary to store binary-to-character mapping

    def __frequency_from_text(self, text):
        """
        Builds a frequency dictionary for characters in the text.
        Uses Counter from collections for efficiency.
        """
        return Counter(text)

    def __build_heap(self, frequency_dict):
        """
        Builds a min-heap using heapq for Huffman tree construction.
        """
        self.__heap = [BinaryTree(key, freq) for key, freq in frequency_dict.items()]
        heapq.heapify(self.__heap)  # Converts list into a heap efficiently

    def __build_binary_tree(self):
        """
        Builds the Huffman tree from the heap by merging two minimum nodes repeatedly.
        """
        while len(self.__heap) > 1:
            node1, node2 = heapq.heappop(self.__heap), heapq.heappop(self.__heap)
            new_node = BinaryTree(None, node1.frequency + node2.frequency)
            new_node.left, new_node.right = node1, node2
            heapq.heappush(self.__heap, new_node)

    def __build_tree_code_helper(self, root, curr_bits=""):
        """
        Recursively assigns binary codes to characters based on the Huffman tree structure.
        """
        if root:
            if root.value:
                self.__code[root.value] = curr_bits  # Store binary representation for the character
                self.__reversecode[curr_bits] = root.value  # Reverse mapping for decoding
            else:
                self.__build_tree_code_helper(root.left, curr_bits + '0')
                self.__build_tree_code_helper(root.right, curr_bits + '1')

    def __build_tree_code(self):
        """
        Wrapper function to start the recursive encoding process.
        """
        self.__build_tree_code_helper(heapq.heappop(self.__heap))

    def __build_encoded_text(self, text):
        """
        Replaces characters in the text with their Huffman binary codes.
        """
        return ''.join(self.__code[char] for char in text)

    def __build_padded_text(self, encoded_text):
        """
        Pads the encoded text to make its length a multiple of 8 for byte conversion.
        """
        padding_value = (8 - len(encoded_text) % 8) % 8  # Calculate padding needed
        padded_info = f"{padding_value:08b}"  # Convert padding value to 8-bit binary
        return padded_info + encoded_text + '0' * padding_value

    def __build_byte_array(self, padded_text):
        """
        Converts the padded binary string into a byte array for storage in a file.
        """
        return bytearray(int(padded_text[i:i+8], 2) for i in range(0, len(padded_text), 8))

    def compress(self):
        """
        Compresses the input file using Huffman coding.
        """
        print("COMPRESSION STARTS...")
        filename, _ = os.path.splitext(self.path)
        output_path = filename + '.bin'

        with open(self.path, 'r', encoding="utf-8") as file:
            text = file.read().rstrip()

        frequency_dict = self.__frequency_from_text(text)
        self.__build_heap(frequency_dict)
        self.__build_binary_tree()
        self.__build_tree_code()

        padded_text = self.__build_padded_text(self.__build_encoded_text(text))
        with open(output_path, 'wb') as output:
            output.write(self.__build_byte_array(padded_text))

        print('Compressed successfully!')
        return output_path

    def __remove_padding(self, text):
        """
        Removes the padding added during compression.
        """
        padding_value = int(text[:8], 2)  # Extract padding size from the first 8 bits
        return text[8:-padding_value] if padding_value else text[8:]

    def __decode_text(self, text):
        """
        Decodes the binary text back into the original characters using Huffman codes.
        """
        decoded_text, current_bits = [], ""
        for bit in text:
            current_bits += bit
            if current_bits in self.__reversecode:
                decoded_text.append(self.__reversecode[current_bits])
                current_bits = ""
        return ''.join(decoded_text)

    def decompress(self, input_path):
        """
        Decompresses a Huffman encoded binary file back into its original text.
        """
        print("DECOMPRESSION STARTS...")
        filename, _ = os.path.splitext(input_path)
        output_path = filename + '_decompressed.txt'

        with open(input_path, 'rb') as file:
            bit_string = ''.join(f"{byte:08b}" for byte in file.read())

        actual_text = self.__decode_text(self.__remove_padding(bit_string))
        with open(output_path, 'w', encoding="utf-8") as output:
            output.write(actual_text)

        print("DECOMPRESSED SUCCESSFULLY!")
        return output_path

# Program execution
path = input("ENTER THE PATH OF YOUR FILE: ")
huffman = HuffmanCode(path)

compressed_file = huffman.compress()

huffman.decompress(compressed_file)
