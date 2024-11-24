#!/bin/bash
from_path=/datahub/public_datasets/amazon_food_review_system
to_path=/codehub/apps/amazon-food-review-system

python -m src.dataset_preparation --from_path $from_path --to_path $to_path --save_json 