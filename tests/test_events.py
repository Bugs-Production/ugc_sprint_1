from http import HTTPStatus

import pytest

from tests.functional.test_data.events import (click_event, missing_fields,
                                               wrong_event_type)


class TestEvents:
    def setup_method(self):
        self.endpoint = "/api/v1/events/"

    @pytest.mark.asyncio
    async def test_events_success(self, aiohttp_request):
        body, status = await aiohttp_request(
            "POST", endpoint=self.endpoint, json=click_event
        )
        assert status == HTTPStatus.OK

    @pytest.mark.asyncio
    async def test_wrong_event_type(self, aiohttp_request):
        body, status = await aiohttp_request(
            "POST", endpoint=self.endpoint, json=wrong_event_type
        )
        assert status == HTTPStatus.NOT_FOUND

    @pytest.mark.asyncio
    async def test_missing_fields(self, aiohttp_request):
        body, status = await aiohttp_request(
            "POST", endpoint=self.endpoint, json=missing_fields
        )
        assert status == HTTPStatus.UNPROCESSABLE_ENTITY
