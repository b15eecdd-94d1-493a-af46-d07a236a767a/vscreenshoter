from moviepy import VideoFileClip
import os
from video_finder import VideoFinder

def get_filename_without_extension(file_path):
    # Получаем имя файла (без пути) и расширение
    filename_with_extension = os.path.basename(file_path)
    
    # Разделяем имя файла и расширение
    name, extension = os.path.splitext(filename_with_extension)
    
    # Возвращаем только имя файла без расширения
    return name

def last_directory(path):
    return os.path.basename(os.path.dirname(path))

class TimeConverter:
    def to_hours_minutes_and_seconds(self, total_seconds):
        hours = total_seconds // 3600
        remaining_seconds = total_seconds % 3600
        minutes = remaining_seconds // 60
        seconds = remaining_seconds % 60
        return hours, minutes, seconds

class VideoScreenshot:
    def __init__(self, video_file, output_directory, interval=10):
        self.video_file = video_file
        self.output_directory = output_directory
        self.interval = int(interval)  # Интервал в секундах
        print(self.output_directory)
        if not os.path.exists(self.output_directory):
            os.makedirs(self.output_directory)
    
    def capture_frames(self):
        clip = VideoFileClip(self.video_file)
        time_converter = TimeConverter()
        duration_hours, duration_minutes, duration_seconds = time_converter.to_hours_minutes_and_seconds(clip.duration)
        for i in range(0, int(clip.duration), self.interval):
            hours, minutes, seconds = time_converter.to_hours_minutes_and_seconds(i)
            if hours < 10:
                hours = '0' + str(hours)
            if minutes < 10:
                minutes = '0' + str(minutes)
            if seconds < 10:
                seconds = '0' + str(seconds)
            if duration_hours > 0:
                filename = str(hours) + ':' + str(minutes) + ':' + str(seconds)
            else:
                filename = str(minutes) + ':' + str(seconds)
            filename = os.path.join(self.output_directory, f"screenshot_{filename}.jpg")
            clip.save_frame(filename, t=i)
            print(f"Скриншот {filename} сохранен")

# Пример использования
if __name__ == "__main__":
    video_file = input('Укажите название файла или каталога: ')
    interval = input('Укажите интервал в секундах: ')
    output_directory = input('Укажите куда сохранять скриншоты: ')
    if video_file == False or video_file.strip() == '' or video_file == None:
        video_file = os.getcwd()
    if output_directory == False or output_directory.strip() == '' or output_directory == None:
        output_directory = os.getcwd() + '/screenshots'
    if video_file == output_directory:
        output_directory += '/screenshots'
    if os.path.isdir(video_file):
        video_paths = VideoFinder(video_file).find_videos()
        for video_file in video_paths:
            new_output_directory = output_directory + '/' + last_directory(video_file)
            screenshotter = VideoScreenshot(video_file, new_output_directory + '/' + get_filename_without_extension(video_file), interval)
            screenshotter.capture_frames() 
    elif os.path.isfile(video_file):
        screenshotter = VideoScreenshot(video_file, output_directory, interval)
        screenshotter.capture_frames()         
    else:
        print('Нету такого файла или каталога.')
