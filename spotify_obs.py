import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import requests
from pathlib import Path

# Настройки для Spotify API
CLIENT_ID = '99405a951db947109fcde43a8474f986'  # Замени на свой Client ID
CLIENT_SECRET = '4e818d43c0714b06a9475bd241bdb985'  # Замени на свой Client Secret
REDIRECT_URI = 'http://127.0.0.1:8080'  # Или другой Redirect URI, который ты указал

# Настройка аутентификации
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri=REDIRECT_URI,
                                               scope='user-read-currently-playing'))

def get_current_track():
    try:
        # Получаем информацию о текущем треке
        current_track = sp.current_user_playing_track()
        if current_track is None:
            return "Нет активного трека", None

        track_name = current_track['item']['name']
        artist_name = current_track['item']['artists'][0]['name']
        # Получаем URL обложки
        image_url = current_track['item']['album']['images'][0]['url'] if current_track['item']['album']['images'] else None

        # Форматируем название трека для прокрутки
        full_text = f"{track_name} - {artist_name}"
        MAX_LENGTH = 50  # Максимальная длина текста перед прокруткой

        if len(full_text) > MAX_LENGTH:
            # Создаем эффект бегущей строки, добавляя пробелы в начале и конце
            padding = " " * 10  # Добавляем отступы для плавности
            scrolling_text = padding + full_text + padding
            formatted_text = scrolling_text
        else:
            formatted_text = full_text

        return formatted_text, image_url

    except Exception as e:
        return f"Ошибка: {str(e)}", None

def download_image(image_url, filename='current_album_cover.jpg'):
    if image_url:
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            with open(filename, 'wb') as file:
                file.write(response.content)
            return True
        except Exception as e:
            print(f"Ошибка при скачивании изображения: {str(e)}")
            return False
    return False

def update_obs_file():
    while True:
        # Получаем текущий трек и URL обложки
        track_info, image_url = get_current_track()
        
        # Записываем название трека в текстовый файл
        with open('current_song.txt', 'w', encoding='utf-8') as file:
            file.write(track_info)
        
        # Скачиваем и сохраняем обложку, если она есть
        if image_url:
            success = download_image(image_url)
            if success:
                print(f"Обложка обновлена: {image_url}")
            else:
                print("Не удалось обновить обложку.")
        else:
            print("Обложка не найдена для текущего трека.")
        
        print(f"Обновлено: {track_info}")
        # Обновляем каждые 5 секунд
        time.sleep(5)

if __name__ == "__main__":
    print("Программа запущена. Авторизуйся в Spotify, если потребуется.")
    update_obs_file()