import os, sys, getopt
import time
from multiprocessing import Process, Queue
import cv2
import numpy as np
from encryption.ImageEncryption import ImageEncryption
from encryption.KnuthShuffle import KnuthShuffle
from slicing.Slicer import Slicer
from util import Utility as Util

def encrypt(password, img_name, out_name):
    print('Encryption started.')
    image_file_name = img_name
    encrypted_image_file_name = out_name

    img = cv2.imread(image_file_name)

    height = int(len(img))
    width = int(len(img[0]))

    array_slicer = Slicer(img, height, width)
    img_top_left, img_top_right, img_bottom_left, img_bottom_right = array_slicer.slice()

    np.random.seed(int(password))

    shuffle = KnuthShuffle()
    s_box = shuffle.create_s_box(np.random)

    random_numbers = np.random.randint(0, 16, (height, width, 6))
    array_slicer.set_array(random_numbers)
    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    image_encryption = ImageEncryption()

    start = time.perf_counter()

    result_queue = Queue()

    procs = []
    proc1 = Process(target=image_encryption.encrypt, args=(s_box, rand_top_left, img_top_left, result_queue, 1))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.encrypt, args=(s_box, rand_top_right, img_top_right, result_queue, 2))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.encrypt, args=(s_box, rand_bottom_left, img_bottom_left, result_queue, 3))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.encrypt, args=(s_box, rand_bottom_right, img_bottom_right, result_queue, 4))
    procs.append(proc4)
    proc4.start()

    image_slice_list = [result_queue.get() for i in range(4)]
    image_slice_list.sort(key=Util.sort_second)

    for proc in procs:
        proc.join()

    finish = time.perf_counter()

    print('Finished in {} second(s)'.format(finish - start))


    encrypted_image = Slicer.concatenate(image_slice_list[0][0], image_slice_list[1][0], image_slice_list[2][0],
                                         image_slice_list[3][0])
    cv2.imwrite(encrypted_image_file_name, encrypted_image)


    return True

def decrypt(password, img_name, out_name):
    print('Decryption started.')
    encrypted_image_file_name = img_name
    decrypted_image_file_name = out_name

    en_img = cv2.imread(encrypted_image_file_name)

    height = int(len(en_img))
    width = int(len(en_img[0]))

    array_slicer = Slicer(en_img, height, width)
    en_img_top_left, en_img_top_right, en_img_bottom_left, en_img_bottom_right = array_slicer.slice()

    np.random.seed(int(password))

    shuffle = KnuthShuffle()
    s_box = shuffle.create_s_box(np.random)
    inverse_s_box = shuffle.create_inverse_s_box()

    random_numbers = np.random.randint(0, 16, (height, width, 6))
    array_slicer.set_array(random_numbers)
    rand_top_left, rand_top_right, rand_bottom_left, rand_bottom_right = array_slicer.slice()

    image_encryption = ImageEncryption()

    start = time.perf_counter()

    result_queue = Queue()

    procs = []
    proc1 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_top_left, en_img_top_left, result_queue, 1))
    procs.append(proc1)
    proc1.start()

    proc2 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_top_right, en_img_top_right, result_queue, 2))
    procs.append(proc2)
    proc2.start()

    proc3 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_bottom_left, en_img_bottom_left, result_queue, 3))
    procs.append(proc3)
    proc3.start()

    proc4 = Process(target=image_encryption.decrypt,
                    args=(s_box, inverse_s_box, rand_bottom_right, en_img_bottom_right, result_queue, 4))
    procs.append(proc4)
    proc4.start()

    image_slice_list = [result_queue.get() for i in range(4)]
    image_slice_list.sort(key=Util.sort_second)

    for proc in procs:
        proc.join()

    finish = time.perf_counter()

    print('Finished in {} second(s)'.format(finish - start))

    cv2.imwrite('results/dec_top_left.png', image_slice_list[0][0])
    cv2.imwrite('results/dec_top_right.png', image_slice_list[1][0])
    cv2.imwrite('results/dec_bottom_left.png', image_slice_list[2][0])
    cv2.imwrite('results/dec_bottom_right.png', image_slice_list[3][0])

    decrypted_image = Slicer.concatenate(image_slice_list[0][0], image_slice_list[1][0], image_slice_list[2][0],
                                        image_slice_list[3][0])
    cv2.imwrite(decrypted_image_file_name, decrypted_image)

    return True

def main(argv):
    inputfile = ''
    outputfile = ''
    password = ''
    try:
          opts, args = getopt.getopt(argv,"hi:o:p:",["ifile=","ofile=","password="])
    except getopt.GetoptError:
          print('test.py -i <inputfile> -o <outputfile> -p <password>')
          sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-p", "--password"):
            password = arg

    if sys.argv[1] == 'enc':
        encrypt(password ,inputfile, outputfile)
    elif sys.argv[1] == 'dec':
        decrypt(password ,inputfile, outputfile)

if __name__ == '__main__':
    main(sys.argv[2:])