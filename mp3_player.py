import os
import pygame
import sys
import tkinter as tk
from tkinter import filedialog

def play_music(music_directory):
    # Pygame 초기화
    pygame.init()
    # 초기 화면 크기 설정
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    # 창의 제목 설정
    pygame.display.set_caption('Pygame Music Player')

    # 한글 폰트 파일 경로 설정
    font_path = 'NanumGothic-Regular.ttf'  # 폰트 파일 경로
    font_size = 24  # 폰트 크기
    font = pygame.font.Font(font_path, font_size)

    # 디렉토리에서 MP3 파일 목록 가져오기
    tracks = [f for f in os.listdir(music_directory) if f.endswith('.mp3')]
    # MP3 파일이 없으면 메시지 출력 후 종료
    if not tracks:
        print("디렉토리에 MP3 파일이 없습니다.")
        return

    # 현재 트랙의 인덱스 및 무한 재생 플래그
    track_index = 0
    repeat_one = False

    # 첫 번째 트랙 로드 및 재생
    pygame.mixer.music.load(os.path.join(music_directory, tracks[track_index]))
    pygame.mixer.music.play()

    # 음악 종료 이벤트 설정
    MUSIC_END = pygame.USEREVENT+1
    pygame.mixer.music.set_endevent(MUSIC_END)

    # 실행 상태 유지 변수
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # 창 크기 조정 이벤트에만 화면을 재설정
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
            elif event.type == pygame.KEYDOWN:
                # 스페이스바로 재생/일시정지
                if event.key == pygame.K_SPACE:
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                # 'n' 키로 다음 트랙 재생
                elif event.key == pygame.K_n:
                    if not repeat_one:
                        track_index = (track_index + 1) % len(tracks)
                        pygame.mixer.music.load(os.path.join(music_directory, tracks[track_index]))
                        pygame.mixer.music.play()
                # 'p' 키로 이전 트랙 재생
                elif event.key == pygame.K_p:
                    if not repeat_one:
                        track_index = (track_index - 1 + len(tracks)) % len(tracks)
                        pygame.mixer.music.load(os.path.join(music_directory, tracks[track_index]))
                        pygame.mixer.music.play()
                # 'r' 키로 현재 곡 무한 반복 토글
                elif event.key == pygame.K_r:
                    repeat_one = not repeat_one
                    pygame.mixer.music.play(-1 if repeat_one else 1)
            elif event.type == MUSIC_END:
                if not repeat_one:
                    # 현재 곡이 끝나면 자동으로 다음 곡 재생
                    track_index = (track_index + 1) % len(tracks)
                    pygame.mixer.music.load(os.path.join(music_directory, tracks[track_index]))
                    pygame.mixer.music.play()
        
        # 화면 배경을 진한 회색으로 채우기
        screen.fill((50, 50, 50))
        # 현재 재생 중인 트랙 정보 표시
        current_track_text = font.render(f'Current track: {tracks[track_index]}', True, (70, 130, 180))
        screen.blit(current_track_text, (20, 50))

        # 플레이리스트 표시
        playlist_y = 100
        for i, track in enumerate(tracks):
            if i == track_index:
                track_text = font.render(track, True, (255, 0, 0) if repeat_one and i == track_index else (70, 130, 180))
            else:
                track_text = font.render(track, True, (255, 255, 255))
            screen.blit(track_text, (20, playlist_y))
            playlist_y += 30

        # 화면 업데이트
        pygame.display.flip()
        # 프레임 속도 조절
        pygame.time.Clock().tick(30)
    
    # Pygame 종료
    pygame.quit()
    sys.exit()

def select_music_directory():
    # tkinter를 사용하여 폴더 선택 창을 띄우기
    root = tk.Tk()
    root.withdraw()  # tkinter 창 숨기기
    music_directory = filedialog.askdirectory()
    root.destroy()
    return music_directory

if __name__ == "__main__":
    # UI에서 음악 폴더 경로 입력 받기
    music_dir = select_music_directory()
    if music_dir:
        play_music(music_dir)
    else:
        print("음악 폴더를 선택하지 않았습니다.")
