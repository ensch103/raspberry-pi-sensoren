# raspberry-pi-sensoren

In die Datei curves.txt werden die Steigungen und y-Achsenabschnitte der Geraden geschrieben.
In die Datei calibration.txt werden die Ro-Werte nach der Kalibrierung geschrieben.
Auf beide Dateien wird nachher bei jeder Messung zugegriffen.

Um zu kalibrieren, muss die Datei calibration.py ausgeführt werden. Dabei werden die 
Dateien calibrated.txt und curves.txt geschrieben und ggf überschrieben.

Um zu messen, muss die Datei main.py ausgeführt werden. Die Messergebnisse werden in die Datei
results.txt geschrieben. Diese Datei wird nicht überschrieben, sondern es werden alle neuen
Messwerte angehängt.

**kalibrieren:** *python calibration.py*  
-> erzeugt Dateien calibrated.txt und curves.txt mit Ro-Werten, Geradensteigungen und 
y-Achsenabschnitten

**messen:** *python main.py*  
-> schreibt Messwerte in Datei "results.txt" (Rs aller 4 Sensoren in Ohm, 
CH4-, CO-, Ozon-, Toluol-, Ammoniak- und Wasserstoffkonzentration je in ppm)