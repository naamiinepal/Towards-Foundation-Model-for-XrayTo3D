"""Generate evaluation script."""
import sys

import wandb

from XrayTo3DShape import MODEL_NAMES, filter_wandb_run, get_run_from_model_name

ANATOMY = "femur"
tags = ["dropout", "model-compare"]
wandb.login()
runs = filter_wandb_run(anatomy=ANATOMY, tags=tags, verbose=False)
if len(runs) == 0:
    print(f"found {len(runs)} wandb runs for anatomy {ANATOMY}. exiting ...")
    sys.exit()
for model_name in MODEL_NAMES:
    run = get_run_from_model_name(model_name, runs)

    command_csv_generate = f"python external/xrayto3D-morphometry/femur_morphometry_v2.py --dir runs/2d-3d-benchmark/{run.id}/evaluation --log_filename femur_morphometry.csv"
    command_csv_processing = f"python external/xrayto3D-morphometry/scripts/process_femur_csv.py runs/2d-3d-benchmark/{run.id}/evaluation/femur_morphometry.csv"

    print(f"# model type: {model_name} tags {tags}")
    print(command_csv_generate)
    print(command_csv_processing)
