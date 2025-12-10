# 命運塔羅 (Destiny Tarot)

這是一個專業、神秘且富有智慧的塔羅牌占卜應用程式。透過 OpenAI 的 GPT 模型，「命運觀測者」將為您解讀塔羅牌的奧秘，並給予深刻且富有哲理的指引。

## 特色

- **專業占卜師**：以「命運觀測者」為名的經典占卜風格，語氣平和、客觀且充滿智慧。
- **完整塔羅牌組**：包含 78 張塔羅牌（正位與逆位）。
- **現代化介面**：使用最新版 Gradio (6.x) 建構的響應式 Web 介面。
- **即時解牌**：利用 OpenAI API (GPT-4o) 進行即時的塔羅牌義解讀。

## 前置需求 (Prerequisites)

- Python 3.10 或更高版本
- OpenAI API Key

## 安裝 (Installation)

1.  **複製專案 (Clone the repository)**

    ```bash
    git clone <repository_url>
    cd tarot
    ```

2.  **建立虛擬環境 (Create Virtual Environment)**

    建議使用虛擬環境來管理套件：

    ```powershell
    # 建立名為 tarot 的虛擬環境
    python -m venv tarot

    # 啟動虛擬環境 (Windows)
    .\tarot\Scripts\activate
    ```

3.  **安裝依賴套件 (Install dependencies)**

    ```bash
    pip install -r requirements.txt
    ```

4.  **設定環境變數 (Setup Environment Variables)**

    在專案根目錄下建立一個 `.env` 檔案，並填入您的 OpenAI API Key：

    ```text
    OPENAI_API_KEY=sk-your_api_key_here
    ```

## 使用方法 (Usage)

確保虛擬環境已啟動，然後執行以下指令：

```bash
python main.py
```

啟動後，程式會顯示一個本地網址 (通常是 `http://127.0.0.1:7860`)，請在瀏覽器中開啟該網址即可開始使用。

## 技術棧 (Technologies Used)

- [Python](https://www.python.org/)
- [Gradio](https://gradio.app/) (v6.x) - 用於建構 Web 介面
- [OpenAI API](https://openai.com/) (v1.x) - 用於生成占卜結果

