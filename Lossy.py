import scipy.fftpack as fftpack
import zlib
from utils import *
import getopt, sys
class jpeg:
    def __init__(self, im, quants):
        self.image = im
        self.quants = quants
        super().__init__()
    def encode_quant(self, quant):
        return (self.enc / quant).astype(int)

    def decode_quant(self, quant):
        return (self.encq * quant).astype(float)
    
    def encode_dct(self, bx, by):
        new_shape = (
            self.image.shape[0] // bx * bx,
            self.image.shape[1] // by * by,
            3
        )
        new = self.image[
              :new_shape[0],
              :new_shape[1]
              ].reshape((
            new_shape[0] // bx,
            bx,
            new_shape[1] // by,
            by,
            3
        ))
        return fftpack.dctn(new, axes=[1, 3], norm='ortho')
    def decode_dct(self, bx, by):
        return fftpack.idctn(self.decq, axes=[1, 3], norm='ortho'
                             ).reshape((
            self.decq.shape[0] * bx,
            self.decq.shape[2] * by,
            3
        ))
    def encode_zip(self):
        return zlib.compress(self.encq.astype(np.int8).tobytes())
    def decode_zip(self):
        return np.frombuffer(zlib.decompress(self.encz), dtype=np.int8).astype(float).reshape(self.encq.shape)

    def intiate(self, qscale, bx, by,output_dir):
        quant = (
            (np.ones((bx, by)) * (qscale * qscale))
            .clip(-100, 100)  # to prevent clipping
            .reshape((1, bx, 1, by, 1))
        )
        self.enc = self.encode_dct(bx, by)
        self.encq = self.encode_quant(quant)
        self.encz = self.encode_zip()
        self.decz = self.decode_zip()
        self.decq = self.decode_quant(quant)
        self.dec = self.decode_dct(bx, by)
        img_bgr = ycbcr2rgb(self.dec)
        cv2.imwrite("{}/compressed_quant_{}.jpeg".format(
            output_dir, qscale), img_bgr.astype(np.uint8))

def Lossy_compress_image_and_save(input_dir, output_dir):
    quant_size = 5
    block_size = 8

    im = cv2.imread(input_dir)

    #Subsampling an Image by a factor of 2

    im = cv2.resize(im, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_LINEAR)

    Ycr = rgb2ycbcr(im);
    obj = jpeg(Ycr, [5])
    quants = [quant_size]
    blocks = [(block_size, block_size)]
    for qscale in quants:
        for bx, by in blocks:
            obj.intiate(qscale, bx, by,output_dir)
