# README #

### Zadanie kwalifikacyjne ###

1. Dodaj repozytorium bazowego Odoo w wersji 16 ([https://github.com/odoo/odoo/tree/16.0](https://github.com/odoo/odoo/tree/16.0)) jako submoduł tego repozytorium
2. Skonfiguruj bazę danych (Postgres 16). Możesz to zrobić:
	- Natywnie na laptopie. Jeśli wybrałeś tę opcję, uzupełnij sekcję `Konfiguracja bazy danych` w pliku `README.md`
	- Użyć gotowego obrazu Docker. Jeśli wybrałeś tę opcję, załącz `docker-compose.yml` do tego repo
3. Stwórz `odoo.conf`, który umożliwi poprawne uruchomienie Odoo 16. Plik ma umożliwiać lokalne uruchomienie odoo 16. Nie musi działać uniwersalnie.
4. Stwórz katalog `addons` w katalogu głównym repozytorium z nowym addonem `interview`
	- Dodaj do `odoo.conf`, aby moduł był zaczytywany przy starcie systemu
	- Nowy addon ma mieć w swoich zaleznościach moduł `sale_management`
5. Rozszerzyć model `sale.order.line` o nowe pola: `width` oraz `height` - typu Float
	- Dodać constraint, aby wartości były tylko dodatnie
	- Wyświetlić nowe pola w tabeli linii zamówień we formularzu zamówienia
6. Rozszerzyć model `sale.order.line` o nowe pole `square_meters` - typ Float
	- Pole ma być niemożliwe do edycji, ma być autoprzeliczane na podstawie `width * height` (załóżmy, że `width` oraz `height` trzymają wartości w centymetrach)
	- Wyświetlić nowe pole w tabeli linii zamówień na formularzu zamówienia
7. Dodać model `delivery.term.type` trzymający informacje o terminie dostawy. Na pewno ma mieć pole: `name`, oraz jeśli trzeba dodatkowe
	- Dodać nowe menu w zakładce Sales gdzie będzie możliwość konfiguracji ww. modelu
	- Administrator ma full access, zwykły user tylko odczyt
8. Dodać pole `delivery_term_type_id`, referencja do modelu z pkt 7, wyświetlić je na formularzu pod polem klient
	- Bez możliwości dodania nowego oraz edycji wybranego terminu z tego poziomu (z poziomu formularza sale ordera)
9. Dodać pole `delivery_date`, typu `Date` do modelu `sale.order`, wyświetlić je na formularzu (pole nieedytowalne), pod `delivery_term_type_id`
    - Wyliczać automatycznie pole `delivery_date` w zależności od wybranego terminu dostawy
    - Zmiana zawartości pola `delivery_term_type_id` ma automatycznie modyfikować pole `delivery_date`
	- Przykłady:
		`name: Za trzy dni` - wyliczy termin od dziś za 3 dni
		`name: Za tydzień` - wyliczy termin od dziś za 7 dni
		`name: Ostatni dzień miesiąca` - wyliczy termin na ostatni dzień bieżącego miesiąca
		`name: Po niedzieli` - wyliczy termin na kolejny poniedziałek
		To oczywiście tylko przykłady. Zaprojektuj model, aby można było skonfigurować najróżniejsze kombinacje.
10. Dodaj 4 pierwsze przykłady w pliku `.xml` jako dane wsadowe
11. Dodać task cron'owy, uruchamiany raz dziennie (dowolna godzina), który:
	- Szuka wszystkich niezaakceptowanych sale orderów
	- Na nowo wylicza termin dostawy, biorąc pod uwagę bieżącą datę

### Konfiguracja bazy danych

TODO
