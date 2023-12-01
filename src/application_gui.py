import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from cloud_service import CloudService
from image_processor import ImageProcessor


class ApplicationGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("文件上传到阿里云OSS")
        self.root.geometry("600x400")

        self.cloud_service = CloudService()
        self.image_processor = ImageProcessor()

        self.setup_widgets()

    def setup_widgets(self):
        # Create and place widgets
        self.button = tk.Button(self.root, text="选择文件并上传", command=self.select_file)
        self.button.pack(pady=20)

        self.remove_button = tk.Button(self.root, text="去除背景并下载到本地", command=self.remove_bg_save_to_local)
        self.remove_button.pack(pady=20)

        self.ddl = ttk.Combobox(self.root, width=12)
        self.ddl['values'] = ('red', 'blue', 'green')
        self.ddl.pack(pady=20)
        # 绑定选择事件
        self.ddl.bind("<<ComboboxSelected>>", self.on_combobox_selected)

        self.label = tk.Label(self.root, text="")
        self.label.pack()

        self.image_label = tk.Label(self.root)
        self.image_label.pack()

    def select_file(self):
        # File selection and upload logic
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return

        # Displaying message on label
        self.label.config(text=f"处理中...")

        try:
            self.cloud_service.upload_file(file_path)
            # Here you would call the cloud service methods to upload the file
            # and get the URL of the uploaded image
            # For example: url = self.cloud_service.upload_file(file_path)

            # Simulating a URL for demonstration purposes
            self.cloud_service.get_signed_url(self.cloud_service.last_uploaded_file_name)
            self.image_processor.show_image(self.cloud_service.last_uploaded_file_url, self.image_label)
            self.label.config(text=f"已上传: {file_path}")
        except Exception as e:
            self.label.config(text=f"上传失败: {e}")

    # Additional GUI methods can be added here
    def remove_bg_save_to_local(self):
        self.image_processor.remove_bg(self.cloud_service.last_uploaded_file_url)

    def on_combobox_selected(self, event):
        print("选中事件")
        ddl_value = self.ddl.get()
        self.image_processor.selected_color = ddl_value
        print(ddl_value)