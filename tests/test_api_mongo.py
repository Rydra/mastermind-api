from typing import Any

import pytest
from hamcrest import *
from pymongo import MongoClient
from starlette import status
from starlette.testclient import TestClient

from apps.mastermind.core.domain.domain import Color
from config.settings import settings
from main import app
from tests.stubs import GameMother


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
        await GameMother().a_game(
            4, 4, 2, [Color.RED, Color.RED, Color.RED, Color.YELLOW], reference="MYREF"
        )

        response = api_client.get("/api/games/")

        expected_response = {
            "results": contains_exactly(
                has_entries(
                    {
                        "num_colors": 4,
                        "secret_code": [
                            Color.RED,
                            Color.RED,
                            Color.GREEN,
                            Color.YELLOW,
                        ],
                        "max_guesses": 2,
                        "reference": "MYREF",
                    }
                )
            )
        }

        assert_that(
            response.status_code, is_(status.HTTP_200_OK), reason=response.json()
        )
        assert_that(response.json(), expected_response)

    async def test_get_game(self, api_client, anyio_backend):
        """Check if retrieve a game correctly"""
        game = await GameMother().a_game(
            4,
            4,
            2,
            [Color.RED, Color.RED, Color.GREEN, Color.YELLOW],
            reference="MYREF",
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
                "state": "running",
            }
        )
        assert_that(response.status_code, is_(status.HTTP_201_CREATED))
        assert_that(response.json(), expected_response)

    async def test_create_guess(self, api_client, anyio_backend):
        """Check if guess create correctly"""
        game = await GameMother().a_game(
            4,
            6,
            2,
            [Color.GREEN, Color.BLUE, Color.YELLOW, Color.RED],
        )

        response = api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": ["orange", "orange", "orange", "orange"]},
        )
        assert_that(
            response.status_code, is_(status.HTTP_200_OK), reason=response.json()
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

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    async def test_retrieve_guesses(self, api_client, anyio_backend):
        """Check if guesses are retrieved correctly"""
        game = await GameMother().a_game(
            4,
            5,
            2,
            [Color.GREEN, Color.BLUE, Color.YELLOW, Color.RED],
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

        assert_that(response.status_code, is_(status.HTTP_200_OK))
        assert_that(response.json(), expected_response)

    @pytest.mark.parametrize(
        "secret_code,guess,white_pegs,black_pegs",
        [
            (
                [Color.RED, Color.GREEN, Color.GREEN, Color.BLUE],
                [Color.RED, Color.GREEN, Color.GREEN, Color.BLUE],
                0,
                4,
            ),
            (
                [Color.RED, Color.RED, Color.RED, Color.RED],
                [Color.BLUE, Color.YELLOW, Color.ORANGE, Color.BLUE],
                0,
                0,
            ),
            (
                [Color.GREEN, Color.BLUE, Color.BLUE, Color.RED],
                [Color.GREEN, Color.BLUE, Color.RED, Color.BLUE],
                2,
                2,
            ),
            (
                [Color.BLUE, Color.BLUE, Color.BLUE, Color.RED],
                [Color.RED, Color.BLUE, Color.GREEN, Color.GREEN],
                1,
                1,
            ),
            (
                [Color.RED, Color.BLUE, Color.GREEN, Color.GREEN],
                [Color.BLUE, Color.BLUE, Color.BLUE, Color.RED],
                1,
                1,
            ),
            (
                [Color.BLUE, Color.BLUE, Color.BLUE, Color.RED],
                [Color.BLUE, Color.BLUE, Color.BLUE, Color.RED],
                0,
                4,
            ),
            (
                [Color.WHITE, Color.BLUE, Color.WHITE, Color.BLUE],
                [Color.BLUE, Color.WHITE, Color.BLUE, Color.WHITE],
                4,
                0,
            ),
            (
                [Color.ORANGE, Color.ORANGE, Color.ORANGE, Color.WHITE],
                [Color.ORANGE, Color.WHITE, Color.WHITE, Color.WHITE],
                0,
                2,
            ),
        ],
    )
    async def test_one_white_peg(
        self, api_client, secret_code, guess, white_pegs, black_pegs, anyio_backend
    ):
        """Check if return one white peg"""
        game = await GameMother().a_game(
            4,
            6,
            2,
            secret_code,
        )

        api_client.post(
            f"/api/games/{game.id}/guesses/",
            json={"code": [c.value for c in guess]},
        )
        response = api_client.get(f"/api/games/{game.id}/")

        self.assert_guess(response, white_pegs, black_pegs)
