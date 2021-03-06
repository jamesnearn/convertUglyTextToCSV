import re
from subprocess import call

def c(txt):
  return ', ' + txt.replace(',', '')

with open('products.txt') as f:
  content = f.read().splitlines()

#                       0    1    2           3              4              5              6
mainLine = re.compile("(.*) (..) (\d+\.\d\d) ([\d,]+\.\d\d) ([\d,]+\.\d\d) ([\d,]+\.\d\d) ([\d,]+\.\d\d)")

fixed = '' 

for index in range(0, len(content) - 1):
  content[index] = content[index].replace('1.00 EA', 'XX')

for index in range(0, len(content) - 1):
  matches = mainLine.findall(content[index])
  matches2 = mainLine.findall(content[index + 1])

  if len(matches) > 0 and len(matches2) > 0:
    m = matches[0]
    fixed += m[0].replace(',', '-') + c(m[1]) + c(m[2]) + c(m[3]) + c(m[4]) + c(m[5]) + c(m[6]) + '\n'
  elif len(matches) > 0 and len(matches2) == 0:
    m = matches[0]
    fixed += m[0].replace(',', '-') + ' ' + content[index+1].replace(',', '-') + c(m[1]) + c(m[2]) + c(m[3]) + c(m[4]) + c(m[5]) + c(m[6]) + '\n' 

fixed = fixed.replace('XX', '1.00 EA')


newLine = re.compile("(.*), (.*), (.*), (.*), (.*), (.*), (.*)")
for item in fixed.splitlines():
  items = newLine.findall(item)
  if len(items) == 1:
    if items[0][2] == "0.00":
      call(["./saveIt.sh", items[0][3], items[0][0], items[0][6]])
    else:
      call(["./saveIt.sh", items[0][2], items[0][0], items[0][6]])
  else:
    print(len(items))

outfile = open("fixed.csv", 'w')
for fixedline in fixed:
  outfile.write(fixedline)
outfile.close()
