python -m venv venv
source venv/bin/activate

Xuất video => audio

Tạo nhìu file âm thanh check
để so sánh tương đồng

Cosine similarity

Yên tĩnh
Ngoài đường
music không lời

<!-- Tạo file output srt  + video gốc -->

ffmpeg -y -i "t.py" subtitles=subtitle1.srt output.mp4

# ffmpeg -y -i "file_cn/trung.mp4" -filter_complex "subtitles=file_cn/trung.srt" "output.mp4"

# ffmpeg -y -i "file_vi/file1.mp4" -filter_complex "subtitles=file_vi/file1.srt" "output.mp4"

ffmpeg -i file_video/file1.mp4 -acodec pcm_s16le -ar 16000 file1_ff.wav

ffmpeg -i file_video/file1.mp4 -ar 44100 file_video/file1_s.wav

ffmpeg -y -f wav -i file_video/file3_DeepFilterNet2.wav -write_xing 0 -f flac file_video/file3_DeepFilterNet2.flac


