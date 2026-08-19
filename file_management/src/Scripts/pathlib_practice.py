from pathlib import Path

# Crear objetos ruta a partir de cadenas
file_path_str = "data/union_data.csv"

data_path = Path(file_path_str)

# Crear objetos trayectoria a partir de otro objetos
base_path = Path("/home/user")
data_dir = Path("data")

# Combining multiple paths
file_path = base_path / data_dir / "prices.csv"
print(file_path)

# Crear objetos de ruta desde el directorio de trabajo actual
cwd = Path.cwd()
print(cwd)

# Crear objetos de ruta desde el directorio de trabajo inicial
home = Path.home()

home / "downloads" / "projects"


image_file = home / "downloads" / "midjourney.png"

# nombre del archivo
image_file.name

# Directorio principal
image_file.parent

# Sufijo
image_file.suffix

# Listado de directorios
cwd = Path.cwd()
for entry in cwd.iterdir():  # <-
    print(entry)

# Es directorio
for entry in cwd.iterdir():
    if entry.is_dir():
        print(entry.name)

# Es archivo
for entry in cwd.iterdir():
    if entry.is_file():
        print(entry.suffix)

# Existe la ruta?
image_file.exists()


# Crear directiorios
data_dir = Path("new_data_dir")
data_dir.mkdir()

# Crear directorio junto con directorios padre
sub_dir = Path("data/nested/subdirectory")
sub_dir.mkdir(parents=True)

# Borrar archivo
to_delete = Path("data/prices.csv")

if to_delete.exists():
    to_delete.unlink()
    print(f"Successfully deleted {to_delete.name}")

# Borrar directorios *vacíos*
empty_dir = Path("new_data_dir")

empty_dir.rmdir()

# Obtener ruta absoluta de una relativa
relative_image = Path("images/midjourney.png")

absolute_image = relative_image.resolve()

# Obtener ruta relativa de absoluta
relative_path = Path.cwd()

absolute_image.relative_to(relative_path)

# búsqueda glob
articles_dir = Path.home() / "articles"
# Find all scripts
notebooks = articles_dir.glob("*.ipynb")
# Print how many found
print(len(list(notebooks)))

# Búsqueda glob recursiva
notebooks = articles_dir.rglob("*.ipynb")  # <-

# Mover archivos
# Define the file to be moved
source_file = Path("new_file.txt")

# Define the location to put the file
destination = Path("data/new/location")

# Create the directories if they don't exist
destination.mkdir(parents=True)

# Move the file
source_file.replace(destination / source_file.name)

# Crear archivos con touch
new_dataset = Path("data/new.csv")
if not new_dataset.exists():
    new_dataset.touch()

# acceder a información de los archivos
original_image = Path("midjourney.png")
image_stats = original_image.stat()  # <-

image_stats

# Obtener la ruta del archivo abierto
current_route = Path(__file__).parent
