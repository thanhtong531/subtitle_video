import os,re
import sys
from datetime import datetime
import time


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def Tong(test_content):
    tong = len(re.findall(r'\w+', test_content))
    return tong

# Thời gian bắt đầu thực thi
start_time = datetime.now()

# Đọc file trong thư mục có sẳn
path = format(sys.argv[1]) + "/"
student_files =[doc for doc in os.listdir(path) if (doc.endswith('.txt') )]
student_notes = [open(path+ _file, encoding='utf-8').read()
                 for _file in student_files]


# Đọc file trong dùng để kiểm tra
path2 = format(sys.argv[2]) + "/"
test_files =[doc for doc in os.listdir(path2) if (doc.endswith('.txt') )]

test_notes = [open(path2+ _file, encoding='utf-8').read()
                 for _file in test_files]


# Khởi tạo vector và hàm kiểm tra
vectorize = lambda Text: TfidfVectorizer().fit_transform(Text).toarray()
similarity = lambda doc1, doc2: cosine_similarity([doc1, doc2])    
vectors = vectorize(student_notes + test_notes)
s_vectors = list(zip(student_files + test_files, vectors))

# Kiểm tra độ tương tự bằng các chập 2 vector
plagiarism_results = set()
def check_plagiarism():
    global s_vectors
    student_a = s_vectors[0][0]
    text_vector_a =  s_vectors[-1][1]
    for student_b , text_vector_b in s_vectors[0:-1]:
        if(student_a==student_b) :
            continue           
        sim_score = similarity(text_vector_a, text_vector_b)[0][1]
        plagiarism_results.add((student_a, student_b, str(round(sim_score*100,4)) + "%"))
    return plagiarism_results 

# tạo file luu ket qua trong thư mục fileKetQua

tachfile = s_vectors[-1][0].split(".")
f = open( "fileKetQua/KetQuaCosine.txt" , 'w',encoding = 'utf-8')



today = datetime.today()
time = today.strftime("%H") + "h" + today.strftime("%M")
date = today.strftime("%Y-%m-%d")
dateVN = today.strftime("%d-%m-%Y")
#Lưu kết quả vào file
f.write("Thực hiện: "+str(time) + " " + str(dateVN) +"\n")
f.write("\nTập tin  ("+ str(Tong(test_notes[0])) +"):")
f.write("\n==== ==== ==== ==== ==== ====\n")
for data in check_plagiarism():
    f.write(str(data) + "\n") 
    
    
end_time = datetime.now()
f.write('\n=> Thời gian thực thi: '+str(end_time - start_time))



# Thời gian kết thúc thực thi
# Thời gian kết thúc thực thi