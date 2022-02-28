# templatex

Pequeño servidor RESTful que se encarga de renderizar datos usando una plantilla
de LaTex.

La API tiene dos endpoints:
- `/pdf/<plantilla>`: Retorna el contenido como PDF
- `/tex/<plantilla>`: Retorna el .tex generado sin renderizar

Se mandan los datos con un POST en formato JSON. Por ejemplo, para el ejemplo `templatex/cards.tex`
los datos serían los siguientes:
```json
{
    "background": true, // or false
    "table": [
        {
            "id": "<identificador de la bbdd>",
            "from": "<Nombre de quien envia la petición",
            "comment": "<Comentarios>",
            "name": "<Nombre de para quien va el cuento/poema",
            "number": "<Número de teléfono al que llamar>"
        }
    ]
}
```

> Obviamente, la tabla puede contener varios records.

Solo hay que hacer una petición HTTP `POST` con los datos en formato JSON, y recibiremos el PDF (o no, si algo ha salido mal)

Esta aberración se ha creado sólo para https://github.com/daviddavo/cypxt20

## ¿xq?

Pues porque mi VPS no da como para meter LaTeX, pero mi ordenador personal, sí.

De esta manera puedo ejecutar `esto` en mi PC personal, redirigir el puerto pertinente
y que la página de cypxt genere los latex que quiera sin tener que instalar nada.
