# Requirements description

Backend aplikace v Pythonu (framework dle vlastního uvážení)

Aplikace by měla periodicky stahovat seznam filmů z API (https://gist.githubusercontent.com/nextsux/f6e0327857c88caedd2dab13affb72c1/raw/04441487d90a0a05831835413f5942d58026d321/videos.json)


Tento seznam by si měla lokálně udržovat v DB vlastního výběru z důvodu možného "výpadku dodavatele"

Uživateli by měla poskytnout JEDNODUCHÝ front-end psaný jakoukoliv technologií, může jednoduše renderovat na straně serveru obyčejné HTML, kde uživateli zobrazí "karty" s jednotlivými videi a umožní mezi nimi filtrovat a řadit je.

Přehrávání !NENÍ! potřeba řešit, ale obrázek z iconUri by byl hezký

Nejde o grafickou podobu a jestli budou barvičky ladit - to není úplně práce backendisty, tzn. nikdo neřešíme design. Důležité je, jak se zhostíte práce s parametry, filtrovanim a řazením.