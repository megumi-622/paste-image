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
            json_load: json or msg
                jsonファイルの内容かエラーメッセージ
    """

    # エラー判定用
    flag = False

    try:
        json_open = open(file_name, 'r')
    except FileNotFoundError as e:
        return flag, 'setting.jsonがありません'
    else:
        json_load = json.load(json_open)
        flag = True

        return flag, json_load


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
        new_file_name = '{}-{:03}{}'.format(ftitle, cnt, fext)
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


    def synthesis(self, file_name, img_path):
        """
        画像を合成する

        Parameters
        ----------
        file_path: string
            画像ファイル名
        img_path: string
            上部に貼り付ける画像
        """

        # 上部に合成する画像
        obi = Image.open(img_path)

        try:
            if os.path.exists(file_name):
                img = Image.open(file_name)
                pass
        except Exception:
            return "画像が存在しません"
        
        # 上部に貼り付ける画像サイズ
        obi_width, obi_height = obi.size

        # メイン画像のサイズ
        img_width, img_height = img.size

        try:
            # 上部に貼り付ける画像をメイン画像の割合を出す
            percentage = float(img_width) / float(obi_width)
            # 割合をもとに上部に貼り付ける画像の高さを出す
            obi_height2 = round((obi_height * float(percentage)), 0)
            # 上部に貼り付ける画像をリサイズする
            resized = obi.resize((img_width, int(obi_height2)))
            pass
        except ZeroDivisionError as e:
            return 'ZeroDivisionError:' + e
        except NameError as e:
            return 'NameError:' + e
        except Exception as e:
            return 'Exception' + e

        try:
            # メイン画像をコピーする
            img_copy = img.copy()
            # リサイズした画像を貼り付ける
            img_copy.paste(resized)
            pass
        except ZeroDivisionError as e:
            return 'ZeroDivisionError:'+ e
        except NameError as e:
            return 'NameError:' + e
        except Exception as e:
            return 'Exception:' + e

        try:
            image = image_obi()
            # リネームして保存する
            new_name = image.rename(file_name)
            img_copy.save(new_name, quality=100)
            return True
        except ZeroDivisionError as e:
            return 'ZeroDivisionError:' +  e
        except NameError as e:
            return 'NameError:' + e
        except Exception as e:
            return 'Exception:' + e
        
        if __name__ == "__main__":
            synthesis()
        
 
inputtext = ""
setting = "setting.json"

if __name__ == "__main__":
    
    setting = 'setting.json'

    flag, json_or_msg = check_setting_file(setting)

    if not flag:
        print(json_or_msg)
    else:
        obi_path = json_or_msg['imgPath']
        try:
            while True:
                print("画像パスを入力 Ctrl+cで終了します")
                path = input(">> ")
                image = image_obi()
                result = image.synthesis(path, obi_path)
                if result is True:
                    print("保存しました")
                    print("画像パスを入力 Ctrl+cで終了します")
                    path = input(">> ")
                else:
                    print(result)
                    print("画像パスを入力 Ctrl+cで終了します")
                    path = input(">> ")
        except KeyboardInterrupt:
            pass
