import typing

from pydantic import BaseModel


class Med(BaseModel):
    name: str
    price: int
    pharmacy: str


class MedInPharmacy(BaseModel):
    pharmacy: str
    price: int


class MedInfo(BaseModel):
    name: str
    pharmacies: list[MedInPharmacy]


class MedsRepoProto(typing.Protocol):

    async def get_med(self, med_name: str) -> MedInfo | None: ...

    async def save_med(self, med: Med) -> None: ...
