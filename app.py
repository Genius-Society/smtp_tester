import os
import smtplib
import gradio as gr
from email.header import Header
from email.mime.text import MIMEText

EN_US = os.getenv("LANG") != "zh_CN.UTF-8"
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
    # 邮件内容
    body = f"""
    <html>
        <body>
            <h1>{title}</h1><br>
            {content}
        </body>
    </html>
    """
    # 构建邮件
    msg = MIMEText(body, "html", "utf-8")
    msg["Subject"] = Header(name, "utf-8")
    msg["From"] = email
    msg["To"] = target
    logs = None
    try:
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(email, password)
            server.sendmail(email, [msg["To"]], msg.as_string())

        logs = "邮件发送成功!"

    except smtplib.SMTPResponseException as e:
        if e.smtp_code == -1:
            logs = "邮件发送成功!"
        else:
            logs = f"邮件发送失败: {e}"

    except Exception as e:
        logs = f"邮件系统故障: {e}"

    return logs


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
