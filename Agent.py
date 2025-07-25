from __future__ import annotations
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm
)

from livekit.agents.multimodal import MultimodalAgent
from livekit.plugins import openai
from dotenv import load_dotenv
from API import AssistantFnc
from prompts import WELCOME_MESSAGE, INSTRUCTIONS
import os

load_dotenv()

async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.SUBSCRIBE_ALL)
    await ctx.wait_for_participant()

    model = openai.realtime.RealtimeModel(
        instruction=INSTRUCTIONS,
        voice="shimmer",
        temperature=0.8,
        modalities=["text","audio"],
    )

    assistant_fnc = AssistantFnc()
    assistant = MultimodalAgent(model = model, fnc_ctx = assistant_fnc)
    assistant.start(ctx.room)

    session = model.session[0]
    session.conversation.item.create(
        llm.ChatMessage(
            role='assistant',
            content=WELCOME_MESSAGE
        )
    )
    session.response.create()

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))