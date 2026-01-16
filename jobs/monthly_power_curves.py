import os
from dotenv import load_dotenv
from utils.training import build_models
from utils.io import save_models
from utils.metadata import save_training_window, save_model_metadata
from utils.training_dataset import build_training_dataset

load_dotenv()

VC_API_KEY = os.environ["VC_API_KEY"]

# your existing logic
combined_dfs, first_date, last_date = build_training_dataset(VC_API_KEY)

models, metadata = build_models(combined_dfs, degree=3)

save_models(models)
save_model_metadata(metadata)
save_training_window(first_date, last_date)
