import os
import shutil
import platform
import subprocess
import time
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename

def get_config_paths():
    base_path = ""
    if platform.system() == 'Windows':
        base_path = os.path.join(os.environ['APPDATA'], 'PrusaSlicer')
    elif platform.system() == 'Darwin':
        base_path = os.path.join(os.environ['HOME'], 'Library', 'Application Support', 'PrusaSlicer')
    elif platform.system() == 'Linux':
        base_path = os.path.join(os.environ['HOME'], '.PrusaSlicer')
    else:
        raise Exception("Ukendt operativsystem")
    
    return {
        'printer': os.path.join(base_path, 'printer'),
        'filament': os.path.join(base_path, 'filament'),
        'print': os.path.join(base_path, 'print')
    }

def choose_file():
    root = Tk()
    root.withdraw()  # Vi vil ikke have et fuldt GUI, så dette fjerner det ekstra vindue
    filename = askopenfilename(title="Vælg konfigurationsfil (.ini)",
                               filetypes=(("INI files", "*.ini"), ("All files", "*.*")))
    root.destroy()  # Lukker det ekstra Tk vindue
    return filename

def copy_config_file(config_file, config_paths):
    for path in config_paths.values():
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
        shutil.copy(config_file, path)
        
    
def restart_prusaslicer():
    try:
        # Lukker PrusaSlicer, hvis det kører
        if platform.system() == 'Windows':
            subprocess.run(["taskkill", "/im", "prusa-slicer.exe", "/f"], check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.run(["pkill", "-f", "PrusaSlicer"], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif platform.system() == 'Linux':
            subprocess.run(["pkill", "-f", "PrusaSlicer"], check=False,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Fejl", f"Fejl ved lukning af PrusaSlicer: {e}")
    
    # Vent kort for at sikre, at processen er lukket helt
    time.sleep(1)
    
    # Starter PrusaSlicer igen
    try:
        # Sti til den eksekverbare PrusaSlicer-fil
        if platform.system() == 'Windows':
            prusa_executable = r"C:\Program Files\Prusa3D\PrusaSlicer\prusa-slicer.exe"
            subprocess.Popen(prusa_executable, shell=True)
        elif platform.system() == 'Darwin':  # macOS
            subprocess.Popen(["open", "-a", "PrusaSlicer"])
        elif platform.system() == 'Linux':
            subprocess.Popen(["PrusaSlicer"])
    except Exception as e:
        messagebox.showerror("Fejl", f"Fejl ved start af PrusaSlicer: {e}")
        

def main():
    config_file = choose_file()  # Brugeren vælger .ini filen
    if config_file:  # Tjekker om en fil blev valgt
        config_paths = get_config_paths()  # Få stierne til konfigurationsmapperne
        copy_config_file(config_file, config_paths)
        messagebox.showinfo("Succes", "Printerprofilerne er blevet impoteret - husk at give MakerSpace et Like på Facebook :)")
        user_response = messagebox.askyesno("Genstart PrusaSlicer", "Vil du genstarte PrusaSlicer nu?")
        if user_response:
            # Her kan du tilføje logikken til at åbne PrusaSlicer, hvis det er nødvendigt.
            # Sørg for, at PrusaSlicer's sti er korrekt, og at det kan kaldes på denne måde.
            # Det er muligt, at du skal specificere den fulde sti til PrusaSlicer-applikationen.
            if platform.system() == 'Windows':
                os.startfile(r"C:\Program Files\Prusa3D\PrusaSlicer\prusa-slicer.exe")
            elif platform.system() == 'Darwin':  # macOS
                subprocess.Popen(["open", "-a", "PrusaSlicer"])
            elif platform.system() == 'Linux':
                subprocess.Popen(["prusaslicer"])
    else:
        messagebox.showwarning("Advarsel", "Ingen fil blev valgt.")

if __name__ == '__main__':
    main()

