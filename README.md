<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Go" />

  &#xa0;

  <!-- <a href="https://go.netlify.app">Demo</a> -->
</div>

<h1 align="center">Go</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/PeopleCreateBestCode/go?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/PeopleCreateBestCode/go?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/PeopleCreateBestCode/go?color=56BEB8">

  <!-- <img alt="License" src="https://img.shields.io/github/license/PeopleCreateBestCode/go?color=56BEB8"> -->

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/PeopleCreateBestCode/go?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/PeopleCreateBestCode/go?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/PeopleCreateBestCode/go?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Go 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-features">Features</a> &#xa0; | &#xa0;
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-instalacja">Instalacja</a>
</p>

<br>

## :dart: About

Gra go to jest fajna gra. Projekt zrobiony na lekcje informatyki. Używa pygame community edition do wyświetlania gry graficznie.

## :sparkles: Features

:heavy_check_mark: Pięknie graficznie wyświetla stan gry\
:heavy_check_mark: Na bieżąco liczy punkty\
:heavy_check_mark: Masha mode

## :rocket: Technologies

To zostało użyte do stworzenia tego projektu:

- [Python](https://www.python.org/)
- [Pygame CE](https://pypi.org/project/pygame-ce/)
- [GIF pygame](https://pypi.org/project/gif-pygame/)

## :white_check_mark: Instalacja

Pobierz gotowy plik z zakładki [releases](https://github.com/PeopleCreateBestCode/Go/releases) lub skorzystaj z poradnika poniżej:
\
Przed rozpoczęciem musisz mieć [Git](https://git-scm.com) i [Python](https://www.python.org/) zainsalowane na komputerze. (i opcjonalnie moduł [Nuitka](https://nuitka.net/) jeśli kompilujesz)

## :checkered_flag: 7

```bash
# Poniższa komenda klonuje repozytorium
$ git clone https://github.com/PeopleCreateBestCode/go.git

# Przejdź do poprawnego folderu
$ cd Go

# stwórz środowisko wirtualne
$ python -m venv .venv

# aktywacja - wybierz opcję dla swojego systemu operacyjnego
$ ./.venv/Scripts/Activate.ps1  # Windows
$ source .venv/bin/activate  # Linux

# Zainsaluj wszystkie zależności
$ pip install -r requirements.txt

# Start
$ python main.py

### Ewentualnie możesz kompilować projekt do jednego pliku exe za pomocą modułu Nuitka

# zainstaluj najnowszą wersję modułu
$ pip install --upgrade nuitka

# kompiluj
$ python -m nuitka --mode=onefile --windows-console-mode=disable --include-data-dir=assets=assets --output-filename=Go.exe main.py

```


Made with :heart: by <a href="https://github.com/PeopleCreateBestCode" target="_blank">PeopleCreateBestCode organization</a>

&#xa0;

<a href="#top">Back to top</a>
