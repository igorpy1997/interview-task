# README #

This README would normally document whatever steps are necessary to get your application up and running.

### Zadanie kwalifikacyjne ###

1. Dodaj repozytorium bazowego Odoo w wersji 16 ([https://github.com/odoo/odoo/tree/16.0](https://github.com/odoo/odoo/tree/16.0)) jako submoduł tego repozytorium
2. Skonfiguruj bazę danych (Postgres 16). Możesz to zrobić:
	- Natywnie na laptopie. Jeśli wybrałeś tę opcję, uzupełnij sekcję `Konfiguracja bazy danych`
	- Użyć gotowego obrazu Docker. Jeśli wybrałeś tę opcję, załącz `docker-compose.yml` do tego repo
3. Stwórz `odoo.conf`, który umożliwi poprawne uruchomienie Odoo 16 `odoo.conf`, który umożliwi poprawne uruchomienie Odoo 16
4. Stwórz katalog z nowym addonem `interview`
	- Dodaj do konfiguracji, aby Odoo uruchamiało się z włączonym tymże addonem
	- Nowy addon ma być zależny od addona `sale_management`
5. Rozszerzyć model `sale.order.line` o nowe pola: `width` oraz `height` - typu Float
	- Dodać constraint, aby wartości były tylko dodatnie
	- Wyświetlić nowe pola w tabeli linii zamówień we formularzu zamówienia
6. Rozszerzyć model `sale.order.line` o nowe pole `square_meters`
	- Pole ma być niemożliwe do edycji, ma być autoprzeliczane na podstawie `width * height` (załóżmy, że `width` oraz `height` trzymają wartości w centymetrach)
	- Wyświetlić nowe pole w tabeli linii zamówień na formularzu zamówienia
7. Dodać model trzymający informacje o terminie dostawy. Na pewno ma mieć pole: `name`, oraz ewentualnie dodatkowe, jeśli trzeba
	- Dodać nowy menu item w module Sales gdzie będzie możliwość konfiguracji ww. modelu
	- Administrator ma full access, zwykły user tylko odczyt
8. Dodać pole `delivery_term_type`, referencja do modelu z pkt 7, wyświetlić je na formularzu
	- Bez możliwości dodania nowego oraz edycji wybranego terminu z tego poziomu (z poziomu formularza sale ordera)
9. Dodać pole `delivery_date`, typu `Date` do modelu `sale.order`, wyświetlić je na formularzu (pole nieedytowalne)
	- Wyliczać automatycznie pole `delivery_date` w zależności od wybranego terminu dostawy
	- Przykłady:

		`name: Za trzy dni` - wyliczy termin od dziś za 3 dni

		`name: Za tydzień` - wyliczy termin od dziś za 7 dni

		`name: Ostatni dzień miesiąca` - wyliczy termin na ostatni dzień bieżącego miesiąca

		`name: Po niedzieli` - wyliczy termin na kolejny poniedziałek

		To oczywiście tylko przykłady. Zaprojektuj model, aby można było skonfigurować najróżniejsze kombinacje.

10. Dodaj 4 pierwsze przykłady w pliku `.xml` jako dane wsadowe
11. Dodać task cron'owy, uruchamiany raz dziennie (dowolna godzina), który:
	- Szuka wszystkich niezakończonych sale orderów
	- Na nowo wylicza termin dostawy, biorąc pod uwagę bieżącą datę



### Konfiguracja bazy danych
