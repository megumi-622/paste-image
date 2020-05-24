from PIL import Image
import os.path, json


def check_setting_file(file_name):
    """
    設定ファイルを確認＆値取得  

    Parameter:
    ----------
        file_name: string
            設定用jsonファイル名 *.json
    Returns:
    ----------
        list
            flag: Boolean
                設定ファイル読み混み可否
            msg: string
                jsonファイルの内容かエラーメッセージ
    """

    # エラー判定用
    flag = False

    try:
        json_open = open(file_name, "r")
    except FileNotFoundError as e:
        return flag, "setting.jsonがありません"
    else:
        # msg = json.load(json_open)
        msg = json_open
        flag = True

        return flag, msg


def img_check(file_path):
    """
    画像があるかどうか確認
    Parameters
    ----------
    file_path: string
        画像ファイルパス

    Returns
    ----------
    flag: boolean
    """
    try:
        if os.path.exists(file_path):
            return True
    except Exception:
        return False


class image_obi:

    def rename(self, file_path, cnt=1):
        """
        ファイル名を変更する

        Parameters
        ----------
        file_path: string
            画像ファイル名

        Returns
        ----------
        new_path: fspath
            新しいファイルパス
        """
        #ファイル名と拡張子をわける
        ftitle, fext = os.path.splitext(str(file_path))

        # ファイル名と0埋め数値と拡張子を結合
        new_file_name = "{}-{:03}{}".format(ftitle, cnt, fext)
        # 新しいファイル名をパス化する
        new_path = os.fspath(new_file_name)

        if os.path.exists(new_path):
            # 同一名ファイルが存在したら再度renameを行う
            image = image_obi()
            return image.rename(file_path, cnt=cnt+1)
        else:
            return new_path

        if __name__ == "__main__":
            rename()


    def synthesis(self, main_img, obi_img):
        """
        画像を合成する

        Parameters
        ----------
        file_path: string
            画像ファイル名
        img_path: string
            上部に貼り付ける画像
        """

        obi_flag = img_check(obi_img)

        if not obi_flag:
            return (False, "帯用画像がありません")

        main_flag = img_check(main_img)

        if not main_flag:
            return (False, "メイン用画像がありません")

        # 上部に合成する画像を開く
        obi = Image.open(obi_img)

        # メイン画像を開く
        img = Image.open(main_img)
    
        # 上部に貼り付ける画像サイズ
        obi_width, obi_height = obi.size

        # メイン画像のサイズ
        img_width, img_height = img.size

        if obi_width <= 0 or img_width <= 0:
            return (False, "画像サイズが小さすぎます")

        if obi_height <= 0:
            return (False, "画像サイズが小さすぎます")

        # 上部に貼り付ける画像をメイン画像の割合を出す
        percentage = float(img_width) / float(obi_width)
        # 割合をもとに上部に貼り付ける画像の高さを出す
        obi_height2 = round((obi_height * float(percentage)), 0)
        # 上部に貼り付ける画像をリサイズする
        resized = obi.resize((img_width, int(obi_height2)))
    
        # メイン画像をコピーする
        img_copy = img.copy()
        # リサイズした画像を貼り付ける
        img_copy.paste(resized)

        image = image_obi()
        # リネームして保存する
        new_name = image.rename(main_img)
        img_copy.save(new_name, quality=100)

        return True, "画像を保存しました ファイル名は {}".format(new_name)

        if __name__ == "__main__":
            synthesis()
        
 
setting = "setting.json"

if __name__ == "__main__":
    
    setting = "setting.json"

    flag, msg = check_setting_file(setting)

    if not flag:
        print(msg)
    else:
        obi_path = json.load(msg)["imgPath"]
        try:
            while True:
                print("画像パスを入力 Ctrl+cで終了します")
                path = input(">> ")
                image = image_obi()
                img_flag, img_msg = image.synthesis(path, obi_path)
                if img_flag:
                    print("\n", img_msg)
                    print("\n 画像パスを入力 Ctrl+cで終了します")
                    path = input(">> ")
                else:
                    print("\n", img_msg)
                    print("\n 画像パスを入力 Ctrl+cで終了します")
                    path = input(">> ")
        except KeyboardInterrupt:
            pass
