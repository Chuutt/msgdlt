from telethon import TelegramClient

api_id = "10098309"
api_hash = "aaacac243dddc9f0433c89cab8efe323"

client = TelegramClient("default", api_id, api_hash)
client.start()


async def clean(res, chatsn):
    for n in chatsn:
        c = res[n]
        count, name, messages, group = c[0], c[1], c[2], c[3]
        
        print(f"Deleting {count} messages from {name}...", end=" ")
        await client.delete_messages(group, messages, revoke=True)
        print("completed!")


async def main():
    print("Telegram message cleaner")
    
    print("Fetching dialogs...", end="") 
    dialogs = await client.get_dialogs(limit=None)
    print(f"\rFetched {len(dialogs)} dialogs in total")
    
    groups = [i for i in dialogs if i.is_group]
    print(f"{len(groups)} groups \n")
    
    me = await client.get_me()
    res = []
    for i in groups:
        print(f"\rFetching messages from {i.name}...\t\t", end="")
        messages = [i.id for i in await client.get_messages(i, limit=99999, from_user=me)]
        res.append((len(messages), i.name, messages, i))
    print("\rFetched messages from all groups\t\t")
    
    res = sorted(res, key=lambda i: (-i[0], i[1]))
    print("Top groups by message count \n")
    print("\n".join((f"[{i}]\t{c[0]} messages \t{c[1]}" for i, c in enumerate(res))))
    
    delfrom = None
    while not delfrom:
        try:
            print("Enter group numbers (separated by space) from which you want delete ALL your messages:")
            print("example: 0 3 5")
            delfrom = [int(i) for i in input().split()]
        except:
            pass
    await clean(res, delfrom)
    print("Done!")


with client:
    client.loop.run_until_complete(main())
