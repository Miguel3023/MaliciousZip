# MaliciousZip
Este Script de Python contiene los bytes de la estrutura de un archivo con extensión ".zip". Se le hace creer al servidor que se está subiendo un archivo ".zip" que contiene un ".pdf" comprimido, lo que realmente sucede es que subimos un archivo ".php" gracias a que añadimos un null byte a la hora de definir la extensión del ".pdf", que contiene un ejecución a nivel de sistema Unix/Linux para entablarte una reverse shell a través del puerto 4646.

# Cómo ejecutarlo?

Al ejecutarlo te preguntará por tu IP y la de la víctima, paralelamente tienes que estar en escucha a través del puerto 4646 con Netcat para recibir la conexión y entablarte exitosamente la reverse shell.
