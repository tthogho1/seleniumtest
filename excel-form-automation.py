from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time

def read_excel_and_input_form(excel_path):
    """
    Excelファイルを読み込み、現在開いているChromeブラウザに対してフォーム入力を行う関数
    
    Parameters:
    excel_path (str): Excelファイルのパス
    """
    try:
        # Excelファイルの読み込み
        df = pd.read_excel(excel_path, header=None)

        # 列名を取得
        column_names = df.iloc[0]
        df.columns = column_names
        
        # 数字がコンソールから入力されるまで待つ。数字以外は無視して再度待機。qを入力すると終了
        
        while True:
            user_input = input("数字を入力してください：")
            if user_input == 'q':
                break
            elif user_input.isdigit() == False:
                continue
        
            # 各行のデータを処理
            suffix = str(int(user_input))
            for index, row in df.iterrows():
                if pd.isna(row['value' + suffix]):  # 空の値はスキップ
                    continue
                    
                if row['type' + suffix] in ['text', 'tel','password']:
                    # 要素が見つかるまで待機
                    element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.NAME, row['name' + suffix]))
                    )
                    # 入力前にクリア
                    element.clear()
                    # 値を入力（数値の場合は文字列に変換）
                    element.send_keys(str(row['value' + suffix]))
                    # 少し待機
                    time.sleep(0.5)
        
            # 「次へ」ボタンをクリック
            #next_button = WebDriverWait(driver, 10).until(
            #    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '次へ')]"))
            #)
            #next_button.click()
            
            print("フォーム入力が完了しました")
        
    except FileNotFoundError:
        print(f"Excelファイルが見つかりません: {excel_path}")
    except Exception as e:
        print(f"エラーが発生しました: {str(e)}")

# 使用例
if __name__ == "__main__":
    # Excelファイルのパスを指定
    # デバッグポートを指定してChromeに接続
    #chrome_options = Options()
    #chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    driver = webdriver.Chrome()

    excel_path = "input_tags.xlsx"  # あなたのExcelファイルのパスに変更してください    
    read_excel_and_input_form(excel_path)
