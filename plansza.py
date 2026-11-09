from enums import *
import copy
import position_parser


class Plansza:

    def __init__(self, rozmiar: int, sgf: str = ""):

        self.plansza = [[Tile.BORDER for _ in range(rozmiar + 2)] if i == 0 or i == rozmiar + 1 else [Tile.BORDER if k == 0 or k == rozmiar + 1 else Tile.EMPTY for k in range(rozmiar + 2)] for i in range(rozmiar + 2)]
        # Ta linijka u góry tworzy planszę w jednej linijce. (Mogłem to zrobić w bardziej rozbudowanej funckji ale python to python :P)

        # 55555555555
        # 50000000005    (5 to ramka, a 0 to pusty tile. jeśli rozmiar jest podany 9 to jest 11 rzędów i 11 kolumn ponieważ ramka z każdej strony liczy się jako pole)
        # 50000000005
        # 50000000005
        # 50000000005
        # 50000000005
        # 50000000005
        # 50000000005
        # 50000000005
        # 50000000005
        # 55555555555

        self.punkty_czarne = 0
        self.punkty_biale = 0

        self.rozmiar = rozmiar
        self.poprzednia = None  ## plansza sprzed ostatniego ruchu, potrzebna do ko

        if sgf != "":
            self.plansza = position_parser.parse_position_from_sgf(rozmiar, sgf)

    def debug_printuj_plansze(self, plansza): ## Nie do używania !!!

        slownik = {
                Tile.EMPTY.value: "\033[48;5;0m*\033[0m",
                Tile.BLACK.value: "\033[48;5;27m*\033[0m",
                Tile.WHITE.value: "\033[48;5;28m*\033[0m",
                Tile.BLACK_POINT.value: "\033[48;5;52m*\033[0m",
                Tile.WHITE_POINT.value: "\033[48;5;60m*\033[0m",
                Tile.BORDER.value: "\033[48;5;58m*\033[0m",
                Tile.TEMP_ONE.value: "\033[48;5;222m*\033[0m",
                Tile.TEMP_ZERO.value: "\033[48;5;55m*\033[0m",
                Tile.TEMP_OPPOSITE_ONE.value: "\033[48;5;141m*\033[0m",
                Tile.TEMP_OPPOSITE_ZERO.value: "\033[48;5;142m*\033[0m",
                Tile.WHITE_DEAD.value: "\033[48;5;210m*\033[0m",
                Tile.BLACK_DEAD.value: "\033[48;5;211m*\033[0m"
                }
        print(
            "Legenda: "
            "\033[48;5;0mPusty\033[0m",
            "\033[48;5;27mCzarny\033[0m",    ### Zrobione na szybko ale potrzebne aby łatwiej odnajdywać się w planszy (:
            "\033[48;5;28mBiały\033[0m",
            "\033[48;5;52mCzarnyPunkt\033[0m",
            "\033[48;5;60mBiałyPunkt\033[0m",
            "\033[48;5;58mRamka\033[0m",
            "\033[48;5;222mTempJeden\033[0m",
            "\033[48;5;55mTempZero\033[0m",
            "\033[48;5;141mTempOppositeOne\033[0m",
            "\033[48;5;142mTempOppositeZero\033[0m",
            "\033[48;5;210mWhiteDead\033[0m",
            "\033[48;5;211mBlackDead\033[0m"
        )
        print("    ", end="")
        for i in range(len(plansza)):
            print(str(i % 10), end="")
        print()
        try:
            for rzad in range(len(plansza)):
                print(str(rzad) + (".  " if rzad < 10 else ". "), end="")
                for kolumna in range(len(plansza[rzad])):
                    print(f"{slownik[plansza[rzad][kolumna].value]}", end="")
                print()
        except:
            pass

    def grupa(self, rzad, kolumna):
        ## zwraca kamienie połączone z tym na (rzad, kolumna) i ich oddechy
        kolor = self.plansza[rzad][kolumna]
        kamienie = [(rzad, kolumna)]
        oddechy = []

        i = 0
        while i < len(kamienie):
            r, k = kamienie[i]
            i += 1

            for nr, nk in ((r - 1, k), (r + 1, k), (r, k - 1), (r, k + 1)):
                if self.plansza[nr][nk] == Tile.EMPTY and (nr, nk) not in oddechy:
                    oddechy.append((nr, nk))
                elif self.plansza[nr][nk] == kolor and (nr, nk) not in kamienie:
                    kamienie.append((nr, nk))

        return kamienie, oddechy

    def postaw(self, rzad, kolumna, czy_czarny):
        if self.plansza[rzad][kolumna] != Tile.EMPTY:
            return False

        stara = copy.deepcopy(self.plansza)

        przeciwnik = Tile.WHITE if czy_czarny else Tile.BLACK
        self.plansza[rzad][kolumna] = Tile.BLACK if czy_czarny else Tile.WHITE

        ## zbijanie kamieni przeciwnika które nie mają już oddechów
        for nr, nk in ((rzad - 1, kolumna), (rzad + 1, kolumna), (rzad, kolumna - 1), (rzad, kolumna + 1)):
            if self.plansza[nr][nk] == przeciwnik:
                kamienie, oddechy = self.grupa(nr, nk)

                if len(oddechy) == 0:
                    for r, k in kamienie:
                        self.plansza[r][k] = Tile.EMPTY

        ## samobójstwo
        kamienie, oddechy = self.grupa(rzad, kolumna)
        if len(oddechy) == 0:
            self.plansza = stara
            return False

        ## ko - nie można od razu odbić
        if self.plansza == self.poprzednia:
            self.plansza = stara
            return False

        self.poprzednia = stara
        return True

    def policz(self, martwe, komi):
        ## liczenie po chińsku: żywe kamienie + puste pola otoczone tylko przez jeden kolor
        ## martwe kamienie liczą się jak puste pola
        punkty_czarne = 0
        punkty_biale = komi
        wynik = copy.deepcopy(self.plansza)
        sprawdzone = []

        for rzad in range(1, self.rozmiar + 1):
            for kolumna in range(1, self.rozmiar + 1):
                tile = self.plansza[rzad][kolumna]

                if tile in (Tile.BLACK, Tile.WHITE) and (rzad, kolumna) not in martwe:
                    if tile == Tile.BLACK:
                        punkty_czarne += 1
                    else:
                        punkty_biale += 1
                    continue

                if (rzad, kolumna) in sprawdzone:
                    continue

                ## szukamy całego obszaru i sprawdzamy jakie kolory są dookoła
                obszar = [(rzad, kolumna)]
                kolory = []
                i = 0
                while i < len(obszar):
                    r, k = obszar[i]
                    i += 1

                    for nr, nk in ((r - 1, k), (r + 1, k), (r, k - 1), (r, k + 1)):
                        t = self.plansza[nr][nk]

                        if t == Tile.BORDER:
                            continue

                        if t in (Tile.BLACK, Tile.WHITE) and (nr, nk) not in martwe:
                            if t not in kolory:
                                kolory.append(t)
                        elif (nr, nk) not in obszar:
                            obszar.append((nr, nk))

                sprawdzone += obszar

                for r, k in obszar:
                    if self.plansza[r][k] == Tile.BLACK:
                        wynik[r][k] = Tile.BLACK_DEAD
                    elif self.plansza[r][k] == Tile.WHITE:
                        wynik[r][k] = Tile.WHITE_DEAD

                    if kolory == [Tile.BLACK]:
                        punkty_czarne += 1
                        if self.plansza[r][k] == Tile.EMPTY:
                            wynik[r][k] = Tile.BLACK_POINT
                    elif kolory == [Tile.WHITE]:
                        punkty_biale += 1
                        if self.plansza[r][k] == Tile.EMPTY:
                            wynik[r][k] = Tile.WHITE_POINT

        return punkty_czarne, punkty_biale, wynik
