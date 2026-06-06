import torchvision.transforms as transforms
from config import Config

def get_train_transforms():
    """
    Returns data augmentation transforms for the training set:
    - Resize to 224x224
    - Random horizontal flip
    - Random rotation (up to 30 degrees)
    - Color jitter (brightness, contrast, saturation)
    - Normalization with ImageNet constants
    """
    return transforms.Compose([
        transforms.Resize(Config.IMAGE_SIZE),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.RandomRotation(degrees=30),
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2),
        transforms.ToTensor(),
        # Standard ImageNet mean & std for transfer learning with ResNet-50
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

def get_val_test_transforms():
    """
    Returns evaluation transforms for validation/testing:
    - Resize to 224x224
    - Normalization with ImageNet constants
    """
    return transforms.Compose([
        transforms.Resize(Config.IMAGE_SIZE),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
