# -*- coding:utf-8 -*-
__author__ = 'LiLei'
import numpy as np
from Huffman import createNodes,createHuffmanTree,huffmanEncoding
import struct

def count_freq(_array):
    unique, counts = np.unique(_array, return_counts=True)
    return unique.tolist(),counts.tolist()

def create_str_code(_arr,_dict):
    str_code = ''
    for item in _arr.copy().tolist():
        str_code = str_code+_dict[item]
    return str_code

def generate_num_code(_str):
    stored_num = []
    element = 0
    count = 0
    for index in range(len(_str)):
        element=element+int(_str[index])*(2**count)
        count=count+1
        if count == 8 or index == len(_str)-1:
            stored_num.append(element)
            count = 0
            element = 0

    return np.array(stored_num,dtype=np.uint8), len(_str)

'''
huffman_encode:
input: the array which will be compressed
return：
stored_num_arr: the array will be stored, which dtype is np.uint8
str_length:the length of string of binary code,while type should unsigned long long(8 bytes)
_codebook: the codebook,while type is dict
'''
def huffman_encode(_compressingArr):
    key_list,counts = count_freq(_compressingArr)
    nodes = createNodes(counts)
    root = createHuffmanTree(nodes)
    codec = huffmanEncoding(nodes,root)
    _codebook = dict(zip(key_list,codec))
    str_code = create_str_code(_compressingArr,_codebook)
    stored_num_arr, str_length = generate_num_code(str_code)
    return stored_num_arr, str_length, _codebook

'''
huffman_encode:
input:
stored_num_arr:the stored array
str_length:the length of string of binary code
codebook:the codebook
return:
original_num:the compressed array
'''
def huffman_decode(_huffman_info):
    stored_num_arr = _huffman_info[0]
    str_length = _huffman_info[1]
    codebook = _huffman_info[2]

    stored_num = stored_num_arr.tolist()
    str_code = ''
    for num in stored_num:
        num_bin_str = bin(num)[2:]   # from decimalism to binary
        if len(num_bin_str) != 8:
            num_bin_str = '0'*(8-len(num_bin_str)) + num_bin_str
        num_bin_str = num_bin_str[::-1]  # reverse
        str_code = str_code + num_bin_str
    str_code = str_code[:str_length]

    codebook_new = {value:key for key,value in codebook.items()}
    original_num = []
    whole_key = ''
    for ch in str_code:
        whole_key = whole_key+ch;
        if whole_key in codebook_new.keys():
            original_num.append(codebook_new[whole_key])
            whole_key = ''
    return np.array(original_num)


'''   beginning of store the codebook  '''
#B: unsigned char(1 bytes)
def huffman_store_keys(file, _keys_list):
    key_array = np.array(_keys_list, dtype=np.uint8)
    file.write(struct.pack('B', key_array.size))
    file.write(key_array.tobytes())


def huffman_store_values(file,_values_list):
    file.write(struct.pack('B', len(_values_list))) # store the num of values
    for value in _values_list:
        bvalue = bytes(value,encoding='utf-8')
        fmt = str(len(value))+'s'
        file.write(struct.pack('B', len(value)))
        file.write(struct.pack(fmt, bvalue))


def huffman_restore_keys(file):
    key_nums = np.fromfile(file, dtype=np.uint8, count=1)
    key_array = np.fromfile(file, dtype=np.uint8, count=key_nums[0])
    return key_array


def huffman_restore_values(file):
    result_arr = []
    result_list = []
    result_char = []
    values_nums = np.fromfile(file, dtype=np.uint8, count=1)
    for i in range(values_nums[0]):
        value_length = np.fromfile(file, dtype=np.uint8, count=1)
        result_arr.append(np.fromfile(file, dtype=np.uint8, count=value_length[0]))
    for item in result_arr:
        item = item.tolist()
        result_list.append(item)
    for item in result_list:
        char = ''
        for it in item:
            it = chr(it)
            char = char + it
        result_char.append(char)
    return result_char


'''   store the codebook ; input: _file: the file pointer ;_codebook_dict: the codebook'''
def huffman_store_codebook(_file, _codebook_dict):
    keys = list(_codebook_dict.keys())
    values = list(_codebook_dict.values())
    huffman_store_keys(_file, keys)
    huffman_store_values(_file, values)


'''   restore the codebook ;input: _file: the file pointer;return the codebook'''
def huffman_restore_codebook(_file):
    _restored_keys = huffman_restore_keys(_file)
    _restored_values = huffman_restore_values(_file)
    return dict(zip(_restored_keys,_restored_values))


'''   store the all huffman information  
input: 
_file: the file pointer
_huffman_info: the all huffman information,include stored num array,length of string, the codebook
Q: unsigned long long(8 bytes)
'''
def huffman_store(_file, _huffman_info):
    _stored_num_arr = _huffman_info[0]
    _str_length = _huffman_info[1]
    _codebook = _huffman_info[2]
    _file.write(struct.pack('Q', _stored_num_arr.size))
    _file.write(_stored_num_arr.tobytes())
    _file.write(struct.pack('Q', _str_length))
    huffman_store_codebook(_file, _codebook)


'''   restore the all huffman information  
input: 
_file: the file pointer
return:
_stored_num_arr:stored num array
_str_length:length of string
_codebook: the codebook
'''
def huffman_restore(_file):
    array_size = np.fromfile(_file, dtype=np.uint64, count=1)
    _stored_num_arr = np.fromfile(_file,dtype=np.uint8,count=array_size[0])
    _str_length = np.fromfile(_file, dtype=np.uint64, count=1)[0]
    _codebook = huffman_restore_codebook(_file)
    print("_codebook: ",_codebook)
    return _stored_num_arr, _str_length, _codebook


if __name__ == '__main__':
    # nums = 5000
    # arr = np.random.randint(0, 255, nums)
    # arr[0:int(nums*0.2)] = 0
    # print(arr)
    import cv2
    img_src = "data/freqStatics/1p.jpg"
    img_arr = cv2.imread(img_src)
    img_arr = img_arr.flatten()
    huffman_info = huffman_encode(img_arr)
    path = 'test'
    f = open(path, 'wb')
    huffman_store(f, huffman_info)
    f.close()

    # f1 = open(path, 'rb')
    # huffman_info_ = huffman_restore(f1)
    # original_arr = huffman_decode(huffman_info_)
    # print(original_arr)
    # f1.close()
