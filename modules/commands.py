import os
import webbrowser
import pywhatkit
import datetime
import psutil
import pyautogui
import requests

from modules.fetchData import get_weather, get_news 
from modules.spotify import SpotifyController

class CommandProcessor:
    def __init__(self):
        self.spotify = SpotifyController()
        self.commands = {
            "open file explorer": self.open_file_explorer,
            "open folder": self.open_folder,
            "open whatsapp": self.open_whatsapp,
            "open code": self.open_vscode,
            "open chatgpt": self.open_chatgpt,
            "open terminal": self.open_terminal,
            "open calculator": self.open_calculator,
            "open task manager": self.open_task_manager,
            "check battery": self.check_battery,
            "tell me the time": self.get_time,
            "increase volume": self.increase_volume,
            "decrease volume": self.decrease_volume,
            "mute volume": self.mute_volume,
            "unmute volume": self.unmute_volume,
            "play music": self.play_music,
            "play playlist" : self.play_playlist,
            "search google": self.google_search,
            "play youtube": self.play_youtube,
            "play song" : self.play_song,
            "shutdown": self.shutdown_pc,
            "restart": self.restart_pc,
            "lock pc": self.lock_pc,
            "take screenshot": self.take_screenshot,
            "open notepad": self.open_notepad,
            "open control panel": self.open_control_panel,
            "get weather": self.handle_weather,
            "weather in": self.handle_weather,
            "tell me the weather": self.handle_weather,
            "get news": self.handle_news,
            "tell me the news": self.handle_news,
            "exit": self.exit_program
        }

    def process_command(self, text):
        text = text.lower()

        for command, action in self.commands.items():
            if command in text:
                return action(text)

        print(f"⚠️ Unknown command received: {text}")
        return "Sorry User, I didn't understand that command. 🫤"

    def open_file_explorer(self, text):
        os.system("explorer")
        return "📂 Opening File Explorer for you!"

    def open_folder(self, text):
        path = text.replace("open folder", "").strip()
        if path:
            os.system(f'explorer "{path}"') 
            return f"📁 Opening {path}!"
        return "Please provide a folder path, User!"

    def open_whatsapp(self, text):
        os.system("start whatsapp://")
        return "💬 Opening WhatsApp for you!"

    def open_vscode(self, text):
        os.system("code")
        return "🧑‍💻 Launching VS Code!"
    
    def play_song(self, text):
        song_name = text.replace("play song", "").strip()
        if song_name:
            return self.spotify.play_song(song_name)
        return "Please tell me which song to play, User!"

    def play_playlist(self, text):
        playlist_name = text.replace("play playlist", "").strip()
        if playlist_name:
            return self.spotify.play_playlist(playlist_name)
        return "Please tell me which playlist to play, User!"

    def open_chatgpt(self, text):
        webbrowser.open("https://chat.openai.com")
        return "🤖 Opening ChatGPT!"

    def open_terminal(self, text):
        os.system("start cmd")
        return "⌨️ Opening Terminal!"

    def open_calculator(self, text):
        os.system("calc")
        return "🧮 Calculator is open!"

    def open_task_manager(self, text):
        os.system("taskmgr")
        return "📊 Opening Task Manager!"

    def check_battery(self, text):
        battery = psutil.sensors_battery()
        percent = battery.percent
        return f"🔋 Your system battery is at {percent}%."

    def get_time(self, text):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"⏰ User, the time is {now}."

    def increase_volume(self, text):
        pyautogui.press("volumeup", presses=5)
        return "🔊 Increasing volume!"

    def decrease_volume(self, text):
        pyautogui.press("volumedown", presses=5)
        return "🔉 Decreasing volume!"

    def mute_volume(self, text):
        pyautogui.press("volumemute")
        return "🔇 Muting volume!"

    def unmute_volume(self, text):
        pyautogui.press("volumemute")
        return "🔈 Unmuting volume!"

    def play_music(self, text):
        music_folder = r"D:\Music" 
        songs = os.listdir(music_folder)
        if songs:
            os.startfile(os.path.join(music_folder, songs[0]))
            return f"🎶 Playing {songs[0]}!"
        return "No music found in the folder!"

    def google_search(self, text):
        query = text.replace("search google", "").strip()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            return f"🌐 Searching Google for: {query}"
        return "What do you want to search, User?"

    def play_youtube(self, text):
        query = text.replace("play youtube", "").strip()
        if query:
            pywhatkit.playonyt(query)
            return f"📺 Playing {query} on YouTube!"
        return "Tell me what to play, User!"

    def handle_weather(self, text):
        city = "Delhi"
        if "in" in text:
            city = text.split("in")[-1].strip()
        return get_weather(city)

    def handle_news(self, text):
        return get_news()

    def shutdown_pc(self, text):
        os.system("shutdown /s /t 10")
        return "🛑 Shutting down in 10 seconds!"

    def restart_pc(self, text):
        os.system("shutdown /r /t 10")
        return "🔄 Restarting your PC shortly!"

    def lock_pc(self, text):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "🔒 Locking your PC!"

    def take_screenshot(self, text):
        screenshot = pyautogui.screenshot()
        screenshot.save("screenshot.png")
        return "📸 Screenshot taken and saved!"

    def open_notepad(self, text):
        os.system("notepad")
        return "📓 Opening Notepad!"

    def open_control_panel(self, text):
        os.system("control")
        return "🛠️ Opening Control Panel!"

    def exit_program(self, text):
        return "👋 Goodbye, Sagar! Have a great day."

if __name__ == "__main__":
    cp = CommandProcessor()
    # print(cp.process_command("get weather in Bangalore"))
    print(cp.process_command("play YouTube Arijit Singh Songs"))
