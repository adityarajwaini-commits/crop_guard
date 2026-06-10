"""
Standalone training script optimized for GPU environments (Colab, Lambda Labs, etc.)
Can be run: python train_full_pipeline.py --data_dir /path/to/data
"""
import os
import sys
import argparse
import logging
import json
import time
from datetime import datetime
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torchvision.models as models
from torchvision.models import ResNet50_Weights
import numpy as np
from sklearn.metrics import accuracy_score, precision_recall_fscore_support

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

def build_model(num_classes: int, freeze_backbone: bool = True) -> nn.Module:
    """Builds ResNet-50 model with custom classification head."""
    logging.info(f"Loading pretrained ResNet-50 backbone...")
    weights = ResNet50_Weights.DEFAULT
    model = models.resnet50(weights=weights)

    if freeze_backbone:
        logging.info("Freezing ResNet-50 backbone layers...")
        for param in model.parameters():
            param.requires_grad = False
            
    # Replace classification layer
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
    """Unfreezes all model parameters for fine-tuning."""
    logging.info("Unfreezing all ResNet-50 backbone layers for fine-tuning...")
    for param in model.parameters():
        param.requires_grad = True

def train_one_epoch(model, loader, criterion, optimizer, device):
    """Trains model for one epoch."""
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
        
        if (idx + 1) % 50 == 0:
            logging.info(f"Batch {idx+1}/{len(loader)} - Loss: {loss.item():.4f}")

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc

def evaluate(model, loader, criterion, device):
    """Evaluates model on a dataset."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    all_preds = []
    all_labels = []

    with torch.no_grad():
        for images, labels in loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            loss = criterion(outputs, labels)

            running_loss += loss.item() * images.size(0)
            _, preds = torch.max(outputs, 1)
            correct += torch.sum(preds == labels.data).item()
            total += labels.size(0)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.cpu().numpy())

    epoch_loss = running_loss / total
    epoch_acc = correct / total
    return epoch_loss, epoch_acc, np.array(all_preds), np.array(all_labels)

def save_checkpoint(model, optimizer, epoch, val_loss, class_names, save_dir, filename="best_checkpoint.pth"):
    """Saves model checkpoint."""
    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, filename)
    state = {
        'epoch': epoch,
        'model_state_dict': model.state_dict(),
        'optimizer_state_dict': optimizer.state_dict(),
        'val_loss': val_loss,
        'class_names': class_names
    }
    torch.save(state, save_path)
    logging.info(f"Checkpoint saved to: {save_path}")

def save_training_report(history, class_names, save_dir):
    """Saves training history and metadata."""
    report = {
        'training_history': history,
        'num_classes': len(class_names),
        'class_names': class_names,
        'timestamp': datetime.now().isoformat()
    }
    
    report_path = os.path.join(save_dir, "training_report.json")
    with open(report_path, 'w') as f:
        json.dump(report, f, indent=2)
    logging.info(f"Training report saved to: {report_path}")

def train_pipeline(data_dir: str, save_dir: str, epochs: int = 20, batch_size: int = 32, 
                   learning_rate: float = 0.001, val_ratio: float = 0.15, test_ratio: float = 0.15,
                   resume_checkpoint: str = None):
    """Complete training pipeline."""
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Using device: {device}")
    logging.info(f"CUDA available: {torch.cuda.is_available()}")
    
    # Check dataset
    if not os.path.exists(data_dir):
        raise FileNotFoundError(f"Dataset directory not found: {data_dir}")
    
    # Import data loaders (requires config.py and utils modules)
    try:
        from utils.data_loaders import get_data_loaders
        from config import Config
    except ImportError as e:
        logging.error(f"Could not import required modules. Make sure you're running from project root: {e}")
        raise
    
    # Get data loaders
    train_loader, val_loader, test_loader, class_names = get_data_loaders(
        data_dir,
        train_ratio=1.0 - val_ratio - test_ratio,
        val_ratio=val_ratio,
        test_ratio=test_ratio,
        batch_size=batch_size,
        num_workers=4 if torch.cuda.is_available() else 0
    )
    
    num_classes = len(class_names)
    logging.info(f"Dataset loaded: {num_classes} classes")
    logging.info(f"Classes: {class_names}")
    logging.info(f"Train batches: {len(train_loader)}, Val batches: {len(val_loader)}, Test batches: {len(test_loader)}")
    
    # Build model
    model = build_model(num_classes=num_classes, freeze_backbone=True)
    model = model.to(device)
    
    criterion = nn.CrossEntropyLoss()
    
    # Phase 1: Train head only
    logging.info("="*60)
    logging.info("PHASE 1: Training Classification Head")
    logging.info("="*60)
    
    optimizer = optim.Adam(model.fc.parameters(), lr=learning_rate)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.1)
    
    best_val_loss = float('inf')
    history = {'phase1': [], 'phase2': []}
    
    from models.utils import EarlyStopping
    early_stopping = EarlyStopping(patience=5)
    
    for epoch in range(1, epochs + 1):
        start_time = time.time()
        
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc, _, _ = evaluate(model, val_loader, criterion, device)
        
        epoch_time = time.time() - start_time
        scheduler.step(val_loss)
        
        logging.info(
            f"Epoch {epoch}/{epochs} ({epoch_time:.1f}s) | "
            f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}%"
        )
        
        history['phase1'].append({
            'epoch': epoch,
            'train_loss': float(train_loss),
            'train_acc': float(train_acc),
            'val_loss': float(val_loss),
            'val_acc': float(val_acc)
        })

        # Save checkpoint after every epoch (head training)
        save_checkpoint(model, optimizer, epoch, val_loss, class_names, save_dir, f"head_epoch_{epoch}.pth")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(model, optimizer, epoch, val_loss, class_names, save_dir, "best_head_model.pth")

        if early_stopping(val_loss):
            logging.info("Early stopping triggered in Phase 1")
            break
    
    # Phase 2: Fine-tune full model
    logging.info("="*60)
    logging.info("PHASE 2: Fine-tuning Entire Network")
    logging.info("="*60)
    
    # If a resume checkpoint is provided, try to load model weights (useful to resume from head-only checkpoint)
    if resume_checkpoint:
        try:
            logging.info(f"Loading resume checkpoint: {resume_checkpoint}")
            ck = torch.load(resume_checkpoint, map_location=device)
            model.load_state_dict(ck['model_state_dict'])
            # update best_val_loss if present
            if 'val_loss' in ck:
                best_val_loss = ck.get('val_loss', best_val_loss)
        except Exception as e:
            logging.warning(f"Failed to load resume checkpoint: {e}")

    unfreeze_for_finetuning(model)
    finetune_lr = learning_rate * 0.01
    optimizer = optim.Adam(model.parameters(), lr=finetune_lr)
    scheduler = ReduceLROnPlateau(optimizer, mode='min', patience=2, factor=0.1)
    early_stopping = EarlyStopping(patience=5)
    
    finetune_epochs = max(5, epochs // 2)
    
    for epoch in range(1, finetune_epochs + 1):
        start_time = time.time()
        
        train_loss, train_acc = train_one_epoch(model, train_loader, criterion, optimizer, device)
        val_loss, val_acc, _, _ = evaluate(model, val_loader, criterion, device)
        
        epoch_time = time.time() - start_time
        scheduler.step(val_loss)
        
        logging.info(
            f"Finetune Epoch {epoch}/{finetune_epochs} ({epoch_time:.1f}s) | "
            f"Train Loss: {train_loss:.4f} Acc: {train_acc*100:.2f}% | "
            f"Val Loss: {val_loss:.4f} Acc: {val_acc*100:.2f}%"
        )
        
        history['phase2'].append({
            'epoch': epoch,
            'train_loss': float(train_loss),
            'train_acc': float(train_acc),
            'val_loss': float(val_loss),
            'val_acc': float(val_acc)
        })

        # Save checkpoint after every finetune epoch
        save_checkpoint(model, optimizer, epoch, val_loss, class_names, save_dir, f"finetune_epoch_{epoch}.pth")

        if val_loss < best_val_loss:
            best_val_loss = val_loss
            save_checkpoint(model, optimizer, epoch, val_loss, class_names, save_dir, "best_model.pth")

        if early_stopping(val_loss):
            logging.info("Early stopping triggered in Phase 2")
            break

        # Report GPU memory usage for this epoch
        if torch.cuda.is_available():
            try:
                allocated = torch.cuda.memory_allocated(device)
                reserved = torch.cuda.memory_reserved(device)
                peak = torch.cuda.max_memory_allocated(device)
                logging.info(f"GPU Memory - Allocated: {allocated/1024**2:.1f} MB, Reserved: {reserved/1024**2:.1f} MB, Peak: {peak/1024**2:.1f} MB")
                torch.cuda.reset_peak_memory_stats(device)
            except Exception as e:
                logging.debug(f"Could not query GPU memory: {e}")
    
    # Save training report
    save_training_report(history, class_names, save_dir)
    
    # Evaluate on test set
    logging.info("="*60)
    logging.info("FINAL EVALUATION ON TEST SET")
    logging.info("="*60)
    
    # Load best model
    best_model_path = os.path.join(save_dir, "best_model.pth")
    checkpoint = torch.load(best_model_path, map_location=device)
    model.load_state_dict(checkpoint['model_state_dict'])
    
    test_loss, test_acc, test_preds, test_labels = evaluate(model, test_loader, criterion, device)
    precision, recall, f1, _ = precision_recall_fscore_support(test_labels, test_preds, average='macro')
    
    logging.info(f"Test Loss: {test_loss:.4f}")
    logging.info(f"Test Accuracy:  {test_acc*100:.2f}%")
    logging.info(f"Test Precision: {precision*100:.2f}%")
    logging.info(f"Test Recall:    {recall*100:.2f}%")
    logging.info(f"Test F1 Score:  {f1*100:.2f}%")
    
    logging.info("="*60)
    logging.info("Training completed successfully!")
    logging.info(f"Best model saved to: {best_model_path}")
    logging.info("="*60)
    
    return model, history

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train CropGuard ResNet-50 model")
    parser.add_argument("--data_dir", type=str, default="data",
                        help="Path to dataset directory (default: data)")
    parser.add_argument("--save_dir", type=str, default="saved_models",
                        help="Directory to save checkpoints (default: saved_models)")
    parser.add_argument("--epochs", type=int, default=20,
                        help="Number of training epochs (default: 20)")
    parser.add_argument("--batch_size", type=int, default=32,
                        help="Batch size (default: 32)")
    parser.add_argument("--learning_rate", type=float, default=0.001,
                        help="Learning rate (default: 0.001)")
    parser.add_argument("--resume_checkpoint", type=str, default=None,
                        help="Path to checkpoint to resume weights from (optional)")
    
    args = parser.parse_args()
    
    try:
        train_pipeline(
            data_dir=args.data_dir,
            save_dir=args.save_dir,
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate
            ,resume_checkpoint=args.resume_checkpoint
        )
    except Exception as e:
        logging.error(f"Training failed: {e}")
        sys.exit(1)
