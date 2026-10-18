from enums import *
import gra

#############################
##    KONFIGURACJA         ##
#############################

DEBUG = False    ### Jeśli true: gra uruchamia się bez GUI w pygame CE (jedynie tui w terminalu)
ROZMIAR_PLANSZY = 16  ### Ilość pól na planszy (nie wliczając barierki)
KOMI = 6.5  #### bonus dla białych
POCZATKOWA_POZYCJA = "B[gh];W[gi];B[hh];W[hi];B[hg];W[ih];B[kg];W[ig];B[hf];W[if];B[kf];W[he];B[gg];W[ge];B[fg];W[ef];B[kd];W[fe];B[bg];W[eg];B[ci];W[fh]"   ### Początkowa pozycja gry w formacie SGF z gry playgogame.org

## przykładowa pozycja: W[fb];W[hb];W[jb];B[fc];B[gc];B[hc];B[ic];B[jc];B[kc];W[lc];W[mc];W[ed];B[fd];B[ld];W[md];W[de];W[ee];B[fe];B[le];W[me];W[ef];B[ff];B[gf];B[hf];B[lf];W[mf];B[eg];W[fg];W[gg];W[hg];B[ig];B[lg];W[dh];B[eh];W[gh];W[hh];B[ih];B[kh];B[lh];W[mh];B[fi];B[gi];B[hi];B[ii];B[ji];W[fj];W[gj];W[hj];W[ij];W[jj];W[kj];W[lj]
## przykład 2: B[gh];W[gi];B[hh];W[hi];B[hg];W[ih];B[kg];W[ig];B[hf];W[if];B[kf];W[he];B[gg];W[ge];B[fg];W[ef];B[kd];W[fe];B[bg];W[eg];B[ci];W[fh]

#############################
##    Koniec Konfiguracji  ##
#############################



game = gra.Gra(ROZMIAR_PLANSZY, KOMI, POCZATKOWA_POZYCJA, DEBUG)

        
if DEBUG:
    game.graj(-1, -1, False, True, True)
else:
    game.zacznij_gre()
