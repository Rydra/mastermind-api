from typing import Any

import pytest
from hamcrest import *
from pymongo import MongoClient
from starlette import status
from starlette.testclient import TestClient

from apps.mastermind.core.domain.domain import Game
from apps.mastermind.infrastructure.mongo_persistence.uow import MongoUnitOfWork
from config.settings import settings
from main import app


@pytest.fixture
def api_client():
    client = TestClient(app)
    with client:
        # We need to use yield instead of return in order to trigger
        # startup events in the test.
        # ref: https://fastapi.tiangolo.com/advanced/testing-events/
        yield client


@pytest.fixture(autouse=True)
def setup() -> None:
    settings.mongo_dbname = "test_db"
    yield
    client = MongoClient(settings.mongodb_dsm)
    client.drop_database("test_db")


class TestMastermindApi:
    @staticmethod
    async def create_game(
        num_slots: int,
        num_colors: int,
        max_guesses: int,
        reference: str,
        status: str,
        secret_code: list[str],
    ) -> Game:
        async with MongoUnitOfWork() as uow:
            game = Game(
                id=uow.games.next_id(),
                num_slots=num_slots,
                num_colors=num_colors,
                max_guesses=max_guesses,
                reference=reference,
                status=status,
                secret_code=secret_code,
                guesses=[],
            )

            await uow.games.asave(game)
            await uow.commit()
        return game

    def assert_guess(
        self, response: Any, expected_white_peg: int, expected_black_peg: int
    ):
        assert_that(
            response.json()["guesses"][0]["white_pegs"], is_(expected_white_peg)
        )
        assert_that(
            response.json()["guesses"][0]["black_pegs"], is_(expected_black_peg)
        )

    async def test_get_games(self, api_client, anyio_backend):
        """Check if retrieve all games correctly"""
        await self.create_game(
            4,
            4,
            2,
            "MYREF",
            "running",
            ["red", "red", "green", "yellow"],
        )

        response = api_client.get("/api/games/")

        expected_response = {
            "results": contains_exactly(
                has_entries(
                    {
                        "num_colors": 4,
                        "secret_code": ["red", "red", "green", "yellow"],
                        "max_guesses": 2,
                        "reference": "MYREF",
                    }
                )
            )
        }

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    async def test_get_game(self, api_client, anyio_backend):
        """Check if retrieve a game correctly"""
        game = await self.create_game(
            4,
            4,
            2,
            "MYREF",
            "running",
            ["red", "red", "green", "yellow"],
        )

        response = api_client.get(f"/api/games/{game.id}/")

        expected_response = has_entries(
            {
                "num_colors": 4,
                "secret_code": ["red", "red", "green", "yellow"],
                "max_guesses": 2,
                "reference": "MYREF",
            }
        )

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    async def test_create_game(self, api_client, anyio_backend):
        """Check if a game is created correctly"""
        response = api_client.post(
            "/api/games/",
            json={"num_slots": 4, "num_colors": 4, "max_guesses": 2},
        )

        expected_response = has_entries(
            {
                "num_colors": 4,
                "max_guesses": 2,
                "status": "running",
            }
        )
        assert_that(response.status_code, is_(status.HTTP_201_CREATED))
        assert_that(response.json(), expected_response)

    async def test_create_guess(self, api_client, anyio_backend):
        """Check if guess create correctly"""
        game = await self.create_game(
            4,
            6,
            2,
            "MYREF",
            "running",
            ["green", "blue", "yellow", "red"],
        )

        response = api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": ["orange", "orange", "orange", "orange"]},
        )

        response = api_client.get(f"/api/games/{game.id}/")
        expected_response = has_entries(
            {
                "guesses": has_item(
                    {
                        "code": ["orange", "orange", "orange", "orange"],
                        "white_pegs": 0,
                        "black_pegs": 0,
                    }
                )
            }
        )

        assert_that(response.status_code, status.HTTP_201_CREATED)
        assert_that(response.json(), expected_response)

    async def test_retrieve_guesses(self, api_client, anyio_backend):
        """Check if guesses are retrieved correctly"""
        game = await self.create_game(
            4,
            5,
            2,
            "MYREF",
            "running",
            ["green", "blue", "yellow", "red"],
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": ["orange", "orange", "orange", "orange"]},
        )
        api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": ["blue", "red", "orange", "orange"]},
        )
        response = api_client.get(f"/api/games/{game.id}/")

        expected_response = has_entries(
            {
                "guesses": contains_exactly(
                    {
                        "code": ["orange", "orange", "orange", "orange"],
                        "white_pegs": 0,
                        "black_pegs": 0,
                    },
                    {
                        "code": ["blue", "red", "orange", "orange"],
                        "white_pegs": 2,
                        "black_pegs": 0,
                    },
                )
            }
        )

        assert_that(response.status_code, status.HTTP_201_CREATED)
        assert_that(response.json(), expected_response)

    @pytest.mark.parametrize(
        "secret_code,guess,white_pegs,black_pegs",
        [
            (
                ["red", "green", "green", "blue"],
                ["red", "green", "green", "blue"],
                0,
                4,
            ),
            (["red", "red", "red", "red"], ["blue", "yellow", "orange", "blue"], 0, 0),
            (["green", "blue", "blue", "red"], ["green", "blue", "red", "blue"], 2, 2),
            (["blue", "blue", "blue", "red"], ["red", "blue", "green", "green"], 1, 1),
            (["red", "blue", "green", "green"], ["blue", "blue", "blue", "red"], 1, 1),
            (["blue", "blue", "blue", "red"], ["blue", "blue", "blue", "red"], 0, 4),
            (
                ["white", "blue", "white", "blue"],
                ["blue", "white", "blue", "white"],
                4,
                0,
            ),
            (
                ["orange", "orange", "orange", "white"],
                ["orange", "white", "white", "white"],
                0,
                2,
            ),
        ],
    )
    async def test_one_white_peg(
        self, api_client, secret_code, guess, white_pegs, black_pegs, anyio_backend
    ):
        """Check if return one white peg"""
        game = await self.create_game(
            4,
            6,
            2,
            "MYREF",
            "running",
            secret_code,
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": guess},
        )
        response = api_client.get(f"/api/games/{game.id}/")

        self.assert_guess(response, white_pegs, black_pegs)
