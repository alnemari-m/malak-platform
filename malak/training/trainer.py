"""Configurable PyTorch training loop."""

import torch
import torch.nn as nn
import torch.optim as optim
import time
from pathlib import Path


class Trainer:
    """Configurable training loop for PyTorch models.

    Args:
        model: PyTorch model to train.
        device: Device to train on ('cpu' or 'cuda').
        lr: Learning rate.
        momentum: SGD momentum.
        weight_decay: L2 regularization.
        optimizer_type: 'sgd' or 'adam'.
        scheduler_type: 'cosine' or None.
    """

    def __init__(
        self,
        model,
        device=None,
        lr=0.01,
        momentum=0.9,
        weight_decay=5e-4,
        optimizer_type="sgd",
        scheduler_type="cosine",
    ):
        self.device = device or torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        self.model = model.to(self.device)
        self.criterion = nn.CrossEntropyLoss()

        if optimizer_type == "sgd":
            self.optimizer = optim.SGD(
                model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay
            )
        elif optimizer_type == "adam":
            self.optimizer = optim.Adam(
                model.parameters(), lr=lr, weight_decay=weight_decay
            )
        else:
            raise ValueError(f"Unknown optimizer: {optimizer_type}")

        self.scheduler_type = scheduler_type
        self.scheduler = None

    def train(self, train_loader, test_loader, epochs, save_dir=None):
        """Run the full training loop.

        Returns:
            dict with best_accuracy, history, and best_model_path.
        """
        if self.scheduler_type == "cosine":
            self.scheduler = optim.lr_scheduler.CosineAnnealingLR(
                self.optimizer, T_max=epochs
            )

        best_acc = 0.0
        best_path = None
        history = []

        for epoch in range(epochs):
            train_loss, train_acc = self._train_epoch(train_loader)
            test_acc, test_latency = self.evaluate(test_loader)

            if self.scheduler is not None:
                self.scheduler.step()

            record = {
                "epoch": epoch + 1,
                "train_loss": train_loss,
                "train_acc": train_acc,
                "test_acc": test_acc,
                "test_latency_ms": test_latency,
            }
            history.append(record)

            print(
                f"Epoch {epoch+1}/{epochs}  "
                f"Train Loss: {train_loss:.4f}  "
                f"Train Acc: {train_acc:.2f}%  "
                f"Test Acc: {test_acc:.2f}%"
            )

            if test_acc > best_acc:
                best_acc = test_acc
                if save_dir is not None:
                    save_dir = Path(save_dir)
                    save_dir.mkdir(parents=True, exist_ok=True)
                    best_path = save_dir / "best_model.pth"
                    torch.save(self.model.state_dict(), best_path)

        return {
            "best_accuracy": best_acc,
            "history": history,
            "best_model_path": str(best_path) if best_path else None,
        }

    def _train_epoch(self, loader):
        self.model.train()
        running_loss = 0.0
        correct = 0
        total = 0

        for inputs, targets in loader:
            inputs, targets = inputs.to(self.device), targets.to(self.device)

            self.optimizer.zero_grad()
            outputs = self.model(inputs)
            loss = self.criterion(outputs, targets)
            loss.backward()
            self.optimizer.step()

            running_loss += loss.item() * inputs.size(0)
            _, predicted = outputs.max(1)
            total += targets.size(0)
            correct += predicted.eq(targets).sum().item()

        return running_loss / total, 100.0 * correct / total

    def evaluate(self, loader):
        """Evaluate model accuracy and per-image latency.

        Returns:
            (accuracy_percent, avg_latency_ms)
        """
        self.model.eval()
        correct = 0
        total = 0
        latencies = []

        with torch.no_grad():
            for inputs, targets in loader:
                inputs, targets = inputs.to(self.device), targets.to(self.device)

                if self.device.type == "cuda":
                    torch.cuda.synchronize()
                start = time.time()
                outputs = self.model(inputs)
                if self.device.type == "cuda":
                    torch.cuda.synchronize()
                elapsed = time.time() - start
                latencies.append(elapsed / inputs.size(0) * 1000)

                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

        accuracy = 100.0 * correct / total
        avg_latency = sum(latencies) / len(latencies) if latencies else 0.0
        return accuracy, avg_latency
