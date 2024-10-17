from pathlib import Path

f_dir = Path('files')
f_dir.mkdir(exist_ok=True)

f_file = Path(f_dir/'first.txt')
s_file = Path(f_dir / 'second.txt')

with open(f_file, 'w') as first:
    first.write('first comment\n')
    first.write('third comment\n')
    first.write('second comment\n')

with open(s_file, 'w') as second:
    second.write('my comment \n')
    second.write('your comment \n')
    second.write('their comment \n')

with open('files/first.txt') as first:
    for fir in first:
        print(fir)

with open('files/second.txt') as s:
    for i in s:
        print(i)


f_file.unlink()
s_file.unlink()

f_dir.rmdir()
