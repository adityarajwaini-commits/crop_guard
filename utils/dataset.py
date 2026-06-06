import os
from PIL import Image
from torch.utils.data import Dataset

class PlantVillageDataset(Dataset):
    """
    Custom PyTorch Dataset for loading leaf images from the PlantVillage dataset structure.
    Expected folder structure:
    data_dir/
        class_name_A/
            image1.jpg
        class_name_B/
            image2.jpg
    """
    def __init__(self, file_paths, labels, transform=None):
        """
        Args:
            file_paths (list): List of absolute paths to the images.
            labels (list): List of class integer labels matching file_paths.
            transform (callable, optional): PyTorch transform sequence.
        """
        self.file_paths = file_paths
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.file_paths)

    def __getitem__(self, idx):
        # Load image in RGB mode
        img_path = self.file_paths[idx]
        image = Image.open(img_path).convert("RGB")
        label = self.labels[idx]

        if self.transform:
            image = self.transform(image)

        return image, label
