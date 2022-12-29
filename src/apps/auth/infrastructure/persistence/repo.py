from apps.auth.core.domain import User
from apps.auth.core.interfaces import IUserRepository
from apps.shared.typing import Id


class UserRepository(IUserRepository):
    def __init__(self) -> None:
        self.users = {
            1: User(
                id=1,
                username="john.doe",
                hashed_password="$2b$12$0uOBanwHitgfFzfczVMd2esadO0rzBtbnTsjmqb1Oybplsc14jzk2",
            ),
            2: User(
                id=2,
                username="johnny.bravo",
                hashed_password="$2b$12$0uOBanwHitgfFzfczVMd2esadO0rzBtbnTsjmqb1Oybplsc14jzk2",
            ),
        }

    async def get(self, id: Id) -> User | None:
        return self.users.get(id)

    async def get_by_username(self, username: str) -> User | None:
        if username == "john.doe":
            return self.users[1]
        if username == "johnny.bravo":
            return self.users[2]
        return None
