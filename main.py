import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5 import uic
from UI import form
from pytube import YouTube
import pytube.exceptions


class MyWidget(QMainWindow, form.Ui_Form):
    def __init__(self):
        super().__init__()
        self.init_UI()

    def init_UI(self):
        uic.loadUi("UI/download_video.ui", self)
        self.setFixedSize(564, 321)
        self.setWindowIcon(QIcon("icon.png"))
        self.download.clicked.connect(self.download_video)
        self.video_path.clicked.connect(self.assign_file_path)
        self.url_video.setPlaceholderText("Вставьте ссылку на видео")
        self.console.setReadOnly(True)
        self.file_path = ""

    def download_video(self):
        self.console.appendPlainText("Выполняется...")
        ok = self.checking_parameters()
        if ok:
            try:
                video = YouTube(self.url_video.text())
                video = video.streams.get_highest_resolution()
                video.download(self.file_path)
                self.console.appendPlainText(f"Видео сохранено в папку {self.file_path}")
            except pytube.exceptions.RegexMatchError:
                self.console.appendPlainText("Неверный URL видео или видео было удалено")

    def assign_file_path(self):
        self.file_path = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")

    def checking_parameters(self):
        if self.file_path.strip() == "":
            self.console.appendPlainText("Выберете директорию для сохранения видео")
            return False
        elif self.url_video.text().strip() == "":
            self.console.appendPlainText("Вставьте ссылку на видео")
            return False
        else:
            return True


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())