from pyrogram import Client, enums, filters, types

from bot.config import config
from bot import logger


class BikaBot(Client):
    def __init__(self) -> None:
        super().__init__(
            name="BikaMusicBot",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            parse_mode=enums.ParseMode.HTML,
            max_concurrent_transmissions=7,
            link_preview_options=types.LinkPreviewOptions(is_disabled=True),
        )

        self.owner_id = config.OWNER_ID
        self.logger_id = config.LOGGER_ID

        self.bl_users = filters.user()
        self.sudoers = filters.user(self.owner_id) if self.owner_id else filters.user()

        self.id: int | None = None
        self.name: str | None = None
        self.username: str | None = None
        self.mention: str | None = None

    async def boot(self) -> None:
        await super().start()

        me = await self.get_me()
        self.id = me.id
        self.name = me.first_name
        self.username = me.username
        self.mention = me.mention

        if not self.logger_id:
            logger.warning("LOGGER_ID is not configured. Skipping log group check.")
            logger.info("Bot started as @%s", self.username or "unknown")
            return

        try:
            await self.send_message(self.logger_id, "✅ Bika Music Bot started successfully.")
            member = await self.get_chat_member(self.logger_id, self.id)
        except Exception as exc:
            raise SystemExit(
                f"Bot could not access LOGGER_ID {self.logger_id}.\nReason: {exc}"
            ) from exc

        if member.status not in (
            enums.ChatMemberStatus.ADMINISTRATOR,
            enums.ChatMemberStatus.OWNER,
        ):
            raise SystemExit("Please promote the bot as admin in the logger chat.")

        logger.info("Bot started as @%s", self.username or "unknown")

    async def shutdown(self) -> None:
        await super().stop()
        logger.info("Bot stopped.")
