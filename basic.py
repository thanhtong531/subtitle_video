# # importing libraries 

import os,sys

from regex import F
from datetime import datetime

from srtToTxt import srt_to_txt
# from sosanh import check_similarity

from convert import handleFile






# Thời gian bắt đầu thực thi
start_time = datetime.now()

def mp4_to_wav(filename,name,output):
    # name = filename[filename.index('/'):filename.[]]
    os.system('ffmpeg -i {} -ar 44100 {}/{}.wav'.format(filename,output,name))

def noise_reduce(file,file_out):
    os.system('deepFilter {} -o {}'.format(file,file_out))

def rename(filename,newname):
        os.rename(filename, newname)
        

def wav_to_flac(filename,output):
    os.system('ffmpeg -y -f wav -i file3_DeepFilterNet2.wav -write_xing 0 -f flac file_video/file3_DeepFilterNet2.flac')


directory = ''
file_output = ''
lang_out = None
lang_in = None
path_txt = None
try: 
    directory = format(sys.argv[1])
    file_output = format(sys.argv[2])
    lang_in = format(sys.argv[3])
    lang_out = format(sys.argv[4])
    path_txt = format(sys.argv[5])
except:
    print('')

def wav_to_flac(filename,output):
    os.system('ffmpeg -y -f wav -i {} -write_xing 0 -f flac {}'.format(filename,output))

    

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
    all_file_srt = [doc for doc in os.listdir(directory) if (doc.endswith('.srt') )]
    
    
    #   kiểm tra file nào đã tạo phụ đề thì bỏ qua
    

    for index,file in enumerate(all_file_mp4):
            filename = directory + file
        # print(filename,file_output)
            name = file[:file.index('.mp4')]
            filewav = file.replace('mp4','wav')
            
            srt = name+'.srt'
            
            if srt in all_file_srt:
                continue

            # if not (name.find(name+'.srt')):
            mp4_to_wav(filename,name,file_output)
            # else:
                # continue
        
    # Giảm âm thanh nhiễu

            noise_reduce(file_output+filewav,file_output)
            deep = '_DeepFilterNet2.wav'
            # Sau khi giảm nhiễu
            rename(file_output+name+deep,file_output+name+'_nr'+'.wav')
            wav_to_flac(file_output+name+'_nr.wav',file_output+name+'.flac')
            # os.remove(directory+name+'_nr.wav')
            source = file_output+file.replace('.mp4','.flac')
            if lang_in == 'vi' and lang_out == 'en' or lang_out == None:
                flacToSrt(source)
            else:
                flacToSrt(source,lang_in,lang_out)

            # srt to txt train
            srt_to_txt(source.replace('.flac','.srt'),path_txt,name)
            handleFile(path_txt+'/'+name+'.txt',lang_out)
# # Thời gian kết thúc file


end_time = datetime.now()

# print(f'Thời gian chạy {str(end_time-start_time)}')
        







