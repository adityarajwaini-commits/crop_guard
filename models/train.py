import os
import time
import logging
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torchvision.models as models
from torchvision.models import ResNet50_Weights
from config import Config
from utils.data_loaders import get_data_loaders

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(os.path.join(Config.BASE_DIR, "training.log"), mode='a')
    ]
)

from models.utils import EarlyStopping

def build_model(num_classes: int, freeze_backbone: bool = True) -> nn.Module:
    """
    Loads pretrained ResNet-50, replaces the classification layer,
    and freezes the backbone layers if specified.
    """
    logging.info(f"Loading pretrained ResNet-50 backbone...")
    weights = ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)

    if freeze_backbone:
        logging.info("Freezing ResNet-50 backbone layers...")
        for param in model.parameters():
            param.requires_grad = False
            
    # Replace the classification layer (fc)
    # ResNet-50 out features size is 2048
    in_features = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Linear(in_features, 512),
        nn.ReLU(),
        nn.Dropout(0.3),
        nn.Linear(512, num_classes)
    )
    logging.info(f"Replaced classifier head with custom classification head for {num_classes} classes.")
    return model

def unfreeze_for_finetuning(model: nn.Module):
    """
    Unfreezes the entire model parameters to support full fine-tuning.
    """
    logging.info("Unfreezing all ResNet-50 backbone layers for fine-tuning...")
    for param in model.parameters():
        param.requires_grad = True

def train_one_epoch(model, loader, criterion, optimizer, device):
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0

    for idx, (images, labels) in enumerate(loader):
        images, labels = images.to(device), labels.to(device)

        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        running_loss += loss.item() * images.size(0)
        _, preds = torch.max(outputs, 1)
        correct += torch.sum(preds == labels.data).item()
        total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def evaluate(model, loader, criterion, device):
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def save_checkpoint(model, optimizer, epoch, val_loss, class_names, filename="best_checkpoint.pth"):
    os.makedirs(Config.SAVED_MODELS_DIR, exist_ok=True)
    save_path = os.path.join(Config.SAVED_MODELS_DIR, filename)
    state = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_loss': val_loss,
        'class_names': class_names
    }
    torch.save(state, save_path)
    logging.info(f"Checkpoint successfully saved to: {save_path}")

def run_training_pipeline(data_dir: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device for training: {device}")

    # Load dataset loaders
    try:
        train_loader, val_loader, test_loader, class_names = get_data_loaders(data_dir)
        num_classes = len(class_names)
        logging.info(f"Loaded {num_classes} classes: {class_names}")
    except Exception as e:
        logging.error(f"Failed to load dataset: {e}")
        return

    # Build model (Backbone initially frozen)
    model = build_model(num_classes=num_classes, freeze_backbone=True)
    model = model.to(device)

    criterion = nn.CrossEntropyLoss()
    # Optimize classifier head parameters only
    optimizer = optim.Adam(model.fc.parameters(), lr=Config.LEARNING_RATE)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.1)
    early_stopping = EarlyStopping(patience=5)

    best_val_loss = float('inf')

    # Phase 1: Classifier Head Training
    logging.info(f"--- Starting Phase 1: Training Classifier Head ({Config.EPOCHS} epochs) ---")
    for epoch in range(1, Config.EPOCHS + 1):
        start_time = time.time()
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        epoch_time = time.time() - start_time

        scheduler.step(val_loss)
        
        logging.info(
            f"Epoch {epoch}/{Config.EPOCHS} ({epoch_time:.1f}s) | "
            f"Train Loss: {train_loss:.4f} - Train Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} - Val Acc: {val_acc*100:.2f}%"
        )

        # Check and save best head model checkpoint
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(model, optimizer, epoch, val_loss, class_names, "best_head_model.pth")

        if early_stopping(val_loss):
            logging.info("Early stopping triggered in Phase 1.")
            break

    # Phase 2: Full Fine-tuning (Optional check or low learning rate execution)
    logging.info("--- Starting Phase 2: Fine-tuning entire network ---")
    # Unfreeze the model
    unfreeze_for_finetuning(model)
    
    # Run with a much smaller learning rate to preserve features
    finetune_lr = Config.LEARNING_RATE * 0.01
    optimizer = optim.Adam(model.parameters(), lr=finetune_lr)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.1)
    early_stopping = EarlyStopping(patience=5)
    
    # Run fine-tuning epochs
    finetune_epochs = max(5, Config.EPOCHS // 2)
    for epoch in range(1, finetune_epochs + 1):
        start_time = time.time()
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc = evaluate(model, val_loader, criterion, device)
        epoch_time = time.time() - start_time

        scheduler.step(val_loss)

        logging.info(
            f"Finetune Epoch {epoch}/{finetune_epochs} ({epoch_time:.1f}s) | "
            f"Train Loss: {train_loss:.4f} - Train Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} - Val Acc: {val_acc*100:.2f}%"
        )

        # Save checkpoint if it outperforms overall best
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(model, optimizer, epoch, val_loss, class_names, "best_model.pth")

        if early_stopping(val_loss):
            logging.info("Early stopping triggered in Phase 2.")
            break

    logging.info("Training pipeline execution completed.")

if __name__ == "__main__":
    # Standard entry point assuming dataset exists in data/raw folder
    run_training_pipeline(Config.DATA_DIR)
