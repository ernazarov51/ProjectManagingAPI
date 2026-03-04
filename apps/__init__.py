# # import requests
# #
# # def send_telegram_message(text):
# #     token = "7572354458:AAHQMABo5TFFswENfe-FrgzjgIWZZfvw3kE"
# #     chat_id = "-1003870895063"
# #
# #     url = f"https://api.telegram.org/bot{token}/sendMessage"
# #
# #     data = {
# #         "chat_id": chat_id,
# #         "text": text
# #     }
# #
# #     requests.post(url, data=data)
# #
# # send_telegram_message("JHDJ jahdbajs djewd an")
# import datetime
#
# today = datetime.date.today()
# monday = today - datetime.timedelta(days=today.weekday())
#
# week_dates = []
#
# for i in range(6):
#     day = monday + datetime.timedelta(days=i)
#     if day == today:
#         week_dates.append("Bugun 🟢")
#     else:
#         week_dates.append(f"{day.strftime('%Y-%m-%d')} ({day.strftime('%A')})")
#
# print(week_dates)
#
#
tex="""
📅 Aliyev Valijon, Daily Planlar:

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:32
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:32
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:33
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:34
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:34
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:34
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:34
————————————————————

🗓 Sana: 2026-02-26
📌 Turi: #daily_plan
⏰ Yuborilgan vaqt: #2026-02-26, 16:35
————————————————————"""

print(len(tex))
