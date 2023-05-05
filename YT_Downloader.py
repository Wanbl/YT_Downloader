from pytube import Playlist, YouTube
from pydub import AudioSegment
import os

playlist_url = input("Entrez le lien de la playlist : ")
mode = input("Vidéo ou audio ? v/a : ")
playlist = Playlist(playlist_url)

# Récupération des informations de la playlist
print(f"Nom de la playlist : {playlist.title}")
print(f"Nombre de vidéos dans la playlist : {len(playlist.video_urls)}")

# Téléchargement des vidéos
for video_url in playlist.video_urls:
    retry_count = 0
    while True:
        try:
            video = YouTube(video_url)
            break
        except Exception as e:
            print(f"Impossible de récupérer les informations de la vidéo {video_url} : {str(e)}")
            retry_count += 1
            if retry_count >= 10:
                break

    if retry_count >= 10 or video is None:
        print(f"Nombre maximum de tentatives dépassé pour la vidéo {video_url}. Abandon du téléchargement.")
        continue
    
    retry_count = 0
    while True:
        try:
            if(mode == "a"):
                stream = video.streams.filter(only_audio=True, file_extension="mp4")
            else:
                stream = video.streams.filter(file_extension="mp4")
            if len(stream) == 0:
                print(f"Aucun stream disponible pour la vidéo {video_url} avec les critères spécifiés")
                break
            stream = stream.first()
            stream.download(output_path="downloads")
            break
        except Exception as e:
            print(f"Impossible de télécharger la vidéo {video_url} : {str(e)}")
            print(f"Essai numéro {retry_count}")
            retry_count += 1
            if retry_count >= 10:
                break

    print(f"Fin du téléchargement de la vidéo {video_url}")


# lister les fichiers dans le répertoire downloads
files = os.listdir("downloads")

# trier les fichiers par date de modification
files = sorted(files, key=lambda f: os.path.getmtime(os.path.join("downloads", f)))

# parcourir les fichiers et les convertir en mp3
if (mode == "a"):
    for file_name in files:
        try:
            if file_name.endswith(".mp4"):
                mp4_file = os.path.join("downloads", file_name)
                mp3_file = os.path.join("downloads", file_name[:-4] + ".mp3")
                sound = AudioSegment.from_file(mp4_file)
                sound.export(mp3_file, format="mp3")
                os.remove(mp4_file)
        except Exception as e:
            print(f"Impossible de convertir la vidéo {file_name} : {str(e)}")
"""
# Création des mp3 et suppression des mp4
for file_name in os.listdir("downloads"):
    try:
        if file_name.endswith(".mp4"):
            mp4_file = os.path.join("downloads", file_name)
            mp3_file = os.path.join("downloads", file_name[:-4] + ".mp3")
            sound = AudioSegment.from_file(mp4_file)
            sound.export(mp3_file, format="mp3")
            os.remove(mp4_file)
    except Exception as e:
        print(f"Impossible de convertir la vidéo {video_url} : {str(e)}")

"""