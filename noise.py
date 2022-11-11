import argparse
import os,sys,shutil

from regex import F
from datetime import datetime
import noisereduce as nr
from noisereduce.generate_noise import band_limited_noise
from srtToTxt import srt_to_txt
import librosa
import soundfile as sf



from convert import handleFile

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--dir', help="---> đường dẫn file cần chạy")
parser.add_argument('-o', '--dir_op', help='---> đường dẫn lưu trữ file')
parser.add_argument('-s', '--l_in', help='---> truyền ngôn ngữ file đầu vào',default='vi')
parser.add_argument('-d', '--l_out', help='---> truyền ngôn ngữ file cần xuất',default="vi")
parser.add_argument('-txt', '--file_txt', help='---> chuyển về folder srt thành txt để so sánh độ chính xác')
args = parser.parse_args()





start_time = datetime.now()

def mp4_to_wav(filename,name,output):
    os.system('ffmpeg -i {} -ar 44100 {}/{}.wav'.format(filename,output,name))

def noise_reduce(file,file_out):
    y, sr = librosa.load(file)
    reduced_noise = nr.reduce_noise(y = y, sr=sr, thresh_n_mult_nonstationary=2,stationary=False)
    sf.write(file_out,reduced_noise, sr, subtype='PCM_24')


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
    os.system('ffmpeg -i {} -af aformat=s16:44100 {}'.format(filename,output))

def flacToSrt(source,lang_in='vi',lang_out=None):
    if lang_out == None:
        os.system('autosrt {} -S {}'.format(source,lang_in))
    else:
        os.system('autosrt {} -S {} -D {}'.format(source,lang_in,lang_out))



if __name__ == "__main__":
    if directory != '' or file_output != None:
            directory =directory + '/'
            file_output = file_output + '/'
    all_file_mp4 = [doc for doc in os.listdir(directory) if (doc.endswith('.mp4') )]
    
    # kiểm tra file nào đã tạo phụ đề thì bỏ qua
    
        
    for index,file in enumerate(all_file_mp4):
            filename = directory + file
            name = file[:file.index('.mp4')]
            filewav = file.replace('mp4','wav')

            if os.path.exists(file_output+filewav):
                os.remove(file_output+filewav)
            # if(os.path.exists('file_noise')):
            #     shutil.rmtree('file_noise')
            #     os.mkdir('file_noise')
            # break
            mp4_to_wav(filename,name,file_output)
   
            noise_reduce(file_output+filewav,file_output+name+'_rd.wav')
            
            # Sau khi giảm nhiễu
            wav_to_flac(file_output+name+'_rd.wav',file_output+name+'_rd.flac')
            source = file_output+name+'_rd.flac'
            if lang_in == 'vi' and lang_out == 'en' or lang_out == None:
                flacToSrt(source)
            else:
                flacToSrt(source,lang_in,lang_out)

            # srt to txt train
            srt_to_txt(source.replace('.flac','.srt'),path_txt,name)
            handleFile(path_txt+'/'+name+'.txt',lang_out)



# print(f'Thời gian chạy {str(end_time-start_time)}')
        







