from dataclasses import dataclass, field
from typing import TypedDict


class _Address(TypedDict):
	city: str
	streetAddressLine1: str
	streetAddressLine2: str
	streetAddressLine3: str
	postalCode: str

class _Coordinates(TypedDict):
	longitude: float
	latitude: float

class _Meta(TypedDict):
	total: int

class StoreDict(TypedDict):
	id: str
	name: str
	address: _Address
	coordinates: _Coordinates
	today: dict[str, str]
	features: list[str]
	hasArtwork: bool

class DataDict(TypedDict):
	data: list[StoreDict]
	meta: _Meta

@dataclass(order = True, frozen = True, slots = True)
class Store:
	id: int
	name: str
	city: str
	address: str
	latitude: float
	longitude: float
	features: list[str] = field(hash = False)
	artwork: bool

def parse(dct: StoreDict) -> Store:
	return Store(
		id = int(dct["id"]),
		name = dct["name"],
		city = dct["address"]["city"],
		address = dct["address"]["streetAddressLine3"],
		latitude = dct["coordinates"]["latitude"],
		longitude = dct["coordinates"]["longitude"],
		features = dct["features"],
		artwork = dct["hasArtwork"])