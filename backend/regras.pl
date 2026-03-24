:- consult('filmes.pl').

% Filtro de Nota

filtra_nota(_, qualquer).
filtra_nota(Filme, NotaMin) :- 
    number(NotaMin), 
    nota(Filme, N), 
    N >= NotaMin.


% Filtro de Gênero

filtra_genero(_, qualquer).
filtra_genero(Filme, Genero) :- 
    Genero \= qualquer, 
    genero(Filme, Genero).


% Filtro de Duração

filtra_duracao(_, qualquer).
filtra_duracao(Filme, curto) :- 
    duracao(Filme, D), 
    D =< 90.
filtra_duracao(Filme, longo) :- 
    duracao(Filme, D), 
    D > 90.


% Filtro de Ano

filtra_ano(_, qualquer).
filtra_ano(Filme, recente) :- 
    ano(Filme, A), 
    A >= 2016.
filtra_ano(Filme, antigo) :- 
    ano(Filme, A), 
    A < 2016.


% REGRA PRINCIPAL DE RECOMENDAÇÃO
recomendar_filme(Filme, NotaMin, Genero, Duracao, Ano) :-
    filme(Filme),
    filtra_nota(Filme, NotaMin),
    filtra_genero(Filme, Genero),
    filtra_duracao(Filme, Duracao),
    filtra_ano(Filme, Ano).