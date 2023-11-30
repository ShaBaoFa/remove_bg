import tkinter as tk
from .application_gui import ApplicationGUI


def main():
    # Initialize the main window
    root = tk.Tk()
    root.title("文件上传到阿里云OSS")
    root.geometry("600x400")

    # Initialize and run the application GUI
    app = ApplicationGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
