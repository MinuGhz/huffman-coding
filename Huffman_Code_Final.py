import heapq
import os
import json
from collections import Counter

class BinaryTree:
    """
    Represents a node in the Huffman binary tree.
    Each node contains a character (value) and its frequency.
    """
    def __init__(self, value, frequency):
        self.value = value  # Character (None for internal nodes)
        self.frequency = frequency  # Frequency of occurrence
        self.left = self.right = None  # Left and right children

    def __lt__(self, other):
        """
        Defines comparison for heap operations, ensuring lower frequency nodes
        have higher priority.
        """
        return self.frequency < other.frequency 

class HuffmanCode:
    """
    Implements Huffman Coding for file compression and decompression.
    """
    def __init__(self, path):
        self.path = path  # Path to input file
        self.__heap = []  # Min-heap for building the Huffman tree
        self.__code = {}  # Dictionary to map characters to binary codes
        self.__reversecode = {}  # Reverse mapping from binary codes to characters

    def __frequency_from_text(self, text):
        """
        Creates a frequency dictionary for characters in the given text.
        """
        return Counter(text)

    def __build_heap(self, frequency_dict):
        """
        Builds a min-heap using the character frequency dictionary.
        """
        self.__heap = [BinaryTree(key, freq) for key, freq in frequency_dict.items()]
        heapq.heapify(self.__heap)

    def __build_binary_tree(self):
        """
        Constructs the Huffman tree by merging the two smallest nodes repeatedly.
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
            if root.value is not None:
                if curr_bits == "":
                    curr_bits = "0"  # Assign at least one bit to single-node trees
                self.__code[root.value] = curr_bits
                self.__reversecode[curr_bits] = root.value
            else:
                self.__build_tree_code_helper(root.left, curr_bits + '0')
                self.__build_tree_code_helper(root.right, curr_bits + '1')

    def __build_tree_code(self):
        """
        Initializes the encoding process by traversing the Huffman tree.
        """
        if not self.__heap:
            raise ValueError("Error: Huffman heap is empty!")
        root = heapq.heappop(self.__heap)
        self.__build_tree_code_helper(root)

    def __build_encoded_text(self, text):
        """
        Converts the text into its binary representation using the Huffman codes.
        """
        return ''.join(self.__code[char] for char in text)

    def __build_padded_text(self, encoded_text):
        """
        Pads the binary text to make its length a multiple of 8 for byte conversion.
        """
        padding_value = (8 - len(encoded_text) % 8) % 8
        padded_info = f"{padding_value:08b}"
        return padded_info + encoded_text + '0' * padding_value

    def __build_byte_array(self, padded_text):
        """
        Converts the padded binary string into a byte array.
        """
        return bytearray(int(padded_text[i:i+8], 2) for i in range(0, len(padded_text), 8))

    def compress(self):
        """
        Compresses the input file and saves the encoded data with metadata.
        """
        filename, _ = os.path.splitext(self.path)
        output_path = filename + '.bin'
        
        with open(self.path, 'r', encoding="utf-8") as file:
            text = file.read().rstrip()

        if not text:
            raise ValueError("Error: Input file is empty!")
        
        frequency_dict = self.__frequency_from_text(text)
        self.__build_heap(frequency_dict)
        self.__build_binary_tree()
        self.__build_tree_code()
        
        encoded_text = self.__build_encoded_text(text)
        padded_text = self.__build_padded_text(encoded_text)
        
        with open(output_path, 'wb') as output:
            output.write(json.dumps(frequency_dict).encode("utf-8") + b"\n")  
            output.write(self.__build_byte_array(padded_text))  

        return output_path

    def __remove_padding(self, text):
        """
        Removes padding added during compression.
        """
        padding_value = int(text[:8], 2)
        return text[8:] if padding_value == 0 else text[8:-padding_value]

    def __decode_text(self, text):
        """
        Converts binary text back into the original characters using Huffman codes.
        """
        decoded_text, current_bits = [], ""
        for bit in text:
            current_bits += bit
            if current_bits in self.__reversecode:
                decoded_text.append(self.__reversecode[current_bits])
                current_bits = ""
        return ''.join(decoded_text)

    def decompress(self):
        """
        Decompresses the Huffman encoded binary file back into its original text.
        """
        filename, _ = os.path.splitext(self.path)
        output_path = filename + '_decompressed.txt'
        
        with open(self.path, 'rb') as file:
            frequency_data = b""
            while True:
                byte = file.read(1)
                if not byte or byte == b'\n':
                    break
                frequency_data += byte
        
        try:
            frequency_dict = json.loads(frequency_data.decode("utf-8"))
        except Exception as e:
            raise ValueError("Error parsing frequency dictionary: " + str(e))
        
        self.__heap = []
        self.__build_heap(frequency_dict)
        self.__build_binary_tree()
        self.__build_tree_code()
        
        with open(self.path, 'rb') as file:
            file.readline()
            bit_string = ''.join(format(byte, '08b') for byte in file.read())
        
        if not bit_string:
            raise ValueError("Error: No encoded data found in file!")
        
        actual_text = self.__decode_text(self.__remove_padding(bit_string))
        
        with open(output_path, 'w', encoding="utf-8") as output:
            output.write(actual_text)
        
        return output_path

def print_huffman_codes(huffman_code_instance):
    """
    Prints the Huffman codes for all characters in the HuffmanCode instance.
    Args:
        huffman_code_instance (HuffmanCode): An instance of the HuffmanCode class.
    """
    result = []
    if not huffman_code_instance._HuffmanCode__code:
        print("No Huffman codes have been generated yet.")
        return

    print("Huffman Codes:")
    for char, code in huffman_code_instance._HuffmanCode__code.items():
        result.append([f"{char} = {code}"])
        print(f"{char} = {code}")
    return result