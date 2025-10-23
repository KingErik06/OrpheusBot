import pytest 
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch

@pytest_asyncio.fixture
async def mock_bot():
    mock_bot = AsyncMock()
    mock_bot.user = AsyncMock()
    mock_bot.user.name = "TestBot"
    mock_bot.command_prefix = "!"
    mock_bot.cogs = {}
    mock_bot.get_command = MagicMock()
    return mock_bot

@pytest.fixture
def mock_ctx():
    mock_ctx = AsyncMock()
    mock_ctx.author = AsyncMock()
    mock_ctx.author.name = "TestUser"
    mock_ctx.author.id = 123456789
    mock_ctx.send = AsyncMock()
    mock_ctx.message = AsyncMock()
    mock_ctx.message.content = "!test"
    return mock_ctx
