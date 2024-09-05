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
                save_path = os.path.join(directory, f"{filename}")

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

                # 保存先のパスを作成
                directory, filename = os.path.split(file_path)
                # 現在ディレクトリ+/mosaicフォルダに保存する
                directory = os.path.join(directory, "mosaic")
                os.makedirs(directory, exist_ok=True)
                save_path = os.path.join(directory, f"{filename}")

                # モザイク処理した画像を保存
                img.save(save_path)
                print(f"Saved mosaic image: {save_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")


def open_files(blur_strength, block_size, process_type):
    """ファイル選択ダイアログを開いて、画像ファイルを選択する"""
    file_paths = filedialog.askopenfilenames(
        title="画像ファイルを選択してください",
        filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.bmp;*.tiff")]
    )
    if process_type == "blur":
        blur_images(file_paths, blur_strength)
    elif process_type == "mosaic":
        mosaic_images(file_paths, block_size)


def create_gui():
    """GUIを作成して表示する"""
    root = tk.Tk()
    root.title("画像処理ツール")

    # ウィンドウサイズを設定
    root.geometry("300x300")

    # 処理タイプを選択するラジオボタン
    process_type = tk.StringVar(value="blur")
    tk.Radiobutton(root, text="ブラー", variable=process_type,
                   value="blur").pack()
    tk.Radiobutton(root, text="モザイク", variable=process_type,
                   value="mosaic").pack()

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

    # 画像選択ボタン
    tk.Button(root, text="画像を選択", command=lambda: open_files(
        blur_strength.get(), block_size.get(), process_type.get())).pack(expand=True)

    # GUIのメインループを開始
    root.mainloop()


if __name__ == "__main__":
    create_gui()
