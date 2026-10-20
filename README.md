# Rasa + OpenAI Chatbot

一个使用 Rasa 进行意图识别、通过自定义 Action 调用 OpenAI Responses API 生成回复的示例聊天机器人。

## 安全说明

API Key 不存放在源码中。项目从环境变量 `OPENAI_API_KEY` 读取凭据，并从 `OPENAI_MODEL` 读取模型 ID。`.env` 已加入 `.gitignore`，不会被 Git 提交。

如果你曾在旧版本源码中填写真实 API Key，请立即在 OpenAI 控制台撤销该 Key，并创建一个新 Key；仅仅从文件中删除不能使已经泄露的 Key 失效。

## 环境要求

- Python 3.9 或 3.10
- Rasa 3.6.19

Rasa 3.6 不支持较新的 Python 版本，推荐使用 Python 3.9。

## 安装

```powershell
py -3.9 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

复制环境变量模板：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，填写新创建的 API Key 和你账户可用的模型 ID：

```dotenv
OPENAI_API_KEY=your-new-api-key
OPENAI_MODEL=your-model-id
```

不要提交 `.env`。

## 训练和运行

首次运行或修改训练数据后训练模型：

```powershell
rasa train
```

打开第一个终端并启动自定义 Action Server：

```powershell
rasa run actions
```

打开第二个终端并启动命令行聊天：

```powershell
rasa shell
```

如需启动 REST API：

```powershell
rasa run --enable-api --cors "*"
```

默认地址为 `http://localhost:5005`，Action Server 地址为 `http://localhost:5055`。

## 项目结构

```text
.
├── actions/           # 自定义 OpenAI Action
├── data/              # NLU、规则和故事训练数据
├── tests/             # Rasa 对话测试
├── config.yml         # NLU 与策略配置
├── credentials.yml    # 消息通道配置
├── domain.yml         # 意图、回复和 Action 定义
├── endpoints.yml      # Action Server 配置
├── .env.example       # 环境变量模板（不含真实密钥）
└── requirements.txt
```

`.rasa/` 和 `models/` 是可重新生成的缓存及训练产物，已从 Git 中排除。

## 测试

```powershell
rasa data validate
rasa test
```
