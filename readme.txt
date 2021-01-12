Dário Matos 89288
Pedro Almeida 89205
Rui Santos 89293


Como executar a aplicação:
--------------------------
1. Criar um repositório na GraphDB com o nome "f1"
2. importar para o repositório o ficheiro "dataset.n3"
3. instalar requirements.txt (run: pip install -r requirements.txt)
4. executar a Webapp (através da interface do pycharm ou terminal: "python manage.py runserver")


-------------------------
Tópicos mais importantes:
-------------------------

* Página Drivers *
------------------
Adicção/remoção de triplos (Fan Rating)
pesquisa SPARQL ASK


* Página Teams *
----------------
Pesquisa de dados SPARQL (pesquisar equipas pelo nome)
Filtragem de dados SPARQL (filtrar equipas pelo número de corridas e vitórias)
Hiperligações de páginas (nome da equipa) da wikipedia com mais dados acerca de uma equipa


* Página Teams Details *
------------------------
RDFa
inferência (SPARQL construct e insert) de pessoas importantes -> fundadores de uma equipa, diretores e engenheiros


* Página Grand Prix *
---------------------
RDFa
Pesquisa de Dados SPARQL (pesquisa da totalidade de Grand Prix e de dados do respetivo circuito), 
relacionando-os também na componente de RDFa.
Relação com as equipas (equipa que mais vitórias num circuito)
Hiperligações de páginas da wikipedia com mais dados acerca de um Grande Prémio 

* Página Media *
----------------
incorporação de dados da DBpedia (https://wiki.dbpedia.org/), em runtime - SPARQLWrapper

Aviso: durante o desenvolvimento do projeto verificámos que a dbpedia alterou o nome da página onde estavam a ser retirados os dados. Se a página Media carregar sem elementos, a causa mais provável será isso mesmo.
