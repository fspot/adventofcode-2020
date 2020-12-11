import re
from pathlib import Path
from typing import Any, Literal, Optional
from pydantic import BaseModel, Field, ValidationError, validator


class PassportData(BaseModel):
    ecl: Literal['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    cid: Optional[Any]
    pid: str
    byr: int = Field(ge=1920, le=2002)
    iyr: int = Field(ge=2010, le=2020)
    eyr: int = Field(ge=2020, le=2030)
    hgt: str
    hcl: str

    @validator('pid')
    def should_be_valid_pid(cls, pid: str) -> str:
        if not re.fullmatch(r'\d{9}', pid):
            raise ValueError('Invalid pid: ' + pid)
        return pid

    @validator('hcl')
    def should_be_valid_hcl(cls, hcl: str) -> str:
        if not re.fullmatch(r'\#[0-9a-f]{6}', hcl):
            raise ValueError('Invalid hcl: ' + hcl)
        return hcl

    @validator('hgt')
    def should_be_valid_hgt(cls, hgt: str) -> str:
        hgt, unit = hgt[:-2], hgt[-2:]
        if unit == 'in':
            ok = 59 <= int(hgt) <= 76
        elif unit == 'cm':
            ok = 150 <= int(hgt) <= 193
        else:
            ok = False

        if not ok:
            raise ValueError('Invalid hgt: ' + hgt)

        return hgt


def is_valid(infos: dict) -> bool:
    try:
        PassportData(**infos)
        return True
    except ValidationError as e:
        print(e)
        return False


lines = Path('input.txt').read_text().split('\n\n')

total_valid = 0

for line in lines:
    infos = line.split()
    infos = {elem.split(':')[0]: elem.split(':')[1] for elem in infos}
    total_valid += is_valid(infos)

print(total_valid)
