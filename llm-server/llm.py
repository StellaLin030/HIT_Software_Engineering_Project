from flask import Blueprint, Response, json, request, jsonify
from flask_login import login_required, current_user
from flask_cors import cross_origin
import openai
from dashscope import Generation
import dashscope
import requests
import json
from http import HTTPStatus
from models import Conversations, db
from datetime import datetime

llm_bp = Blueprint('llm', __name__)

messages_chatgpt = []
messages_tongyi = []
messages_wenxin = []


@llm_bp.route('/tongyi')
@cross_origin(supports_credentials=True)
@login_required
def stream_numbers():
    global messages_tongyi
    query = request.args.get('query', default='default query')
    messages_tongyi.append({'role': 'user', 'content': query})

    def chat():
        print(query)
        dashscope.api_key = "sk-96f5960806d24c9cbb8b01de99e9c224"
        responses = Generation.call(
            model="qwen-turbo",
            messages=messages_tongyi,
            result_format='message',  # 设置输出为'message'格式
            stream=True,  # 设置输出方式为流式输出
            incremental_output=True  # 增量式流式输出
        )

        whole_message = ""
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                answer_part = response.output.choices[0]['message']['content']
                whole_message += answer_part
                json_data = json.dumps({"message": response.output.choices[0]['message']['content']})
                yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_tongyi.append({'role': 'assistant', 'content': whole_message})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        print(json_data)
        print('通义千问结束')

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


@llm_bp.route('/chatgpt')
@cross_origin(supports_credentials=True)
@login_required
def get_answer():
    global messages_chatgpt
    query = request.args.get('query', default='default query')
    messages_chatgpt.append({'role': 'user', 'content': query})

    def chat():
        openai.api_base = "https://apikeyplus.com/v1"  # 换成代理，一定要加 v1
        openai.api_key = "sk-0oJ42VRZX4MU1GXQ8fB76c349aF649AbA0Fe017cE88b5dC5"

        response = ""
        for resp in openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages_chatgpt,
                stream=True
        ):
            if 'content' in resp.choices[0].delta:
                content = resp.choices[0].delta.content
                response += content
                json_data = json.dumps({"message": content})
                yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据

        messages_chatgpt.append({'role': 'system', 'content': response})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        print(json_data)
        print('ChatGPT结束')

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


@llm_bp.route('/wenxin')
@cross_origin(supports_credentials=True)
@login_required
def wenxin_get_answer():
    global messages_wenxin
    query = request.args.get('query', default='default query')
    messages_wenxin.append({'role': 'user', 'content': query})

    def chat():
        url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()

        payload = json.dumps({
            "messages": messages_wenxin,
            "stream": True
        })
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("POST", url, headers=headers, data=payload, stream=True)

        full_response = ""
        for line in response.iter_lines():
            line_decode = line.decode("UTF-8")
            if line_decode.startswith("data:"):  # 检查是否为 data: 行
                # 将 "data: " 替换为空字符串，然后解析为 JSON
                try:
                    json_line = json.loads(line_decode.replace("data: ", ""))
                    result = json_line.get("result", "")
                    full_response += result
                    if result:
                        json_data = json.dumps({"message": result})
                        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
                except json.JSONDecodeError:
                    print("无法解析为 JSON 格式:", line_decode)
                    continue
        messages_wenxin.append({'role': 'assistant', 'content': full_response})
        json_data = json.dumps({"message": 'done'})
        yield f"data: {json_data}\n\n"  # 按照SSE格式发送数据
        print(json_data)
        print('文心一言结束')

    headers = {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'X-Accel-Buffering': 'no',
    }

    return Response(chat(), content_type='text/event-stream', headers=headers)


def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """

    url = "https://aip.baidubce.com/oauth/2.0/token?client_id=zJlxOu8SlyQFR5kh2i0lw5eS&client_secret=HysKv0tQl7o650EkELYO6URhfswFgQeB&grant_type=client_credentials"

    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")


# 通过文心一言总结当前多轮对话的主题内容，不超过十个字
def get_summary():
    global messages_wenxin
    new_messages = messages_wenxin
    new_messages.append(
        {'role': 'user', 'content': '请你用不超过十个字来总结我们的对话内容，不要多余的对话内容，只要总结内容'})

    url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie-speed-128k?access_token=" + get_access_token()

    payload = json.dumps({
        "messages": new_messages,
        "stream": True
    })
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload, stream=True)
    full_response = ""
    for line in response.iter_lines():
        line_decode = line.decode("UTF-8")
        if line_decode.startswith("data:"):  # 检查是否为 data: 行
            # 将 "data: " 替换为空字符串，然后解析为 JSON
            try:
                json_line = json.loads(line_decode.replace("data: ", ""))
                result = json_line.get("result", "")
                full_response += result
            except json.JSONDecodeError:
                print("无法解析为 JSON 格式:", line_decode)
                continue
    print(full_response)
    return full_response


# 用户创建新的聊天记录时应该保存旧的聊天记录
@llm_bp.route('/conversations/new_conversation', methods=['POST'])
def save_and_clear_conversation():
    global messages_chatgpt, messages_tongyi, messages_wenxin

    # 检查列表是否为空
    if not messages_chatgpt or not messages_tongyi or not messages_wenxin:
        # 列表为空，可以选择返回一个错误响应或者进行其他处理
        return jsonify({'error': 'Some of the message lists are empty.'}), 400

    user_id = current_user.id  # 请替换成你实际的用户 ID
    conversation_id = current_user.conversation_current_id + 1
    current_user.conversation_current_id = conversation_id

    current_timestamp = datetime.utcnow()
    current_summary = get_summary()  # 由文心一言总结对话内容

    # 列表不为空，创建一个新的 Conversations 对象并保存到数据库中
    conversation = Conversations(
        id=conversation_id,
        user_id=user_id,
        chatgpt_messages=json.dumps(messages_chatgpt),  # 转换为 JSON 字符串
        wenxin_messages=json.dumps(messages_wenxin),  # 注意：这里应该是 messages_wenxin 而不是 messages_tongyi
        tongyi_messages=json.dumps(messages_tongyi),
        timestamp=current_timestamp,
        summary=current_summary
    )
    db.session.add(conversation)
    db.session.commit()
    view_conversations()

    # 清空当前对话内容
    messages_chatgpt = []
    messages_tongyi = []
    messages_wenxin = []

    # 返回成功响应或其他适当的响应
    return jsonify({'success': 'Conversation saved successfully.'}), 200


# 用户点击某个聊天记录的主题，获取此次聊天记录的所有内容，类似chatgpt页面的功能
# 从页面返回：对话id
# 返回：chatgpt_messages、chatgpt_messages、tongyi_messages
@llm_bp.route('/conversations/get_conversation', methods=['GET'])
def get_conversation_by_id():
    # global messages_chatgpt,messages_tongyi,messages_wenxin
    conversation_id = request.args.get('id')
    user_id = current_user.id

    if not conversation_id or not user_id:
        return jsonify({'error': 'Missing id or user_id'}), 400

    conversation = Conversations.query.filter_by(id=conversation_id, user_id=user_id).first()

    if conversation is None:
        return jsonify({'error': 'Conversation not found'}), 404

    print("messages_chatgpt:", json.loads(conversation.chatgpt_messages))
    print("messages_tongyi:", json.loads(conversation.tongyi_messages))
    print("messages_wenxin:", json.loads(conversation.wenxin_messages))

    return jsonify({
        'chatgpt_messages': conversation.chatgpt_messages,
        'wenxin_messages': conversation.wenxin_messages,
        'tongyi_messages': conversation.tongyi_messages
    }), 200


# 获取当前用户的所有聊天记录的主题
# input：当前用户id 【不需要从页面获取，后端有记录】
# output： conversation.id, conversation.summary
@llm_bp.route('/conversations/get_conversation_summary', methods=['GET'])
def get_user_conversations():
    user_id = current_user.id
    if not user_id:
        return jsonify({'error': 'Missing user_id'}), 400

    # 查询并按 id 从大到小排序,这样查出来的第一个是最近一次的对话主题
    conversations = Conversations.query.filter_by(user_id=user_id).order_by(Conversations.id.desc()).all()

    if not conversations:
        return jsonify({'error': 'No conversations found for this user'}), 404

    result = [
        {'id': conversation.id, 'summary': conversation.summary}
        for conversation in conversations
    ]
    print(result)
    return jsonify(result), 200


# for test
def view_conversations():
    conversations = Conversations.query.all()
    result = []
    for conversation in conversations:
        result.append({
            'id': conversation.id,
            'user_id': conversation.user_id,
            'chatgpt_messages': conversation.chatgpt_messages,
            'wenxin_messages': conversation.wenxin_messages,
            'tongyi_messages': conversation.tongyi_messages,
            'summary': conversation.summary,
            'timestamp': conversation.timestamp
        })
    return {'conversations': result}


# @llm_bp.route('/messages/all', methods=['GET'])
# def get_all_messages():
#     global messages_chatgpt, messages_tongyi, messages_wenxin
#     print("messages_chatgpt:", messages_chatgpt)
#     print("messages_tongyi:", messages_tongyi)
#     print("messages_wenxin:", messages_wenxin)
#     return jsonify({
#         'chatgpt': messages_chatgpt,
#         'tongyi': messages_tongyi,
#         'wenxin': messages_wenxin
#     }), 200
