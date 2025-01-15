import requests
import json

# Ollama API 的 URL (預設為 localhost:11434)
OLLAMA_API_URL = "http://localhost:11434/api/generate"

# 你想要使用的模型名稱
MODEL_NAME = "llama3.2:3b"  # 請根據您 Ollama 中已安裝的模型名稱進行修改

# 你想要傳遞給模型的 prompt
PROMPT = "請寫一段關於 AI 的短文。"

# 設定 HTTP 請求的 headers
headers = {
    "Content-Type": "application/json",
}

# 設定 HTTP 請求的 payload (包含模型名稱和 prompt)
payload = {
    "model": MODEL_NAME,
    "prompt": PROMPT,
    "stream": False # 將 stream 設為 false，回傳整個結果
}

# 發送 POST 請求到 Ollama API
try:
    response = requests.post(OLLAMA_API_URL, headers=headers, json=payload)
    response.raise_for_status()  # 檢查是否有 HTTP 錯誤

    # 解析 JSON 格式的回應
    data = response.json()
    # print('data=', data)
    
    # 從回應中提取生成的文本
    generated_text = data["response"]

    # 顯示生成的文本
    print("Generated Text:")
    print(generated_text)

except requests.exceptions.RequestException as e:
    print(f"發生錯誤： {e}")

except json.JSONDecodeError as e:
     print(f"JSON 解碼錯誤：{e}")

except KeyError as e:
    print(f"KeyError: {e}. 請檢查 API 回應結構。")
