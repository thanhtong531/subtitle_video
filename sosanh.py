from fileinput import filename
import os,re
import sys
from datetime import datetime
import time
from regex import P
from convert import handleFile

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.metrics.pairwise import cosine_similarity

def Tong(test_content):
    tong = len(re.findall(r'\w+', test_content))
    return tong

# Thời gian bắt đầu thực thi
start_time = datetime.now()


path = ''
path2 = ''
try:
# File train

    path = format(sys.argv[1]) + '/'
    train_files =[doc for doc in os.listdir(path) if (doc.endswith('.txt') )]

    path2 = format(sys.argv[2]) + '/'
    compare_files =[doc for doc in os.listdir(path2) if (doc.endswith('.txt') )]

except:
    print("")


# File so sanh
# path2 = "train/"




# for file in student_files:
#     print(file[:file.index('.')])
# 


def readfile(filename):
    file_input = open(filename, "r", encoding="utf-8")
    read_file = file_input.read()  # Đọc nội dung của File
    read_file = read_file.lower()
    return read_file

    



def check_similarity(file1,file2):
    vector1 = []

    read_file = readfile(file1)
    
    read_file2 = readfile(file2)

    vector1.append(read_file)
    vector1.append(read_file2)
    vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
    similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])
    vector = vectorize(vector1)
    result = similarity(vector[0],vector[1])[0][1]
    return round(result*100,5)

if __name__ == "__main__":
# print(check_similarity('train/tong.txt','fileSoSanh/tong_mau.txt'))
# tạo file luu ket qua trong thư mục fileKetQua
    today = datetime.today()

    time = today.strftime("%H") + "h" + today.strftime("%M")
    date = today.strftime("%Y-%m-%d") 

    dateVN = today.strftime("%d-%m-%Y")

    f = open( "fileKetQua/KetQuaCosine.txt" , 'w',encoding = 'utf-8')
    f.write("Thực hiện: "+str(time) + " " + str(dateVN) +"\n")

    f.write("\n==== ==== ==== ==== ==== ====\n")
    result = []
    i=0
    for train in train_files:
        file1 = path+train
        file2 = path2+train[:train.index('.')]+'_mau.txt'
        if(os.path.isfile(file2)==False):
            print('Đường dẫn thư mục {} không tồn tại'.format(file2))
            continue
        else:
            similarity = str(check_similarity(file1,file2)) 
        #     print(file1,file2)
        # print(str(round(check_similarity(vec)*100,5))+" %")
            kq = '{} so sanh voi {}: {} %'.format(train,train[:train.index('.')]+'_mau.txt',similarity)
            i+=1
            f.write(kq+"\n")
        result.append(kq)
    end_time = datetime.now()
    f.write('\n=> Tổng số có {} file đã thực thi '.format(i))
    f.write('\n=> Thời gian thực thi: '+str(end_time - start_time))

# print(result)








# tachfile = s_vectors[-1][0].split(".")
# f = open( "fileKetQua/KetQuaCosine.txt" , 'w',encoding = 'utf-8')



# #Lưu kết quả vào file
# f.write("Thực hiện: "+str(time) + " " + str(dateVN) +"\n")
# # f.write("\nTập tin  CTUD_QLDatPhong.docx ("+ str(Tong(test_notes[0])) +"):")
# f.write("\n==== ==== ==== ==== ==== ====\n")
# for data in check_plagiarism():
#     f.write(str(data) + "\n") 
    
    
# end_time = datetime.now()
# f.write('\n=> Thời gian thực thi: '+str(end_time - start_time))



# Thời gian kết thúc thực thi
# Thời gian kết thúc thực thi

 