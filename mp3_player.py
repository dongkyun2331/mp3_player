import os
import pygame

def play_music(music_directory):
    # Pygame 초기화
    pygame.mixer.init()
    
    # 디렉토리에서 MP3 파일 목록 가져오기
    tracks = [f for f in os.listdir(music_directory) if f.endswith('.mp3')]
    if not tracks:
        print("No MP3 files found in the directory.")
        return

    # 무한 반복 재생
    while True:
        for track in tracks:
            track_path = os.path.join(music_directory, track)
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.play()
            
            # 현재 트랙이 끝날 때까지 대기
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

            print(f"Finished playing {track}, starting next.")

if __name__ == "__main__":
    music_dir = input("Enter the path to your music folder: ")
    play_music(music_dir)
