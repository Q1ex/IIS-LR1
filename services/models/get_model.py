import shutil
import os

# Настройки
RUN_ID = "9ccf6e5a74574f1aad71e76d7b5d0201"  
SOURCE_BASE_DIR = r"D:\уник\мага\3сем\МОХ\IIS-LR1\research\mlruns\1"
DEST_MODEL_DIR = r"D:\уник\мага\3сем\МОХ\IIS-LR1\services\models"
DEST_MODEL_PATH = os.path.join(DEST_MODEL_DIR, "model.pkl")

# Путь к исходной модели 
source_model_path = os.path.join(SOURCE_BASE_DIR, RUN_ID, "artifacts", "model", "model.pkl")

# Создать директорию назначения, если не существует
os.makedirs(DEST_MODEL_DIR, exist_ok=True)


shutil.copy2(source_model_path, DEST_MODEL_PATH)

print(f"Model with run_id={RUN_ID} copied to {DEST_MODEL_PATH}")