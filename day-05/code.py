from pathlib import Path

lines = Path('input.txt').read_text().splitlines(keepends=False)


def process_seat_infos(si: str) -> int:
    assert len(si) == 7 + 3
    row = si[:7]
    seat = si[-3:]
    row_int = int(row.replace('F', '0').replace('B', '1'), 2)
    column_int = int(seat.replace('L', '0').replace('R', '1'), 2)
    seat_id = row_int * 8 + column_int
    print(f'- {si}: row {row_int}, column {column_int}, seat ID {seat_id}.')
    return seat_id


seat_ids = []
for line in lines:
    seat_ids.append(process_seat_infos(line))

# Ex 1:
print(max(seat_ids))

# Ex 2:
for i in range(max(seat_ids)):
    if i not in seat_ids and i - 1 in seat_ids and i + 1 in seat_ids:
        print(i)
