import os
import json
import torch
from torch.utils.data import DataLoader
from config import Config
from utils.dataset import PlantVillageDataset
from utils.transforms import get_train_transforms, get_val_test_transforms

def build_file_list(data_dir: str):
    """
    Scans the given data directory and builds lists of file paths, labels, and class names.
    """
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Data directory not found at: {data_dir}")

    # Read class names as names of subfolders
    class_names = sorted([d for d in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, d))])
    class_to_idx = {name: i for i, name in enumerate(class_names)}
    
    file_paths = []
    labels = []

    for class_name in class_names:
        class_path = os.path.join(data_dir, class_name)
        for filename in os.listdir(class_path):
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                file_paths.append(os.path.join(class_path, filename))
                labels.append(class_to_idx[class_name])
                
    return file_paths, labels, class_names

def get_data_loaders(
    data_dir: str,
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
    test_ratio: float = 0.15,
    batch_size: int = None,
    num_workers: int = 0
):
    """
    Generates Train, Validation, and Test PyTorch DataLoaders with automatic index splitting.
    """
    if abs(train_ratio + val_ratio + test_ratio - 1.0) > 1e-5:
        raise ValueError("Train, validation, and test ratios must sum up to 1.0")

    file_paths, labels, class_names = build_file_list(data_dir)
    total_samples = len(file_paths)
    
    if total_samples == 0:
        raise ValueError(f"No image files found in dataset path: {data_dir}")

    # Shuffle paths using PyTorch generator for reproducibility
    indices = torch.randperm(total_samples).tolist()
    
    train_end = int(train_ratio * total_samples)
    val_end = train_end + int(val_ratio * total_samples)

    train_indices = indices[:train_end]
    val_indices = indices[train_end:val_end]
    test_indices = indices[val_end:]

    # Map file paths and labels
    train_files = [file_paths[i] for i in train_indices]
    train_labels = [labels[i] for i in train_indices]

    val_files = [file_paths[i] for i in val_indices]
    val_labels = [labels[i] for i in val_indices]

    test_files = [file_paths[i] for i in test_indices]
    test_labels = [labels[i] for i in test_indices]

    # Instantiate datasets with separate train vs eval transforms
    train_dataset = PlantVillageDataset(train_files, train_labels, transform=get_train_transforms())
    val_dataset = PlantVillageDataset(val_files, val_labels, transform=get_val_test_transforms())
    test_dataset = PlantVillageDataset(test_files, test_labels, transform=get_val_test_transforms())

    bs = batch_size or Config.BATCH_SIZE

    # Create loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=bs,
        shuffle=True,
        num_workers=num_workers,
        pin_memory=True
    )
    val_loader = DataLoader(
        val_dataset,
        batch_size=bs,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )
    test_loader = DataLoader(
        test_dataset,
        batch_size=bs,
        shuffle=False,
        num_workers=num_workers,
        pin_memory=True
    )

    return train_loader, val_loader, test_loader, class_names
