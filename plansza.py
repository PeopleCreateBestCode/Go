from enums import *
import copy
import position_parser


class Plansza:

    def __init__(self, rozmiar: int, sgf: str = ""):

        self.plansza = [[Tile.BORDER for _ in range(rozmiar + 2)] if i == 0 or i == rozmiar + 1 else [Tile.BORDER if k == 0 or k == rozmiar + 1 else Tile.EMPTY for k in range(rozmiar + 2)] for i in range(rozmiar + 2)]

        self.bonus_za_zbicia_biali = 0
        self.bonus_za_zbicia_czarni = 0
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
        
        if sgf != "":
            self.plansza = position_parser.parse_position_from_sgf(rozmiar, sgf)

    def debug_printuj_plansze(self, plansza): ## Nie do używania !!!
        
        slownik = {
                Tile.EMPTY.value: "\033[48;5;0m*\033[0m",
                Tile.BLACK.value: "\033[48;5;27m*\033[0m",
                Tile.WHITE.value: "\033[48;5;28m*\033[0m",
                Tile.BLACK_POINT.value: "\033[48;5;52m*\033[0m",
                Tile.WHITE_POINT.value: "\033[48;5;52m*\033[0m",
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
    

    def zmien_pole(self, x, y, pole: Tile):

        self.plansza[y][x] = pole
        

    def sprawdz(self, czy_czarne: bool):        
        w = copy.deepcopy(self.plansza)
        
        for rzad in range(len(self.plansza)):
            for kolumna in range(len(self.plansza[rzad])):
                if (rzad,kolumna) == (6,3):
                    pass
                if w[rzad][kolumna] == Tile.EMPTY:
                    w = self.polacz_plansze(w, self.__policz_punkt(w, kolumna, rzad, czy_czarne), czy_czarne)
        
        self.plansza = self.polacz_plansze(w, w, czy_czarne, True)

    def __policz_punkt(
        self,
        plansza: list[list[Tile]],
        x: int,
        y: int,
        czy_czarne: bool
    ) -> list[list[Tile]]:

        tile = Tile.BLACK if czy_czarne else Tile.WHITE
        
        dead_tile = Tile.BLACK_DEAD if czy_czarne else Tile.WHITE_DEAD

        empty = [
            Tile.TEMP_ZERO,
            Tile.TEMP_OPPOSITE_ZERO
        ]

        accepted = [
            Tile.BORDER,
            Tile.BLACK_POINT if czy_czarne else Tile.WHITE_POINT,
            tile,
            Tile.TEMP_ONE,
            Tile.TEMP_OPPOSITE_ONE
        ]

        unaccepted = [
            Tile.WHITE_POINT if czy_czarne else Tile.BLACK_POINT,
            Tile.BORDER
        ]
        
        opposite = Tile.BLACK if not czy_czarne else Tile.WHITE

        temp_plansza = copy.deepcopy(plansza)
        
        odwiedzone: list[tuple[int, int]] = []

        def zamien_wszystkie_na_martwe() -> None:
            for rzad in range(len(temp_plansza)):
                for kolumna in range(len(temp_plansza[rzad])):
                    if temp_plansza[rzad][kolumna] == tile:
                        temp_plansza[rzad][kolumna] = dead_tile

        ##W[fb];W[hb];W[jb];B[fc];B[gc];B[hc];B[ic];B[jc];B[kc];W[lc];W[mc];W[ed];B[fd];B[ld];W[md];W[de];W[ee];B[fe];B[le];W[me];W[ef];B[ff];B[gf];B[hf];B[lf];W[mf];B[eg];W[fg];W[gg];W[hg];B[ig];B[lg];W[dh];B[eh];W[gh];W[hh];B[ih];B[kh];B[lh];W[mh];B[fi];B[gi];B[hi];B[ii];B[ji];W[fj];W[gj];W[hj];W[ij];W[jj];W[kj];W[lj]
        
        def sprawdz_oddech(x: int, y: int) -> None:
            if (x, y) in odwiedzone:
                return

            odwiedzone.append((x, y))
            
            if temp_plansza[y][x] == dead_tile:
                temp_plansza[y][x] = tile
                
            
            for offset_x, offset_y in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ):
                nx = x + offset_x
                ny = y + offset_y

                if (
                    (nx, ny) not in odwiedzone
                    and temp_plansza[ny][nx] == dead_tile
                ):
                    sprawdz_oddech(nx, ny)

        def usun_martwe() -> None:
            for rzad in range(len(temp_plansza)):
                for kolumna in range(len(temp_plansza[rzad])):
                    if temp_plansza[rzad][kolumna] == dead_tile:
                        temp_plansza[rzad][kolumna] = Tile.EMPTY
                        if dead_tile == Tile.WHITE_DEAD:
                            self.bonus_za_zbicia_czarni += 1
                        else:
                            self.bonus_za_zbicia_czarni += 1
        
        def sprawdz_rekursywny(x: int, y: int) -> None:
            
            # self.debug_printuj_plansze(temp_plansza)
            
            if (x, y) in odwiedzone:
                return

            odwiedzone.append((x, y))

            ok_combo = 0

            for offset_x, offset_y in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ):
                nx = x + offset_x
                ny = y + offset_y

                if temp_plansza[ny][nx] in accepted:
                    ok_combo += 1

            if (
                # any(
                #     temp_plansza[y + offset_y][x + offset_x] in unaccepted
                #     for offset_x, offset_y in (
                #         (-1, 0),
                #         (1, 0),
                #         (0, -1),
                #         (0, 1)
                #     )
                # )
                # or
                sum(
                    temp_plansza[y + offset_y][x + offset_x] in empty
                    for offset_x, offset_y in (
                        (-1, 0),
                        (1, 0),
                        (0, -1),
                        (0, 1)
                    )
                ) >= 1
            ):
                ok_combo = 0

            if ok_combo >= 2 and temp_plansza[y][x] not in unaccepted:
                temp_plansza[y][x] = Tile.TEMP_ONE if temp_plansza[y][x] != opposite else Tile.TEMP_OPPOSITE_ONE
            else:
                temp_plansza[y][x] = Tile.TEMP_ZERO if temp_plansza[y][x] != opposite else Tile.TEMP_OPPOSITE_ZERO
            
            for offset_x, offset_y in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ):
                nx = x + offset_x
                ny = y + offset_y

                if (
                    (nx, ny) not in odwiedzone
                    and temp_plansza[ny][nx] in [Tile.EMPTY, opposite]
                ):
                    sprawdz_rekursywny(nx, ny)
        
        def rozsiej_zero(x: int, y: int) -> None:
            if (x, y) in odwiedzone:
                return

            odwiedzone.append((x, y))

            if temp_plansza[y][x] == Tile.TEMP_ONE:
                temp_plansza[y][x] = Tile.TEMP_ZERO
            elif temp_plansza[y][x] == Tile.TEMP_OPPOSITE_ONE:
                temp_plansza[y][x] = Tile.TEMP_OPPOSITE_ZERO
            
            for offset_x, offset_y in (
                (-1, 0),
                (1, 0),
                (0, -1),
                (0, 1)
            ):
                nx = x + offset_x
                ny = y + offset_y

                if (
                    (nx, ny) not in odwiedzone
                    and temp_plansza[ny][nx] in [Tile.BLACK_POINT, Tile.WHITE_POINT, Tile.TEMP_ONE, Tile.TEMP_OPPOSITE_ONE, Tile.TEMP_ZERO, Tile.TEMP_OPPOSITE_ZERO]
                ):
                    rozsiej_zero(nx, ny)
    

        zamien_wszystkie_na_martwe()
        
        # self.debug_printuj_plansze(temp_plansza)
        
        odwiedzone = []
        
        for rzad in range(len(temp_plansza)):
            for kolumna in range(len(temp_plansza[rzad])):
                if temp_plansza[rzad][kolumna] in [Tile.EMPTY, Tile.TEMP_ONE, Tile.BLACK_POINT, Tile.WHITE_POINT]:
                    sprawdz_oddech(kolumna, rzad)
        
        # self.debug_printuj_plansze(temp_plansza)
        
        usun_martwe()
        
        # self.debug_printuj_plansze(temp_plansza)
        
        odwiedzone = []
        
        sprawdz_rekursywny(x, y)
        
        # self.debug_printuj_plansze(temp_plansza)
        
        for odw in odwiedzone[::-1]:
            if temp_plansza[odw[1]][odw[0]] in [Tile.TEMP_ZERO, Tile.TEMP_OPPOSITE_ZERO]: 
                odwiedzone = []
                rozsiej_zero(*odw)
                break
        
        return temp_plansza

    def polacz_plansze(self, stara_plansza: list[list[Tile]], w: list[list[Tile]], czy_czarne: bool, normalize: bool = False):
        nowa_plansza = [[Tile.EMPTY for j in range(len(self.plansza))] for i in range(len(self.plansza))]
                
        final_punkt = Tile.BLACK_POINT if czy_czarne else Tile.WHITE_POINT
        
        translator = {
            Tile.TEMP_ONE: final_punkt,
            Tile.TEMP_ZERO: Tile.EMPTY,
            Tile.TEMP_OPPOSITE_ZERO: Tile.BLACK if not czy_czarne else Tile.WHITE,
            Tile.TEMP_OPPOSITE_ONE: Tile.BLACK if not czy_czarne else Tile.WHITE
        }
        
        for i in range(len(nowa_plansza)):
            for j in range(len(nowa_plansza[i])):
                if w[i][j] == Tile.TEMP_ONE and normalize:
                    nowa_plansza[i][j] = final_punkt
                elif w[i][j] in [Tile.TEMP_ONE, Tile.TEMP_ZERO, Tile.TEMP_OPPOSITE_ONE, Tile.TEMP_OPPOSITE_ZERO] and not normalize:
                    nowa_plansza[i][j] = w[i][j]
                else:
                    if w[i][j] in translator:
                        nowa_plansza[i][j] = translator[w[i][j]]
                    else:
                        nowa_plansza[i][j] = stara_plansza[i][j]
        
        return nowa_plansza
