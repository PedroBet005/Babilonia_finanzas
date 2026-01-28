import json

RUTA_DATOS = "datos.json"   # ajusta si tu archivo se llama distinto

# 🔒 Backup automático
with open(RUTA_DATOS, "r", encoding="utf-8") as f:
    data = json.load(f)

with open("datos_backup.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Backup creado: datos_backup.json")

# 🔄 Migración de categorías
for e in data.get("expenses", []):
    category = e.get("category")

    if isinstance(category, str) and category.startswith("category_"):
        e["category"] = category.replace("category_", "")

# 💾 Guardar cambios
with open(RUTA_DATOS, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("✅ Migración completada correctamente")
