# Graficas-SR4

INSTRUCCIONES PARA EL PROGRAMA
Parra correr el programa utiliza python3, el progrma principal es SR4 y no recibe ningun argumento.

INSTRUCCIONES PARA EL RENDERIZADO
Para renderizar un objeto y su zbuffer el programa utiliza la funcion de bmp_make: glObjReader. Esta recibe cuatro parametros: el nombre del objeto a renderizar (sin su extension), una escala y dos translate (el primero para x y el segundo para y). La escala es escencial para poder renderizar el objeto ya que permite que el objeto este en una escala de -1 a 1 (la cual se utiliza en bmp_maker), por lo que se debe de utilizar una escala lo suficientemente grande para que todos los vertices se encuentren dentro del rango de -1 a 1. Luego los translates son utilizados para posicionar correctamente el objeto en la imagen.

El zbuffer es procesado dentro de la misma funcion, permitiendo que unicamente se pinte en los lugares correctos. Sin embargo, la variable de zbuffer es inicializada en conjunto con el header permitiendo asi que se puedan renderizar mas objetos dentro de la escena sin ningun problema.

P.D El objeto utilizado como ejemplo ('deer.obj') no es mio.
