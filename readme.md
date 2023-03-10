# Monopoly Game
Konsolowa gra w Monopoly, dla co najmniej dwóch graczy. Rozgrywka odbywa się poprzez wybieranie przez gracza dostępnych opcji i w ten sposób decydowanie o kolejnych ruchach, zarządzanie nieruchomościami.
## Interfejs i rozgrywka
#### __Dodawanie graczy__
Po uruchomieniu gry wyświetla się baner powitalny oraz najaważniejsze informacje o aktualnej rozgrywce. Gracz jest proszony o wprowadzenie imion pierwszych dwóch graczy, oraz zapytany czy chce dodać więcej graczy.

<img src="img/baner.png" width="650" height = "400"/>

#### __Menu główne__
W danym ruchu można dokonać akcji wybranych z głównego menu.

<img src="img/main_menu.png" width="400" height = "250"/>

Wybranie rzutu kośćmi powoduje automatyczną zmianę gracza, zatem zarządzanie nieruchomościami, tzn. kupowanie domów i stawianie pól pod zastaw musi być dokonane przed ruchem.

#### __Rzut kością__
Po wybraniu opcji numer jeden pokazuje się pole na którym wylądowaliśmy i odpowiednie zapytanie związane z rodzajem tego pola. W tabelce pola nieruchomości wymienione są jedynie najważniejsze parametry.

<img src="img/dice_roll.png" width="200" height = "400"/>

#### __Wyświetlenie aktualnego lub wszystkich graczy__
Opcja wyświetlenia wszystkich graczy, lub własnych kart powoduje wyświetlenie się informacji o graczach oaz ich kartach w postaci tabel, dzięki czemu wszystkie informacje są łatwo dostępne i czytelne. Pod tabelką gracza znajdują się jego nieruchomości. Opcja wyświetlania nieruchomości aktualnego gracza wyświetla więcej parametrów np. ceny zakupu domów i hoteli.

<img src="img/all_players.png" width="270" height = "400"/>

#### __Zarządzanie nieruchomościami__

Opcje 4 - 7 pozwalają a zarządzanie nieruchomościami. Wyświetlona zostaje lista nieruchomości należących do aktualnego gracza, a gracz dokonuje wyboru poprzez wpisanie numeru id wybranego pola.

#### __Menu bankructwa__
Jeśli gracz nie jest w stanie zapłacić należności, ale ma wystarczająco majątku w nieruchomościach, jest zmuszony wybrać którąś z opcji menu bankructwa. Po sprzedży domu/hotelu lub oddaniu pola pod zastaw, opłaca dług i gra toczy się dalej. Jeśli jego majątek jest zbyt mały, gracz bankrutuje i zostaje wyłączony z gry.


<img src="img/bancrupt_menu.png" width="520" height = "200"/>

#### __Zapis gry__

Gracz ma możliwość zapisu gry do pliku o formacie pickle, musi w tym celu podać nazwę pliku. Aby ponownie zrestartować grę, należy uruchomić plik main z argumentem `--load`

``$python3 -m main --load [filename]``

## Wymagania i uruchomienie gry
Użyte zewnętrzne moduły:
``tabulate==0.9.0``

Aby uruchomić grę należy w katalogu monopoly uruchomić plik main.py:

``$python3 -m main``

lub jeśli chcemy uruchomić rozpoczętą grę z pliku:

``$python3 -m main --load [filename]``

## Założenia projektowe i zasady Gry
Gra miała bazować na zasadach z oryginlnego monopoly ([link](https://www.hasbro.com/common/instruct/00009.pdf)), ale być jego uproszczoną wersją.

### Plansza
Na planszy znajdują się pola trzech typów:
- Pola ulice

Mogą być kupowane, posiadacz wszystkich pól w danym kolorze może stawiać na nich domy i hotel.
- Pola nieruchomości

Mogą być kupowane, i pobierać od nich opłaty, ale nie można stawiać na nich domów
- Pola Specjalne

Nie mogą być kupowane, są to np. pole start, pole szansa, pole więzienie.

### Rozgrywka
- Gracze poruszają się po planszy w sposób cykliczny
- Rzucają dwoma kośćmi, a ich suma wyzncza liczbę pól którą mają pokonać
- Po wylądowaniu na danym polu, w zależności od rodzaju pola mogą np. kupić je lub zapłacić właścicielowi czynsz.

### Budowa i sprzedaż domów i hoteli
- Przed każdym ruchem gracz może wybudować dom na dowolnym swoim polu, jeśli spełnia poniższe warunki:
  - posiada wszystkie pola w danym kolorze
  - domy są budowane równomiernie na każdym polu w danym kolorze
  - pole nie jest oddane pod zastaw
- Gdy na danym polu gracz postawi cztery domy, może zamienić je na hotel, dopłacając cenę hotelu.
- Sprzedaż domów również musi odbywać się równomiernie.

### Oddawanie pod zastaw i wykupywanie pola
- Aby oddać pole pod zastaw nie może ono mieć żadnych domów ani hoteli
- Aby wykupić pole, trzeba zapłacić kwotę pożyczki + 10% tej kwoty


### Koniec gry i zwycięzca
Gra konczy się, gdy zostanie osiągnięta maksymalna liczba rund, lub pozostanie tylko jeden gracz, który nie jest bankrutem. Zycięzcą zostaje gracz, który uzbierał największy majątek w gotówce i nieruchomościach.

## Architektura projektu

Projekt składa się z trzech modułów oraz pliku main.
- classes - moduł zawierający pliki z implementacjami klas
- database - moduł z plikami zawierającymi dane pól na planszy i stałymi wartościami wykorzystywanymi w grze
- test - moduł zawierający pliki z testami jednostkowymi zorganizowanymi w klasy

### __Dane pól i kart__

Dane pól są przechowywane w plikach w formacie json, w osobnym pliku pola nieruchomości i ulic, a w  osobnym pola specjalne.
- Przykładowy obiekt pola nieruchomości __PropertyField__:
```
{
        "type": "property",
        "colour": "Grey",
        "field_id": 1,
        "name": "Short Line R.R.",
        "rent": 25,
        "prices": {
            "base_price": 200
        },
        "other_rents": {
            "mortgage": 100,
            "owned_2": 50
        }
    },
```
- Przykładowy obiekt pola ulicy __Street__:
```
{
        "type": "street",
        "colour": "deep blue",
        "field_id": 5,
        "name": "Park Place",
        "rent": 35,
        "other_rents": {
            "w_one_house": 175,
            "w_two_houses": 500,
            "w_three_houses": 1100,
            "w_four_houses": 1300,
            "w_hotel": 1500,
            "mortgage": 175
        },
        "prices": {
            "base_price": 350,
            "house_cost": 200,
            "hotel_cost": 200
        }
    },
```

### __Klasa Field__
- abstrakcyjna klasa reprezentująca pole na planszy

### __Klasa PropertyField__
Reprezentuje pole "nieruchomości"

- dziedziczy po Field
- obiekty tej klasy mogą być własnością danego gracza, ale nie można budować na nich domów
- każdy obiekt ma swój indeks oraz nazwę
- przechowuje dane o opłatach innych niż podstawowa w postaci słownika


### __Klasa Street__
Reprezentuje pole "ulica".

- dziedziczy po PropertyField
- obiekty tej klasy mogą mieć domy i hotele
- przechowuje dane o opłatach innych niż podstawowa w postaci słownika
- przechowuje dane o cenach za domki i hotel w postaci słownika


### __Klasa Board__
Reprezentuje planszę po której poruszają się gracze.

- przechowuje kolekcje obiektów dziedziczących po Field
- przechowuje kolekcję kart szansy
- umożliwia uzyskanie danego pola na podstawie jego indeksu

### __Klasa Player__
Reprezentuje gracza

- Przechowuje listę indeksów pól nieruchomości, które posiada dany gracz
- Przechowuje aktualny stan konta
- obiekt Player może zmieniać swoje położenie na planszy na podstawie aktualnego wyniku rzutu kością
- umożliwia wydawanie i zarabianie pieniędzy


### __Klasa Game__
Reprezentuje stan gry, pozwala na interakcję między obiektami pozostałych klas.

Najważniejszym parametem obiektu klasy Game jest aktualny gracz i aktualne pole na którym gracz stoi. Większość metod dotyczy interakcji między tymi dwoma obiektami.

Metody tej klasy pozwalają na:
- wygenerownaie nowego rzutu kością
- ruchu gracza o wylosowaną liczbę oczek
- kupno pola na którym gracz stanął
- opłacenie czynszu z pola na którym gracz stanął
- oddanie pod zastaw danego pola należącego do gracza
- generowanie opisów graczy i pól planszy

Zawiera także metody pomocnicze udostępniające informacje o stanie gry dla interfejsu.

### __Klasa ChanceCard__
Reprezentuje kartę szansy wylosowaną na polu szansy.

- obiekt karty posiada swój indeks, krótki opis, oraz typ akcji która zostaje wykonana na graczu przy użyciu karty.
- dostępne typy akcji wykonywanych przez kartę są zdefiniowane w klasie dziedziczącej po klasie Enum ChanceFieldAction w pliku chance_card.py

### __fields_from_json.py__
Plik zawiera funkcje umożliwiające wczytanie obiektów PropertyField, SpecialField, Street, ChanceCard z plików w formacie json.

### __game_constants.py__
Plik zawiera klasę GameConstants dziedziczącą po klasie IntEnum. Klasa ta przechowuje stałe wartosci gry, czyli np. maksymalną liczbę graczy, maksymalną liczbę rund, maksymalny index pola na planszy.

### __Interfejs__

W pliku interface.py najważniejszą funkcją jest funcja play, która jest główną pętlą programu i jako argument przyjmuje obiekt klasy Game. Jest to jedyna funkcja wywołana w pliku main i ona wywołuje pozostałe funkcje interfejsu.

Pozostałe funkcje odpowiadają za:
- Przyjęcie od użytkownika okreslonego inputu
- Wyświetlanie menu, informacji o użytkownikach i polach
- Wybieranie opcji z menu
- Sprawdzanie warunków do danej akcji (np. do kupna domu) i wyświetlanie odpowiednich komunikatów w zależności od problemu
- Zapis obecnego stanu gry
- Odczyt stanu gry z pliku
## Testy

W sumie zaimplementowałam 78 testów. Testy zostały pogrupowane w pliki, w niektórych pliakach zostały pogrupowane w klasy.
W pliku test_field.py znajduje sieę klasa TestField oraz TestStreetField, które testują odpowiednio klasę nieruchomości oraz klasę Street.
Najwięcej testów dotyczy klasy Game. W pliku test_game.py znajdują się następujące klasy:
- TestGame
    - testująca główne funkcjonalności klasy Game
- TestHouseBuilding
    - testująca budowanie domów i hoteli, oraz ich sprzedaż
- TestGameWinThreePlayes
    - testująca sytuacje bliskie wygranej w przypadku trzech graczy
- TestGameOtherMethods
    - testująca poszczególne metody klasy Game
- TestMortgage
    - testująca stawianie pól pod zastaw

Interfejs oraz całościowe działąnie programu było testowane manualnie, przeze mnie oraz moich znajomych. Braliśmy pood uwagę różne scenariusze i staraliśmy się doprowadzić do danych sytuacji w grze. Przetestowanie niektórych sytuacji, np. menu bankructwa wymagało utworzenia osobnego pliku testowego main, który uruchamiał grę w odpowiednim stanie.

## To Do
- Sprzedawanie pól innym graczom
- Komputerowy Gracz
- Pole więzienia
    - Klasa Player posiada natomiast parametry umożliwiającą implementację tej funkcjonalności
