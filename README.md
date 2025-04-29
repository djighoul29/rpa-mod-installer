
# 📦 RPA Mod Installer  

## 📌 Description  

A tool for installing modifications in Ren'Py games with files packed into RPA archives.  
It is particularly useful for adding custom translations when the `tl` folder with localization files is archived.  
Additionally, it supports other types of modifications by allowing both overwriting existing files and adding new ones.  

This program was created on my own initiative to reduce the size of a fan-made [Ukrainian translation mod](https://steamcommunity.com/sharedfiles/filedetails/?id=3209395934) for the game _Slay the Princess_.  
At its core, it is a simple graphical interface, built with Tkinter, for the command-line tool [**rpatool**](https://github.com/shizmob/rpatool).  
The project also includes a pre-configured setup for **PyInstaller**, which allows everything to be packed into a single, convenient executable file.

---

## 🚀 How to Use  
### **0. Prerequisites**  
Ensure you have **Python 3** and **PyInstaller** installed on your PC.  

### **1. Customize the Installer**  
- Open **`installer.py`** and modify the last few lines to customize in-app text (e.g., links, credits).  
- Edit **`config.json`** to set the correct game title and file paths for your modification.  
- Replace **`icon.ico`** with your custom icon.  

### **2. Add Your Mod Files**  
Move your mod files into the **`mod/`** folder.  
For example, if you have a modified `screens.rpyc`, place it inside **`mod/`**.  

### **3. Modify the Build Configuration**  
- Open **`build.spec`**  
- Change the installer’s name by modifying:  
  ```
  name="rpa-mod-installer"
  ```
### **4. Build the Installer**  
- Run the following command in the project directory:
    ```sh
    py -m PyInstaller .\build.spec
    ```
- The compiled installer will appear in the newly created **`dist/`** folder.
### **5. Test & Distribute**

✅ Test your installer  
✅ Publish it  
✅ Share it with others  
✅ Enjoy modding your favorite Ren'Py games! 🎉

---

## 📜 License
This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it, as long as you include the original license and credit the author.  

