from PIL import Image

# Путь к файлу, который следует обработать.

PathToFile = 'D:\Demo DXF Files\qrcode.png'

# Расстояние в пикселях от основного изображения, чтобы компенсировать
# эффекты разгона/торможения при использовании FlyCut.

Offset = 40

# Расстояние между пикселями в миллиметрах (диаметр точки от лазера)

PixelSize = 0.15

# Длина линии пикселя. Управляющие программы не понимают примитив "точка",
# В качестве точки выступит линия очень малой длины.

Pix = 0.05

# Посчет повторяющихся элементов в строке


def Counter(A):
    Q = []
    count = 1
    for i in range(0, len(A)-1):
        if A[i] == A[i+1]:
            count = count+1
        else:
            Q.append((i-count+1, A[i], count))
            count = 1
    Q.append((i-count+1,  A[i],  count))
    return Q

# Создаем файл с программой перемещений в G-кодах
# Если надо импортировать в CypCut, расширение следует изменить
#  на ".nc"


f = open(PathToFile.split('.', 1)[0]+'.lcc', 'w')

im = Image.open(PathToFile)

# Переменная X позволяет установить масштаб изображения
X = 1
Width = round(im.width*X)
Height = round(im.height*X)
Dim = (Width, Height)
# Изменение размера с учетом масштаба
if X != 1:
    b = im.resize(Dim, 1)
else:
    b = im
# Перевод изображения в однобитный формат
c = b.convert("1", dither=None)
#c.show()
Bitmap = []
Stroka = []

for y in range(0, Height):
    for x in range(0, Width):
        Stroka.append(c.getpixel((x, y)))
    Bitmap.append(Stroka)
    Stroka = []

f.write('G21' + '\n')

for y in range(0, len(Bitmap)):

    Z = Counter(Bitmap[y])

    if y % 2 == 0:

        # Прорисовка полей слева
        f.write('G00 '+'X0'+' Y'+str(Height*PixelSize-y*PixelSize)+'\n')
        f.write('G01 '+'X0.05'+' Y'+str(Height*PixelSize-y*PixelSize)+'\n')

        for x in range(0, len(Z)):
            if Z[x][1] == 0:
                f.write(
                       'G00 ' + 'X' +
                       str(round(Z[x][0]*PixelSize + Offset*PixelSize, 4)) +
                       ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
                       '\n')

                f.write(
                       'G01 ' + 'X' +
                       str(round((Z[x][0]+Z[x][2] + Offset)*PixelSize, 4)) +
                       ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
                       '\n')

        # Прорисовка полей справа
        f.write(
               'G00 ' + 'X' +
               str(round(Width*PixelSize + Offset*2*PixelSize, 4)) +
               ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
               '\n')
        f.write(
               'G01 '+'X' +
               str(round(Width*PixelSize + Offset*2*PixelSize + Pix, 4)) +
               ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
               '\n')

    else:

        # Прорисовка полей справа
        f.write(
               'G00 ' + 'X' +
               str(round(Width*PixelSize + Offset*2*PixelSize + Pix, 4)) +
               ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
               '\n')
        f.write(
               'G01 ' + 'X' +
               str(round(Width*PixelSize + Offset*2*PixelSize, 4)) +
               ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
               '\n')

        for x in range(0, len(Z)):
            if Z[x][1] == 0:
                f.write(
                       'G00 ' + 'X' +
                       str(round((Z[x][0] + Z[x][2] + Offset)*PixelSize, 4)) +
                       ' Y' + str(round(Height*PixelSize - y*PixelSize, 4))
                       + '\n')
                f.write(
                       'G01 ' + 'X' +
                       str(round((Z[x][0] + Offset)*PixelSize, 4)) +
                       ' Y' + str(round(Height*PixelSize-y*PixelSize, 4)) +
                       '\n')

        # Прорисовка полей слева
        f.write(
               'G00 ' + 'X0.05' +
               ' Y' + str(round(Height*PixelSize - y*PixelSize, 4)) +
               '\n')
        f.write(
               'G01 ' + 'X0' +
               'Y'+str(round(Height*PixelSize-y*PixelSize, 4))+'\n')


f.close()
