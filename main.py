from Lossless import *
from Lossy import *

if __name__ == '__main__':
    print("Choose the Type of Image Compression: \n 1) Lossy \n 2) Lossless \n")
    val = input("Enter the Option: ")
    fileName = input("Enter the imageName: ")
    input_dir = "C:\\Users\\Krishna Kumar K\\PycharmProjects\\Image_Compression\\venv\\Input_Data\\" + fileName
    file = fileName.split('.')
    output_dir = "C:\\Users\\Krishna Kumar K\\PycharmProjects\\Image_Compression\\venv\\Output_Data"
    output_path = output_dir + "\\compressed_" + file[0] + ".jpeg"
    if val == '2':
        print("Lossless")
        Lossless_compress_image_and_save(input_dir, output_path)
    else:
        print("Lossy")
        Lossy_compress_image_and_save(input_dir, output_dir)
