# 塔羅 (Tarot)

這是一個結合了可愛貓咪人格的塔羅牌占卜應用程式。透過 OpenAI 的 GPT 模型，薯條貓貓大師將為您解讀塔羅牌的奧秘，並給予正面積極的建議。

## 特色

- **貓咪占卜師**：以「喵喵」為口頭禪的可愛占卜風格。
- **完整塔羅牌組**：包含 78 張塔羅牌（正位與逆位）。
- **互動式介面**：使用 Gradio 建構的友善使用者介面。
- **即時解牌**：利用 OpenAI API 進行即時的塔羅牌義解讀。

## 前置需求 (Prerequisites)

- Python 3.7 或更高版本
- OpenAI API Key

## 安裝 (Installation)

1.  **複製專案 (Clone the repository)**

    ```bash
    git clone <repository_url>
    cd tarot
    ```

2.  **安裝依賴套件 (Install dependencies)**

    ```bash
    pip install -r requirements.txt
    ```

3.  **設定環境變數 (Setup Environment Variables)**

    在專案根目錄下建立一個 `.env` 檔案，並填入您的 OpenAI API Key：

    ```text
    OPENAI_API_KEY=sk-your_api_key_here
    ```

    或者您可以參考 `.env.example` (如果有的話) 或直接修改 `.env` 檔案。

## 使用方法 (Usage)

執行以下指令啟動應用程式：

```bash
python main.py
```

啟動後，程式會顯示一個本地網址 (通常是 `http://127.0.0.1:7860`)，請在瀏覽器中開啟該網址即可開始使用。

## 技術棧 (Technologies Used)

- [Python](https://www.python.org/)
- [Gradio](https://gradio.app/) - 用於建構 Web 介面
- [OpenAI API](https://openai.com/) - 用於生成占卜結果

## 參考資料 (Reference)

- [IT邦幫忙文章](https://ithelp.ithome.com.tw/articles/10323720)
