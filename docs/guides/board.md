# Board — Twój codzienny punkt startowy

Kiedy otwierasz casedock, pierwsza rzecz którą widzisz to Board. To nie jest dashboard z wykresami. To nie jest lista wszystkiego co masz do zrobienia. To jest **twój widok na dziś** — spokojny, celowy, bez szumu.

## Co jest na Boardzie

Board ma trzy sekcje. Tyle. Nie pięć, nie dziesięć. Trzy.

### 1. Daily Focus

Najważniejsza rzecz na stronie. Twoja praca na dziś.

**Jeden główny Case (Main)** + opcjonalnie **dwa supporting Cases (Secondary)**.

Przykład: Rano siadasz do pracy. Wiesz że dziś chcesz:
- Głównie: naprawić błąd logowania użytkowników
- Jeśli będzie moment: poprawić dokumentację API
- Jeśli będzie moment: odpowiedzieć na email od klienta o integracji

Ustawiasz "Fix login bug" jako Main, a dwa pozostałe jako Secondary. Teraz kiedy otwierasz casedock, od razu wiesz na czym jesteś. Nie musisz myśleć "co miałem robić?" — Board ci przypomina.

**Jeśli nie masz ustawionego focusa**, widzisz spokojny komunikat: "Nothing has the front yet. Pick one main Case and, if useful, up to two secondary Cases." Żadnego_alert.png, żadnego czerwonego wykrzyknika. Po prostu informacja.

Dlaczego max 1 + 2? Bo focus oznacza uwagę. Jeśli wszystko jest ważne, nic nie jest ważne. Trzy case'y to maks tego co realnie możesz mieć w głowie jednego dnia.

### 2. Stale Cases (rzeczy które potrzebują decyzji)

To jest **delikatne przypomnienie**, nie narzekanie.

Jeśli masz aktywny Case którego nie ruszyłeś od 7 dni (domyślnie), Board ci o nim przypomni. Nie listą alarmów, nie powiadomieniem — po prostu jedna karta na Boardzie z napisem "Untouched for 11 days" i trzema opcjami:

- **Done** — zamknij, bo skończone. Często zapominamy zamknąć rzeczy które już działają.
- **Move to waiting** — przenieś, bo czekasz na kogoś/coś. Niech nie zaśmieca listy aktywnych.
- **Still active** — "wiem o tym, pracuję nad tym". Ale uwaga: możesz kliknąć to tylko 3 razy. Potem musisz podjąć decyzję.

Przykład: Masz Case "Refactor settings page". Ostatnia edycja była 2 tygodnie temu. Board ci go pokazuje. Klikasz "Still active" bo naprawdę chcesz do tego wrócić. Za tydzień Board pyta znowu. Klikasz "Still active" drugi raz. Za kolejny tydzień — trzeci raz. Czwartego razu nie ma. Board mówi: "ok, teraz musisz zdecydować — robisz to, czekasz na coś, czy to już done?"

Dlaczego nie blokada? Bo hard blocki przy ADHD działają gorzej niż przypomnienia. Zablokujesz kogoś i zamiast działać, będzie unikał apki. Lepiej delikatnie przypomnieć i dać wyjście.

Case'y które są w dzisiejszym focusie nie pojawiają się jako stale — sensowne, bo nad nimi właśnie pracujesz.

### 3. Stats + Linki

Na samym dole Boardu masz jeden wiersz z trzema liczbami i dwoma linkami:

```
4 active  ·  3 waiting  ·  2 closed this week

[See all active →]    [See waiting →]
```

To jest pogląd sytuacji. Widzisz ile masz na talerzu bez wchodzenia w detale. Klikasz "See all active" i jedziesz do pełnej listy aktywnych case'ów. Klikasz "See waiting" i widzisz co czeka.

Dlaczego nie pełna lista na Boardzie? Bo Board to "co robię dziś", nie "co mam do zrobienia w ogóle". Pełne listy są w osobnych widokach — jak Inbox ma swój własny ekran, tak Active i Waiting mają swoje.

---

## Focus transition prompt

Jest jeszcze jedna rzecz która może się pojawić na Boardzie, ale tylko w konkretnym momencie.

Kiedy zmieniasz główny focus na nowy Case, a stary Case od czasu ustawienia focusa nie był edytowany — Board pyta co z nim:

```
"Fix login bug" hasn't been updated since you focused on it.
[Done]  [Move to waiting]  [Still working]
```

To jest naturalny moment na to pytanie — właśnie zmieniasz priorytet, więc myślisz o tym co było ważne a co jest ważne teraz. Nie intruzja, tylko wykorzystanie momentu.

Dlaczego to działa? Bo normalnie zapominamy zamknąć rzeczy. Kiedy ustawiasz nowy focus, apka łapie moment i pyta. Nie musisz pamiętać o zamknięciu starego — apka ci przypomni.

---

## Czego na Boardzie NIE ma (i dlaczego)

**Pełna lista aktywnych case'ów** — jest w osobnym widoku (`/active/`). Board pokazuje tylko focus + problemy (stale). Jak chcesz przeglądnąć wszystko — klikasz link.

**Pełna lista czekających case'ów** — osobny widok (`/waiting/`). Same tytuły i next steps, bez akcji. Bo z czekającymi rzeczami nie ma co robić poza sprawdzeniem czy coś się ruszyło.

**Inbox** — Inbox ma swój własny ekran. Na Boardzie jest tylko licznik w nawigacji na górze. Nie mieszamy intake'u z pracą.

**Zamknięte case'y** — zliczane w statystykach ("2 closed this week"), ale nie wyświetlane. Zrobione jest zrobione.

---

## Jak używać Boardu na co dzień

**Rano:**
1. Otwierasz casedock
2. Widzisz focus — wiesz na czym jesteś
3. Jeśli Board pyta o stare case'y — szybko decydujesz (5 sekund)
4. Zaczynasz pracę

**W ciągu dnia:**
1. Przeskakujesz między case'ami? Zmieniasz focus. Board pyta co ze starym.
2. Otwierasz Board żeby wrócić do pracy — widzisz co jest na dziś

**Wieczór lub jutro rano:**
1. Zamykasz case'y które skończyłeś
2. Przenosisz do Waiting rzeczy które są zablokowane
3. Ustawiasz nowy focus na jutro

---

## Dla dociekliwych — jak to działa technicznie

- **Stale detection**: Case jest "stale" jeśli jest aktywny i nie był edytowany od 7+ dni (`CASEDOCK_STALE_PERIOD_DAYS`). Sprawdzane na podstawie `updated_at` — ale same potwierdzenia "Still active" nie aktualizują tego pola (używamy `QuerySet.update()` żeby ominąć `auto_now`).
- **Stale exclusion**: Case'y w dzisiejszym focusie nie są pokazywane jako stale.
- **Ack limit**: Max 3 potwierdzenia "Still active" (`CASEDOCK_STALE_ACK_LIMIT`). Potem zostają tylko opcje Done i Waiting.
- **Transition prompt**: Pojawia się tylko gdy zmieniasz main focus i stary Case nie był edytowany po ustawieniu focusa (porównujemy `Case.updated_at` z `FocusAssignment.created_at`).
- **HTMX**: Wszystkie akcje (stale resolution, focus actions) działają bez przeładowania strony — HTMX swapuje cały `#board-page`.
