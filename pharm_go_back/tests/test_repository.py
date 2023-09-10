import pytest
from repository.interface import MedsRepoProto, Med

new_meds_info = [
    {
        "name": "smekta",
        "price": 3300,
        "pharmacy": "psp"
    },
    {
        "name": "smekta",
        "price": 3200,
        "pharmacy": "aversi"
    },
    {
        "name": "zoloft",
        "price": 1100,
        "pharmacy": "jpc"
    }
]


@pytest.mark.asyncio
async def test_repo_save_new_elem(repository: MedsRepoProto):
    for med in new_meds_info:
        await repository.save_med(Med(**med))

    med_info = await repository.get_med("smekta")

    assert med_info.model_dump() == {
        "name": "smekta",
        "pharmacies": [
            {
                "price": 3300,
                "pharmacy": "psp"
            },
            {
                "price": 3200,
                "pharmacy": "aversi"
            },
        ]
    }
