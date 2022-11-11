import argparse
import os,sys

from regex import F
from datetime import datetime

from srtToTxt import srt_to_txt
# from sosanh import check_similarity

from convert import handleFile
import noisereduce as nr
import soundfile as sf
import librosa
from noisereduce.generate_noise import band_limited_noise

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dir', help="---> đường dẫn file cần chạy")
parser.add_argument('-o', '--dir_op', help='---> đường dẫn lưu trữ file')
parser.add_argument('-s', '--l_in', help='---> truyền ngôn ngữ file đầu vào')
parser.add_argument('-d', '--l_out', help='---> truyền ngôn ngữ file cần xuất',default="vi")
parser.add_argument('-txt', '--file_txt', help='---> chuyển về folder srt thành txt để so sánh độ chính xác')
args = parser.parse_args()





start_time = datetime.now()

def mp4_to_wav(filename,name,output):
    # name = filename[filename.index('/'):filename.[]]
    os.system('ffmpeg -i {} -ar 44100 {}/{}.wav'.format(filename,output,name))

def noise_reduce(file,file_out):
    y, sr = librosa.load(file)
    reduced_noise = nr.reduce_noise(y = y, sr=sr, thresh_n_mult_nonstationary=2,stationary=False)
    sf.write(file_out,reduced_noise, sr, subtype='PCM_24')
    print('Đã giảm tiếng ồn xong!')

def rename(filename,newname): 
    os.rename(filename, newname)
  
# If Source is a file 
# but destination is a directory




directory = ''
file_output = ''
lang_out = None
lang_in = None
path_txt = None
try: 
    directory = args.dir
    file_output = args.dir_op
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
    if directory != '' or file_output != None:
            directory =directory + '/'
            file_output = file_output + '/'
    all_file_mp4 = [doc for doc in os.listdir(directory) if (doc.endswith('.mp4') )]
    all_file_srt = [doc for doc in os.listdir(directory) if (doc.endswith('.srt') )]
    # kiểm tra file nào đã tạo phụ đề thì bỏ qua
    
        
    for index,file in enumerate(all_file_mp4):
            file_mp4 = directory + file
            name = file[:file.index('.mp4')]
            filewav = file.replace('mp4','wav')
        
    # Giảm âm thanh nhiễu
            srt = name+'.srt'
            if len(all_file_mp4) == len(all_file_srt):
                print('Tat ca cac file da hoan thanh')
                break
            if srt in all_file_srt:
                continue

            
            
            mp4_to_wav(file_mp4,name,file_output)
            
            noise_reduce(file_output+filewav,file_output+name+'_noise.wav')
            # Sau khi giảm nhiễu
            os.remove(file_output+filewav)
            rename(file_output+name+'_noise.wav',file_output+filewav)
            wav_to_flac(file_output+name+'.wav',file_output+name+'.flac')
            # os.remove(directory+name+'_nr.wav')
            source = file_output+file.replace('.mp4','.flac')
            if lang_in == 'vi' and lang_out == 'en' or lang_out == None:
                flacToSrt(source)
            else:
                flacToSrt(source,lang_in,lang_out)

            # srt to txt train
            srt_to_txt(source.replace('.flac','.srt'),path_txt,name)
            handleFile(path_txt+'/'+name+'.txt',lang_out)
            file_srt = source.replace('.flac','.srt')
            # videoOutput(file_mp4,file_srt,directory+name+'_output'+'.mp4')



# print(f'Thời gian chạy {str(end_time-start_time)}')
        







