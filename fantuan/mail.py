# -*- coding:utf-8 -*-
from sae.mail import send_mail

mail_from = "fantuan@jiajun.me"
mail_server = "smtp.gmail.com"
mail_port = 587
mail_password = "Q2%eWLF3"

def sendSignUpMail(to, name):
    msg = """亲爱的{},

  欢迎加入饭团,我们的应用旨在使的您的生活更加方便和快捷。
  如果你有任何意见和建议，请致信 celeheaven@gmail.com 。
  衷心地祝福您快乐每一天。

Regards,
Fantuan Team

http://fantuan.sinaapp.com"""
    title = "欢迎加入饭团"
    send_mail(to, title, msg.format(name), (mail_server, mail_port, mail_from, mail_password, True))
