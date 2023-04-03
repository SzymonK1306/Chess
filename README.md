## Program składa się z plików
- main.py - plik z klasą okna głównego
- chess_scene.py - plik z klasą sceny, na której rozgrywana jest partia (dziedziczenie po QGraphicsScene)
- piece.py - plik z klasą pojedynczej bierki (dziedziczenie po QGraphicsPixmapItem)
- piece.py - plik z klasą pola szachowego (dziedziczenie po QGraphicsPixmapItem)
- clock.py - plik z klasą zegara szachowego (dziedziczenie po QGraphicsScene)
- logic.py - plik z klasą logiki szachowej, plansza jako numpy array
- promotion.py - plik z klasą okna dialogowego przy promocji piona

## Przyjęte założenia
- Po wciśnięciu prawego przycisku myszy jest możliwość zmiany grafiki figur i pól
- Bierkę należy przeciągnąć w podświetlone pole
- Po wykonaniu ruchu należy kliknąć w zegar
- W polu tekstowym można wykonać ruch wpisując długą notację szachową, np. "Ka2-a3" - ruch króla, "a2-a4" - ruch piona
- Szach sygnalizowany jest czerwonym podświetleniem szachowanego króla
- W przypadku mata pojawia się odpowiedni komunikat, gra się nie zamyka, ale żaden ruch nie jest możliwy do wykonania
- Wszystkie grafiki zaciągnięto z pliku .rc
- W przypadku promocji piona pojawia się okno wyboru figury
- Zaaplikowano bicie w przelocie, roszadę
- Niemożliwe jest wykonanie zabronionych ruchów, w przypadku takiej próby bierka wraca na swoje miejsce
- W ruchy zabronione wliczane są te, które powodują odsłonięcie króla

Wykonano wszystkie punkty zadania, zatem moim zdaniem na 15 punktów