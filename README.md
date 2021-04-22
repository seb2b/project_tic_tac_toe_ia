# Projet Tic Tac Toe IA

### Groupe 1

- ALLIOT Sébastien
- BOUCOUM Idy

### Description du repository

- `main.py` : Script pour jouer au Tic Tac Toe face à une IA (Näive, Minimax ou Minimax Alpha Beta)
- `dist/main/main` : Exécutable du script python `main.py` généré à l'aide du package [PyInstaller](http://www.pyinstaller.org/)
- `simulation.py` : Script pour lancer des simulations de `n` parties entre deux IA (board 3x3)

### Résultats des simulations

Chaque simulation de rencontre a été jouée sur 1000 parties d'un board 3x3.

Joueur 1      | Joueur 2      | V / N / D       | Probabilités       | Temps d'exécution
:-----------: | :-----------: | :-------------: | :----------------: | :----------------:
IA Naïve      | IA Naïve      | 567 / 129 / 304 | 0.56 / 0.12 / 0.30 | 00h 00m 01s
IA Naïve      | IA MiniMax    | 0 / 212 / 788   | 0 / 0.21 / 0.78    | 00h 19m 29s
IA Naïve      | IA MiniMax AB | 0 / 184 / 816   | 0 / 0.18 / 0.81    | 00h 01m 07s
IA MiniMax    | IA Näive      | 995 / 5 / 0     | 0.99 / 0.005 / 0   | 01h 15m 27s
IA MiniMax AB | IA Näive      | 996 / 4 / 0     | 0.99 / 0.004 / 0   | 00h 07m 43s
IA MiniMax    | IA MiniMax AB | 0 / 1000 / 0    | 0 / 1 / 0          | 02h 21m 12s
IA MiniMax AB | IA MiniMax    | 0 / 1000 / 0    | 0 / 1 / 0          | 00h 26m 56s

Les cas `IA MiniMax VS IA Minimax` et `IA MiniMax AB VS IA Minimax AB` n'ont pas été testé car non pertinent (égalité logique dans chaque cas).