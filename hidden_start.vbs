Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\Gaming\Desktop\Dota2 W-L Overlay for OBS"
WshShell.Run "python main.py", 0, False