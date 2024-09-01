import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageFilter
import os


def blur_images(file_paths, blur_strength):
    """指定されたファイルにぼかし処理を適用"""
    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                # 画像にぼかしフィルタを適用
                blurred_image = img.filter(
                    ImageFilter.GaussianBlur(blur_strength))  # ぼかしの強さは調整可能

                # 保存先のパスを作成
                directory, filename = os.path.split(file_path)
                # 現在ディレクトリ+/blurredフォルダに保存する
                directory = os.path.join(directory, "blurred")
                os.makedirs(directory, exist_ok=True)
                save_path = os.path.join(directory, f"blurred_{filename}")

                # ぼかした画像を保存
                blurred_image.save(save_path)
                print(f"Saved blurred image: {save_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def open_files(blur_strength):
    """ファイル選択ダイアログを開いて、画像ファイルを選択する"""
    file_paths = filedialog.askopenfilenames(
        title="画像ファイルを選択してください",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    blur_images(file_paths, blur_strength)


def create_gui():
    """GUIを作成して表示する"""
    root = tk.Tk()
    root.title("画像ぼかしツール")

    # ウィンドウサイズを設定
    root.geometry("300x200")

    # ぼかしの強さを設定するスライダー
    tk.Label(root, text="ぼかしの強さ").pack()
    blur_strength = tk.IntVar(value=10)
    tk.Scale(root, from_=0, to_=100, orient=tk.HORIZONTAL,
             variable=blur_strength).pack()

    # 画像選択ボタン
    tk.Button(root, text="画像を選択", command=lambda: open_files(
        blur_strength.get())).pack(expand=True)

    # GUIのメインループを開始
    root.mainloop()


if __name__ == "__main__":
    create_gui()
