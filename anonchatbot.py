from aiogram import Bot, Dispatcher, types, executor

bot_token = "token"

bot = Bot(bot_token)
dp = Dispatcher(bot)

print("Bot started")

searching = []
found = []
chatting = []

with open("searching.txt", "r") as file:
    for line in file:
        searching.append(int(line.strip()))

with open('found.txt', 'r') as file:
    for line in file:
        line_data = line.strip().split(',')
        found.append([int(j) for j in line_data])

with open("chatting.txt", "r") as file:
    for line in file:
        chatting.append(int(line.strip()))

print("Backups read")

print("Backup info: ")
print("Searching:", searching)
print("Found:", found)
print("Chatting:", chatting)

@dp.message_handler()
async def echo(message: types.Message):

    userid = message.chat.id
    content = message.text

    if content == "!j":
        if userid not in searching and userid not in chatting:
            searching.append(userid)
            print(f"Message to {userid}: you are now searching for chatmates!")
            await bot.send_message(userid, "You are now searching for chatmates!")

    elif content == "!l":
        if userid not in searching and userid not in chatting:
            print(f"Message to {userid}: you are not in a chat. Use !j to search for a chat.")
            await bot.send_message(userid, "You are not in a chat! Use !j to search for a chat.")
        if userid in searching:
            searching.remove(userid)
            print(f"Message to {userid}: you have left the queue.")
            await bot.send_message(userid, "You have left the queue.")
        elif userid in chatting:
            print(f"Message to {userid}: you have left the chat.")
            await bot.send_message(userid, "You have left the chat.")
            for subarr in found:
                if userid in subarr:
                    receiver = subarr[0] if userid == subarr[1] else subarr[1]
                    subarr.remove(userid)
                    print(f"Message to {receiver}: your chatmate has left.")
                    await bot.send_message(receiver, "Your chatmate has left.")
                    chatting.remove(userid)
                    chatting.remove(receiver)
                    found.remove(subarr)

    else:
        if userid in chatting:
            for subarr in found:
                if userid in subarr:
                    receiver = subarr[0] if userid == subarr[1] else subarr[1]
                    print(f"Message to {receiver}: {content}")
                    await bot.send_message(receiver, content)
        else:
            print(f"Message to {userid}: You have not found a chatmate yet! Use !j to search for a chat.")
            await bot.send_message(userid, "You have not found a chatmate yet! Use !j to search for a chat.")

    if len(searching) == 2:
        found.append([searching[0], searching[1]])
        chatting.extend(searching)
        print(f"Message to {searching[0]}: chatmate found!")
        await bot.send_message(searching[0], "Chatmate found!")
        print(f"Message to {searching[1]}: chatmate found!")
        await bot.send_message(searching[1], "Chatmate found!")
        searching.clear()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates = False)

print("Bot stopped")

with open("searching.txt", "w") as file:
    for i in searching:
        file.write(str(i) + "\n")

with open('found.txt', 'w') as file:
    for line_data in found:
        file.write(','.join([str(j) for j in line_data]) + '\n')

with open("chatting.txt", "w") as file:
    for i in chatting:
        file.write(str(i) + "\n")

print("Backups made")
