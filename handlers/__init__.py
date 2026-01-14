from pathlib import Path
from importlib import import_module

routers = []

# Путь к текущей директории
current_dir = Path(__file__).parent

# Используем rglob для рекурсивного поиска всех .py файлов
for file in current_dir.rglob("*.py"):
    # Пропускаем __init__.py и другие системные файлы
    if file.name == "__init__.py" or file.name.startswith("__"):
        continue

    # Получаем относительный путь для импорта
    relative_path = file.relative_to(current_dir)
    # Преобразуем путь в формат модуля (заменяем / на . и убираем .py)
    module_path = str(relative_path).replace('/', '.').replace('\\', '.')[:-3]
    module_name = f"{__package__}.{module_path}"

    try:
        module = import_module(module_name)
        if hasattr(module, "router"):
            routers.append(module.router)
    except ImportError as e:
        print(f"Ошибка импорта модуля {module_name}: {e}")