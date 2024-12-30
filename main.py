from PIL import Image, ImageFilter
import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES


def blur_images(file_paths, blur_strength):
    """指定されたファイルにぼかし処理を適用"""
    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                # 画像にぼかしフィルタを適用
                blurred_image = img.filter(
                    ImageFilter.GaussianBlur(blur_strength))  # ぼかしの強さは調整可能

                # 保存先のパスを作成（元のファイルを上書き）
                save_path = file_path

                # ぼかした画像を保存
                blurred_image.save(save_path)
                print(f"Saved blurred image: {save_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def mosaic_images(file_paths, block_size):
    """指定されたファイルにモザイク処理を適用"""
    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                # 画像サイズを取得
                width, height = img.size

                # モザイク処理を適用
                for x in range(0, width, block_size):
                    for y in range(0, height, block_size):
                        # ブロックの範囲を計算
                        box = (x, y, x + block_size, y + block_size)
                        # ブロックを切り出し
                        block = img.crop(box)
                        # ブロックの平均色を計算
                        avg_color = block.resize((1, 1)).resize(block.size)
                        # ブロックを平均色で塗りつぶす
                        img.paste(avg_color, box)

                # 保存先のパスを作成（元のファイルを上書き）
                save_path = file_path

                # モザイク処理した画像を保存
                img.save(save_path)
                print(f"Saved mosaic image: {save_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def resize_images(file_paths, resize_percentage):
    """指定されたファイルのサイズを変更"""
    for file_path in file_paths:
        try:
            with Image.open(file_path) as img:
                # 画像サイズを取得
                width, height = img.size
                # 新しいサイズを計算
                new_width = int(width * resize_percentage / 100)
                new_height = int(height * resize_percentage / 100)
                # 画像サイズを変更
                resized_image = img.resize((new_width, new_height))

                # 保存先のパスを作成（元のファイルを上書き）
                save_path = file_path

                # サイズ変更した画像を保存
                resized_image.save(save_path)
                print(f"Saved resized image: {save_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def get_all_image_files(directory):
    """指定されたディレクトリ内のすべての画像ファイルを再帰的に取得"""
    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                image_files.append(os.path.join(root, file))
    return image_files


def open_files(blur_strength, block_size, resize_percentage, process_type, file_paths=None):
    """ファイル選択ダイアログを開いて、画像ファイルを選択する"""
    if not file_paths:
        file_paths = filedialog.askopenfilenames(
            title="画像ファイルを選択してください",
            filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
        )
    all_files = []
    for path in file_paths:
        if os.path.isdir(path):
            all_files.extend(get_all_image_files(path))
        else:
            all_files.append(path)

    # 確認ダイアログを表示
    if messagebox.askyesno("確認", "破壊的な処理だけど実行する？バックアップとった？"):
        if process_type == "blur":
            blur_images(all_files, blur_strength)
        elif process_type == "mosaic":
            mosaic_images(all_files, block_size)
        elif process_type == "resize":
            resize_images(all_files, resize_percentage)


def drop(event, blur_strength, block_size, resize_percentage, process_type):
    """ドラッグアンドドロップされたファイルを処理する"""
    # ファイルパスの波括弧を削除し、エスケープシーケンスを正しく処理
    file_paths = [path.strip('{}') for path in event.data.split()]
    open_files(blur_strength, block_size,
               resize_percentage, process_type, file_paths)


def create_gui():
    """GUIを作成して表示する"""
    root = TkinterDnD.Tk()
    root.title("画像処理ツール")

    # ウィンドウサイズを設定
    root.geometry("300x400")

    # 処理タイプを選択するラジオボタン
    process_type = tk.StringVar(value="blur")
    tk.Radiobutton(root, text="ブラー", variable=process_type,
                   value="blur").pack()
    tk.Radiobutton(root, text="モザイク", variable=process_type,
                   value="mosaic").pack()
    tk.Radiobutton(root, text="サイズ変更", variable=process_type,
                   value="resize").pack()

    # ぼかしの強さを設定するスライダー
    tk.Label(root, text="ぼかしの強さ").pack()
    blur_strength = tk.IntVar(value=5)
    tk.Scale(root, from_=0, to_=20, orient=tk.HORIZONTAL,
             variable=blur_strength).pack()

    # モザイクのブロックサイズを設定するスライダー
    tk.Label(root, text="モザイクのブロックサイズ").pack()
    block_size = tk.IntVar(value=10)
    tk.Scale(root, from_=1, to_=50, orient=tk.HORIZONTAL,
             variable=block_size).pack()

    # サイズ変更のパーセンテージを設定するテキストボックス
    tk.Label(root, text="サイズ変更のパーセンテージ").pack()
    resize_percentage = tk.StringVar(value="50")
    tk.Entry(root, textvariable=resize_percentage).pack()

    # 画像選択ボタン
    tk.Button(root, text="画像を選択", command=lambda: open_files(
        blur_strength.get(), block_size.get(), int(resize_percentage.get()), process_type.get())).pack(expand=True)

    # ドラッグアンドドロップの設定
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', lambda event: drop(
        event, blur_strength.get(), block_size.get(), int(resize_percentage.get()), process_type.get()))

    # GUIのメインループを開始
    root.mainloop()


if __name__ == "__main__":
    create_gui()
