WEBHOOK_CACHE = {}

async def get_webhook(channel):
    webhook = WEBHOOK_CACHE.get(channel.id)
    if webhook:
        try:
            await webhook.fetch()
            return webhook
        except Exception:
            pass

    webhooks = await channel.webhooks()
    for webhook in webhooks:
        if webhook.name == "chatgptbot":
            WEBHOOK_CACHE[channel.id] = webhook
            return webhook

    webhook = await channel.create_webhook(name="chatgptbot")
    WEBHOOK_CACHE[channel.id] = webhook
    return webhook