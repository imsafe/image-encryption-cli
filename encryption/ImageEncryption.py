from util import Utility as Util


class ImageEncryption:

    def encrypt(self, s_box, random_numbers, im, result_queue, image_id):
        for i in range(len(im)):
            for j in range(len(im[0])):
                b, g, r = im[i][j]

                hex_r = Util.convert_dec_to_hex(r)
                hex_g = Util.convert_dec_to_hex(g)
                hex_b = Util.convert_dec_to_hex(b)

                row_r = int(hex_r[0], 16)
                column_r = int(hex_r[1], 16)

                row_g = int(hex_g[0], 16)
                column_g = int(hex_g[1], 16)

                row_b = int(hex_b[0], 16)
                column_b = int(hex_b[1], 16)

                new_r = int(s_box[random_numbers[i][j][0], random_numbers[i][j][1]], 16) ^ int(s_box[row_r, column_r], 16)
                new_g = int(s_box[random_numbers[i][j][2], random_numbers[i][j][3]], 16) ^ int(s_box[row_g, column_g], 16)
                new_b = int(s_box[random_numbers[i][j][4], random_numbers[i][j][5]], 16) ^ int(s_box[row_b, column_b], 16)

                im[i, j] = new_b, new_g, new_r

        result_queue.put((im, image_id))

    def decrypt(self, s_box, inverse_s_box, random_numbers, im, result_queue, image_id):
        for i in range(len(im)):
            for j in range(len(im[0])):
                b, g, r = im[i][j]

                hex_r = Util.convert_dec_to_hex(r)
                hex_g = Util.convert_dec_to_hex(g)
                hex_b = Util.convert_dec_to_hex(b)

                new_r = int(s_box[random_numbers[i][j][0], random_numbers[i][j][1]], 16) ^ int(hex_r, 16)
                new_g = int(s_box[random_numbers[i][j][2], random_numbers[i][j][3]], 16) ^ int(hex_g, 16)
                new_b = int(s_box[random_numbers[i][j][4], random_numbers[i][j][5]], 16) ^ int(hex_b, 16)

                new_r = Util.convert_dec_to_hex(new_r)
                new_g = Util.convert_dec_to_hex(new_g)
                new_b = Util.convert_dec_to_hex(new_b)

                im[i, j] = int(inverse_s_box[int(new_b[0], 16), int(new_b[1], 16)], 16), int(
                    inverse_s_box[int(new_g[0], 16), int(new_g[1], 16)], 16), int(
                    inverse_s_box[int(new_r[0], 16), int(new_r[1], 16)],
                    16)

        result_queue.put((im, image_id))
        