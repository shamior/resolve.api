import pycountry
from pydantic import BaseModel, Field

brasil = pycountry.countries.get(alpha_3="BRA")


class CountryPresentable(BaseModel):
    code: str = Field(examples=[brasil.alpha_3 if brasil is not None else ""])
    name: str = Field(examples=[brasil.name if brasil is not None else ""])
