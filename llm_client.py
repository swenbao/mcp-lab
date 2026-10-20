"""最小 LLM 決策：模型選工具，client 經由 MCP 執行，再交回模型回答。"""

import argparse
import asyncio
import json
import os
from pathlib import Path

from dotenv import dotenv_values
from mcp import Client
from mcp.types import TextContent
from openai import AsyncOpenAI, APIConnectionError, APIStatusError


INSTRUCTIONS = (
    "你是本專案的小幫手，使用繁體中文簡短回答。"
    "使用者詢問本專案術語表的資料時，先呼叫 lookup_term，依實際結果回答，不憑記憶猜測。"
    "一般招呼不需要工具。工具找不到資料時就如實說明。"
)


async def ask(question: str, mcp: Client, llm: AsyncOpenAI, model: str) -> None:
    # 1. 從 MCP server 取得工具描述，轉成 OpenAI function calling 的工具定義。
    listing = await mcp.list_tools()
    tool = next((item for item in listing.tools if item.name == "lookup_term"), None)
    if tool is None:
        raise RuntimeError("這個 MCP server 沒有提供本課的 lookup_term 工具。")
    tools = [{
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": {**tool.input_schema, "additionalProperties": False},
        "strict": True,
    }]
    print(f"\n從 MCP 取得工具：{tool.name}")
    print(f"模型：{model}")
    print(f"\n問題：\n{question}")
    history = [{"role": "user", "content": question}]
    options = dict(
        model=model, instructions=INSTRUCTIONS, tools=tools,
        parallel_tool_calls=False, max_output_tokens=800, store=False,
        include=["reasoning.encrypted_content"],
    )

    # 2. 模型決定直接回答，或產生工具名稱與參數。此時尚未執行 MCP 工具。
    response = await llm.responses.create(input=history, tool_choice="auto", **options)
    if response.status != "completed":
        raise RuntimeError(f"模型回覆尚未完成（{response.status}），本次不執行工具。")
    calls = [item for item in response.output if item.type == "function_call"]
    if calls:
        if len(calls) != 1 or calls[0].name != tool.name:
            raise RuntimeError("本課只允許呼叫一次已提供的 lookup_term。")
        call = calls[0]
        arguments = json.loads(call.arguments)
        print(f"\nLLM 選擇工具：{call.name}")
        print(f"LLM 產生參數：\n{json.dumps(arguments, ensure_ascii=False, indent=2)}")

        # 3. 真正發 MCP 請求的是 client；function calling 本身不會執行工具。
        result = await mcp.call_tool(call.name, arguments)
        text = "\n".join(block.text for block in result.content if isinstance(block, TextContent))
        print(f"\nMCP server 回覆：\n{text}")

        # 4. 保留模型輸出（包含 reasoning 等項目），再補上對應的工具結果。
        history.extend(response.output)
        history.append({
            "type": "function_call_output", "call_id": call.call_id,
            "output": json.dumps({"is_error": result.is_error, "text": text}, ensure_ascii=False),
        })
        # 只示範一次工具呼叫；第二次 API 請求用來整理答案，不再呼叫工具。
        response = await llm.responses.create(input=history, tool_choice="none", **options)
        if response.status != "completed":
            raise RuntimeError(f"最終回覆尚未完成（{response.status}），請調整模型或輸出上限。")
    else:
        print("\nLLM 選擇直接回答，沒有呼叫 MCP 工具。")
    print(f"\nLLM 最終回答：\n{response.output_text or '（沒有文字回覆）'}\n")


async def main(question: str, url: str, key: str, model: str) -> None:
    async with Client(url, read_timeout_seconds=10) as mcp:
        async with AsyncOpenAI(
            api_key=key, base_url="https://api.openai.com/v1", timeout=30, max_retries=0
        ) as llm:
            await ask(question, mcp, llm, model)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="讓 LLM 決定是否透過 MCP 查詢術語")
    parser.add_argument("question", help="例如：請查本專案術語表，banana 的解釋是什麼？")
    parser.add_argument("--url", help="覆寫 .env 的 MCP_SERVER_URL")
    parser.add_argument("--model", help="覆寫 .env 的 OPENAI_MODEL")
    args = parser.parse_args()
    settings = dotenv_values(Path(__file__).resolve().with_name(".env"))
    key = (settings.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") or "").strip()
    if not key:
        parser.exit(1, "請先在專案 .env 填入 OPENAI_API_KEY，再執行。\n")
    url = args.url or settings.get("MCP_SERVER_URL") or "http://127.0.0.1:8000/mcp"
    model = args.model or settings.get("OPENAI_MODEL") or "gpt-5.4-mini"
    try:
        asyncio.run(main(args.question, url, key, model))
    except APIConnectionError:
        parser.exit(1, "無法連到 OpenAI API，請確認網路連線。\n")
    except APIStatusError as error:
        parser.exit(1, f"OpenAI API 回傳 HTTP {error.status_code}；請確認 key、額度與模型存取權。\n")
