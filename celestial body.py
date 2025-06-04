from math import *
'''
oto klasa która będzie reprezentować Ziemię i kometę
Deklaruje je się tak jak poniżej:
Ziemia = celestial_body(a_z, e_z, i_z, t_0_z, arg_of_per_z, long_of_asc_z, r_z, t_z, 1.9891*10**30, 6.6743*10**-11)
Gdzie:
a - półoś wielka[m]
e - mimośród[bez jednostek]
i - inklinacja[stopnie]
t_0 - czas przejścia przez perycentrum[s]
arg_of_per - argument perycentrum[stopnie]
long_of_asc_z - długość węzła wstępującego[stopnie]
Przyjmujemy standardową konwencję - inklinację liczymy względem ekliptyki, długość węzła wstępującego od punktu barana
i argument perycentrum wzrasta zgodnie z kierunkiem ruchu ciała.

Anomalia prawdziwa theta = 0 dla przejścia przez perycentrum, narasta wraz z ruchem ciała.

Program oblicza współrzędne x, y, z oraz składowe v_x, v_Y, v_z

do konwersji współrzędnych potrzebny jest jeszcze czas t[s] w momencie początka symulacji(UWAGA, nie jest
on używany do obliczania czegokolwiek bezpośrednio, podobnie t_0. Jest to informacja dla programu, że gdy
 t < t_0 to ciało się zbliża do Słońca, a gdy t > t_0, to ciało się oddala) oraz początkowa odległość od Słońca r[m]. Potrzebna
 jest także masa ciała centralnego M i stała grawitacji G. 

Wykorzytuję układ współrzędnych kartezjańskich, gdzie oś x leci w kierunku punktu barana, z jest prostopadłe do ekliptyki, a y
jest prostopadłe do x i z i jednocześnie ukłąd pozostaje prawoskrętny(tzn. od osi x do osi y obracamy się przeciwnie do wskazówek zegara)
. Innymi słowy jest to najprostrzy szkolny układ współrzędnych. Słońce jest w punkcie (0, 0, 0)

Pomocniczo wykorzystuję sferyczny układ współrzędnych. Kąt phi jest u mnie w zakresie -90 <= phi <= 90
theta = 0 jest dla kierunku dodatnich X-ów. 

dodatkowo obliczany jest moment pędu L
'''


class celestial_body:
    def __init__(self, a, e, i, t_0, arg_of_per, long_of_asc, r, t, M, G):
        self.a = a
        self.e = e
        self.i = radians(i)
        self.t_0 = t_0
        self.arg_of_per = radians(arg_of_per)
        self.long_of_asc = radians(long_of_asc)
        self.r = r
        self.t = t
        self.x = 0
        self.y = 0
        self.z = 0
        self.v_x = 0
        self.v_y = 0
        self.v_z = 0
        self.M = M
        self.G = G
        self.L = sqrt(self.G*self.M * self.a * (1 - self.e**2))
        self.convert_cartesian_coordinates()

    def convert_cartesian_coordinates(self):
        cos_theta = ((self.a*(1 - self.e**2)/self.r) - 1)/self.e
        theta = 0
        if(self.t > self.t_0):
            theta = acos(cos_theta)
        else:
            theta = 2*pi - acos(cos_theta)
        angle_1 = self.arg_of_per+theta
        self.z = sin(self.i) * sin(angle_1) * self.r
        cos_vertical = sqrt(1 - (sin(self.i) * sin(self.arg_of_per + theta))**2)
        if(self.i > pi/2):
            cos_vertical *= -1
        cos_horizontal = cos(angle_1)/cos_vertical
        sin_horizontal = sqrt(1 - cos_horizontal**2)
        if angle_1 > pi:
            sin_horizontal *= -1
        self.x = self.r*cos_vertical * cos_horizontal
        self.y = self.r*cos_vertical * sin_horizontal
    def calculate_Velocity(self):
        self.v_x = self.v_x
