import os
import logging
import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import itertools

from config import Config
from models.train import build_model
from utils.data_loaders import get_data_loaders

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def plot_confusion_matrix(cm, class_names, save_path):
    """
    Plots the confusion matrix and saves it as an image.
    """
    plt.figure(figsize=(10, 8))
    plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Greens)
    plt.title('Confusion Matrix')
    plt.colorbar()
    
    tick_marks = np.arange(len(class_names))
    plt.xticks(tick_marks, class_names, rotation=45, ha="right")
    plt.yticks(tick_marks, class_names)

    # Compute normalization percentages
    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    cm_normalized = np.nan_to_num(cm_normalized) # Replace NaNs with zero if sum is zero

    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        val_raw = cm[i, j]
        val_pct = cm_normalized[i, j] * 100
        text = f"{val_raw}\n({val_pct:.1f}%)"
        
        plt.text(j, i, text,
                 horizontalalignment="center",
                 verticalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True Class label')
    plt.xlabel('Predicted Class label')
    
    # Save the figure
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.close()
    logging.info(f"Confusion Matrix plot saved to: {save_path}")

def run_evaluation(model_path: str):
    # 1. Verify checkpoint existence
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model checkpoint not found at: {model_path}. Train the model first.")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    logging.info(f"Evaluating model using device: {device}")

    # 2. Load the training/test structures and classes
    try:
        _, _, test_loader, class_names = get_data_loaders(Config.DATA_DIR)
    except Exception as e:
        logging.error(f"Failed to load dataset: {e}")
        return

    # 3. Load checkpoint state
    checkpoint = torch.load(model_path, map_location=device)
    num_classes = len(class_names)
    
    # 4. Instantiate model and load state dictionary
    model = build_model(num_classes=num_classes, freeze_backbone=False)
    model.load_state_dict(checkpoint['model_state_dict'])
    model = model.to(device)
    model.eval()

    all_preds = []
    all_labels = []

    # 5. Run inference over test set
    logging.info("Running evaluation predictions on the test set...")
    with torch.no_grad():
        for images, labels in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, preds = torch.max(outputs, 1)
            
            all_preds.extend(preds.cpu().numpy())
            all_labels.extend(labels.numpy())

    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)

    # 6. Calculate performance metrics
    accuracy = accuracy_score(all_labels, all_preds)
    precision, recall, f1, _ = precision_recall_fscore_support(all_labels, all_preds, average='macro')
    
    # Per-class scores
    per_class_precision, per_class_recall, per_class_f1, _ = precision_recall_fscore_support(
        all_labels, all_preds, average=None, labels=range(num_classes)
    )

    cm = confusion_matrix(all_labels, all_preds)

    # 7. Generate text report
    report_lines = []
    report_lines.append("="*50)
    report_lines.append("              CropGuard Evaluation Report")
    report_lines.append("="*50)
    report_lines.append(f"Model Source: {model_path}")
    report_lines.append(f"Accuracy:     {accuracy*100:.2f}%")
    report_lines.append(f"Precision:    {precision*100:.2f}% (Macro)")
    report_lines.append(f"Recall:       {recall*100:.2f}% (Macro)")
    report_lines.append(f"F1-Score:     {f1*100:.2f}% (Macro)")
    report_lines.append("\n" + "-"*50)
    report_lines.append("                 Per-Class Metrics")
    report_lines.append("-"*50)
    
    for i, class_name in enumerate(class_names):
        report_lines.append(
            f"Class '{class_name}':\n"
            f"  Precision: {per_class_precision[i]*100:.2f}%\n"
            f"  Recall:    {per_class_recall[i]*100:.2f}%\n"
            f"  F1-Score:  {per_class_f1[i]*100:.2f}%"
        )
        
    report_lines.append("\n" + "="*50)
    report_text = "\n".join(report_lines)

    # Print to console
    print(report_text)

    # Save metrics report file
    report_save_path = os.path.join(Config.SAVED_MODELS_DIR, "evaluation_report.txt")
    with open(report_save_path, 'w') as f:
        f.write(report_text)
    logging.info(f"Evaluation report text saved to: {report_save_path}")

    # Plot and save confusion matrix image
    cm_image_path = os.path.join(Config.SAVED_MODELS_DIR, "confusion_matrix.png")
    plot_confusion_matrix(cm, class_names, cm_image_path)

if __name__ == "__main__":
    best_model_chk = os.path.join(Config.SAVED_MODELS_DIR, "best_model.pth")
    # If full fine-tuned model doesn't exist, try fallback to trained head checkpoint
    if not os.path.exists(best_model_chk):
        best_model_chk = os.path.join(Config.SAVED_MODELS_DIR, "best_head_model.pth")
        
    try:
        run_evaluation(best_model_chk)
    except FileNotFoundError as e:
        logging.error(e)
