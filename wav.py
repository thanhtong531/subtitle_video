import argparse
import os,sys

from regex import F
from datetime import datetime

from srtToTxt import srt_to_txt
# from sosanh import check_similarity

from convert import handleFile


parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dir', help="---> đường dẫn file cần chạy")
# parser.add_argument('-o', '--dir_op', help='---> đường dẫn lưu trữ file')
parser.add_argument('-s', '--l_in', help='---> truyền ngôn ngữ file đầu vào')
parser.add_argument('-d', '--l_out', help='---> truyền ngôn ngữ file cần xuất',default="vi")
parser.add_argument('-txt', '--file_txt', help='---> chuyển về folder srt thành txt để so sánh độ chính xác')
args = parser.parse_args()





start_time = datetime.now()

def mp4_to_wav(filename,output,name):
    # name = filename[filename.index('/'):filename.[]]
    os.system('ffmpeg -i {} -ar 44100 {}/{}.wav'.format(filename,output,name))

def noise_reduce(file,file_out):
    os.system('deepFilter {} -o {}'.format(file,file_out))

def rename(filename,newname): 
    os.rename(filename, newname)
  
# If Source is a file 
# but destination is a directory




directory = ''
lang_out = None
lang_in = None
path_txt = None
try: 
    directory = args.dir
    # file_output = args.dir_op
    lang_in = args.l_in
    lang_out = args.l_out
    path_txt = args.file_txt
except:
    print('')

def wav_to_flac(filename,output):
    os.system('ffmpeg -y -f wav -i {} -write_xing 0 -f flac {}'.format(filename,output))

    

def flacToSrt(source,lang_in='vi',lang_out=None):
    if lang_out == None:
        os.system('autosrt {} -S {}'.format(source,lang_in))
    else:
        os.system('autosrt {} -S {} -D {}'.format(source,lang_in,lang_out))

def videoOutput(file_in,file_srt,file_out):
        os.system('ffmpeg -y -i {} -filter_complex "subtitles={}" {}'.format(file_in,file_srt,file_out))


if __name__ == "__main__":
        path = directory[:directory.index("/")+1]
        # File nhập đầu vào
        file = directory[directory.index("/")+1:]
        if not (os.path.exists(path)):
            os.mkdir(path)
        
        name = file[:file.index('.mp4')]
        mp4_to_wav(path+file,path,name)     
       
        


        noise_reduce(path+name+'.wav',path)
        deep = '_DeepFilterNet2.wav'
            # # Sau khi giảm nhiễu
        rename(path+name+deep,path+name+'_nr'+'.wav')
        wav_to_flac(path+name+'_nr.wav',path+name+'.flac')
            # # os.remove(directory+name+'_nr.wav')
        source = path+name+'.flac'
        if lang_in == 'vi' and lang_out == 'en' or lang_out == None:
            flacToSrt(source)
        else:
            flacToSrt(source,lang_in,lang_out)

            
        if lang_in == lang_out:
            videoOutput(path+file,path+name+'.srt',path+name+'_output'+'.mp4')
        else:
            videoOutput(path+file,path+name+'_translated.srt',path+name+'_output'+'.mp4')



# print(f'Thời gian chạy {str(end_time-start_time)}')
        







