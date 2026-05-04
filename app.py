import os
import requests
import gradio as gr

EN_US = os.getenv("LANG") != "zh_CN.UTF-8"
API_SMTP = os.getenv("smtpi")
if not API_SMTP:
    raise EnvironmentError("请检查环境变量 smtpi")

ZH2EN = {
    "SMTP 在线测试工具": "SMTP online tester",
    "测试昵称": "Test nickname",
    "发信人昵称": "Sender name",
    "SMTP 服务器": "SMTP host",
    "发信人邮箱": "From email",
    "SMTP 测试": "SMTP Test",
    "测试标题": "Test title",
    "收信人邮箱": "To email",
    "应用密钥": "API key",
    "发送状态": "Status",
    "正文": "Content",
    "标题": "Title",
    "端口": "Port",
}


def _L(zh_txt: str):
    return ZH2EN[zh_txt] if EN_US else zh_txt


def infer(target, title, content, name, email, password, host, port):
    try:
        response = requests.get(
            API_SMTP,
            params={
                "host": host,
                "Port": port,
                "key": password,  # apikey
                "email": email,  # from
                "mail": target,  # to
                "title": title,  # subject
                "name": name,  # nickname
                "text": content,  # content
            },
        )
        if response.status_code == 200:
            result: dict = response.json()
            return result.get("status")

        else:
            raise ConnectionError(f"{response.status_code}")

    except Exception as e:
        return f"{e}"


def main():
    return gr.Interface(
        fn=infer,
        inputs=[
            gr.Textbox(label=_L("收信人邮箱"), placeholder="Recipient"),
            gr.Textbox(label=_L("标题"), value=_L("测试标题")),
            gr.TextArea(label=_L("正文"), value=_L("SMTP 在线测试工具")),
            gr.Textbox(label=_L("发信人昵称"), value=_L("测试昵称")),
            gr.Textbox(label=_L("发信人邮箱"), placeholder="Sender"),
            gr.Textbox(label=_L("应用密钥"), placeholder="SMTP password"),
            gr.Textbox(label=_L("SMTP 服务器"), value="smtp.163.com"),
            gr.Slider(label=_L("端口"), minimum=0, maximum=65535, step=1, value=25),
        ],
        outputs=gr.TextArea(label=_L("发送状态"), buttons=["copy"]),
        flagging_mode="never",
        title=_L("SMTP 测试"),
    )


if __name__ == "__main__":
    main().launch(css="#gradio-share-link-button-0 { display: none; }", ssr_mode=False)
