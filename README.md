<<<<<<< HEAD
# Stock-prices
Mini Gestor de Precios de Acciones

Vas a crear un pequeño proyecto en Python que gestione precios de acciones usando Yahoo
Finance como fuente de datos. El objetivo es aprender a: - Configurar un proyecto profesional con
Git y Poetry. - Usar APIs externas para traer datos financieros. - Guardar y consultar información
en una base de datos SQLite. - Evitar descargas innecesarias guardando datos localmente.

Pasos a Seguir

1. Preparar el entorno del proyecto
Crea un nuevo repositorio en tu cuenta de GitHub llamado stock-prices. 2. Clona el repositorio
en tu computadora. 3. Inicializa el proyecto con Poetry: poetry init - Define el nombre del
proyecto: stock-prices. - Añade una breve descripción. - Configura el autor con tu nombre. - Acepta
el resto con defaults. 4. Instala las dependencias necesarias: poetry add yfinance
sqlalchemy sqlite-utils matplotlib

2. Crear el script principal
Dentro del proyecto, crea un archivo main.py que haga lo siguiente: 1. Permita al usuario ingresar
un ticker (ej: AAPL, MSFT). 2. Revise si los precios ya están guardados en SQLite (stocks.db). 3.
Si existen, muéstralos. 4. Si no existen, descárgalos desde Yahoo Finance, guárdalos y luego
muéstralos.

3. Funcionalidad extra: Visualización
- Implementa una opción para graficar los precios históricos usando matplotlib. - El gráfico debe
mostrar la evolución del precio de cierre (Close) en el tiempo.

4. Ejemplo de uso esperado
$ poetry run python main.py Ingrese ticker: AAPL Datos no encontrados en la base de datos.
Descargando de Yahoo Finance... Datos guardados en stocks.db Mostrando últimos 5 registros:
2025-09-01 229.12 2025-09-02 231.05 2025-09-03 228.45 2025-09-04 232.70 2025-09-05 234.11
¿Desea ver un gráfico? (s/n): s --> Se abre una ventana con el gráfico de precios

5. Entrega
- El repositorio debe contener: 1. pyproject.toml generado por Poetry. 2. main.py con el código del
ejercicio. 3. .gitignore para excluir archivos innecesarios (.venv, __pycache__, *.db). - Sube los
cambios a GitHub y comparte el link del repositorio.


Para Ejecutar

pyenv local 3.12.10

```

2- crear venv con poetry
```bash
poetry shell
```

3-
```bash 

poetry install