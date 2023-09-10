from repository.interface import MedInfo, Med


class MedsRepoLocal:

    def __init__(self):
        self._repo = {
            "loperamid": [
                {
                    "pharmacy": "JPC",
                    "price": 520
                },
                {
                    "pharmacy": "aversi",
                    "price": 530
                }
            ],
            "loratadin": [
                {
                    "pharmacy": "Pharmadepo",
                    "price": 1100
                },
                {
                    "pharmacy": "aversi",
                    "price": 1200
                }
            ]
        }

    async def get_med(self, med_name: str) -> MedInfo | None:
        if med := self._repo.get(med_name):
            med_info = {
                "name": med_name,
                "pharmacies": med
            }
            return MedInfo(**med_info)
        return None

    async def save_med(self, med: Med) -> None:
        new_info = {
            "pharmacy": med.pharmacy,
            "price": med.price
        }
        if med_info := self._repo.get(med.name):  # type: list[dict]
            med_info.append(new_info)
        else:
            self._repo[med.name] = [new_info, ]
