#!bash
#Examples from: http://edition.cnn.com/2015/09/17/arts/math-art/index.html

python mathart.py -c red -C blue -n 25000 -o "artwork1.png" -e line -X1 "sin(108.0*pi*k/n)*sin(4.0*pi*k/n)" -Y1 "cos(106.0*pi*k/n)*sin(4.0*pi*k/n)" -X2 "sin(104.0*pi*k/n)*sin(4.0*pi*k/n)" -Y2 "cos(102.0*pi*k/n)*sin(4.0*pi*k/n)"
python mathart.py -c black -C blue -n 25000 -o "artwork2.png" -e line -X1 "3.0/4.0*cos(86.0*pi*k/n)" -Y1 "sin(84.0*pi*k/n)**5" -X2 "sin(82.0*pi*k/n)**5" -Y2 "3.0/4.0*cos(80.0*pi*k/n)"

python mathart.py -c red -C blue -n 25000 -o "artwork3.png" -e circle -Xc "sin(14.0*pi*k/n)" -Yc "cos(26.0*pi*k/n)**3" -R "1.0/4.0*cos(40.0*pi*k/n)**2"
python mathart.py -c red -C blue -n 25000 -o "artwork4.png" -e circle -Xc "cos(6.0*pi*k/n)" -Yc "sin(20.0*pi*k/n)**3" -R "1.0/4.0*cos(42.0*pi*k/n)**2"
python mathart.py -c red -C blue -n 25000 -o "artwork5.png" -e circle -Xc "cos(6.0*pi*k/n)" -Yc "sin(14.0*pi*k/n)**3" -R "1.0/4.0*cos(66.0*pi*k/n)**2"
python mathart.py -c black -C blue -n 25000 -o "artwork6.png" -e circle -Xc "cos(14.0*pi*k/n)**3" -Yc "sin(24.0*pi*k/n)**3" -R "1.0/3.0*cos(44.0*pi*k/n)**4"
python mathart.py -c red -C green -n 25000 -o "artwork7.png" -e circle -Xc "sin(22.0*pi*k/n)**3" -Yc "cos(6.0*pi*k/n)" -R "1.0/5.0*cos(58.0*pi*k/n)**2"
python mathart.py -c yellow -C blue -n 25000 -o "artwork8.png" -e circle -Xc "cos(2.0*pi*k/n)" -Yc "sin(18.0*pi*k/n)**3" -R "1.0/4.0*cos(42.0*pi*k/n)**2"

