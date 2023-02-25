import pytest

from app.ycomb import parser


@pytest.mark.asyncio
async def test_get_comments():
    total = 0
    async for x in parser.get_comments():
        assert x.id
        assert x.text
        assert x.date
        assert x.user.id
        assert x.post.id
        assert x.post.title
        total += 1
    assert total == 30
