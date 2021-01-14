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

	PREFIX dbp: <http://dbpedia.org/property/>
	PREFIX dct: <http://purl.org/dc/terms/>
	PREFIX dbc: <http://dbpedia.org/resource/Category:>
	CONSTRUCT {
	?team <http://dbpedia.org/property/importantFigure> ?name
	}
	WHERE {
	{
		?team dct:subject dbc:Formula_One_constructors .
	    ?team dbp:principal ?name .
	}
	UNION
	{
		?team dct:subject dbc:Formula_One_constructors .
	    ?team dbp:founders ?name .
	}
	union
	{ 
	    ?team dct:subject dbc:Formula_One_constructors .
	    ?team dbp:engineeringHead ?name .
	}
	}
substituir "construct" por "insert" para inserir novos triplos


* Página Grand Prix *
---------------------
RDFa: fotos dos grafos na pasta readme. 
      Foto rdfa-gp  -> informação sobre um Grand Prix (copiar da linha 1115 - 1150, por exemplo)
      Foto rdfa-gps -> informação sobre todos os Grand Prix (copiar da linha 68 - 1152)
      

Pesquisa de Dados SPARQL (pesquisa da totalidade de Grand Prix e de dados do respetivo circuito), 
relacionando-os também na componente de RDFa.
Relação com as equipas (equipa que mais vitórias num circuito)
Hiperligações de páginas da wikipedia com mais dados acerca de um Grande Prémio 


* Página Media *
----------------
RDFa
incorporação de dados da DBpedia (https://wiki.dbpedia.org/), em runtime - SPARQLWrapper

Aviso: durante o desenvolvimento do projeto verificámos que a dbpedia alterou o nome da página onde estavam a ser retirados os dados. Se a página Media carregar sem elementos, a causa mais provável será isso mesmo.
