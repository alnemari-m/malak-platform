"""Knowledge distillation: train a small student model using a
larger teacher model's soft predictions."""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class KnowledgeDistiller:
    """Knowledge distillation with temperature scaling.

    Args:
        teacher: Pre-trained teacher model (frozen).
        student: Smaller student model to train.
        temperature: Softmax temperature for soft targets (default 4.0).
        alpha: Weight for soft loss vs hard loss (default 0.7).
    """

    def __init__(self, teacher, student, temperature=4.0, alpha=0.7):
        self.teacher = teacher
        self.student = student
        self.temperature = temperature
        self.alpha = alpha

    def train(
        self,
        train_loader,
        test_loader=None,
        epochs=30,
        lr=0.001,
        device=None,
    ):
        """Run the distillation training loop.

        Returns:
            dict with best_accuracy and history.
        """
        device = device or torch.device("cpu")
        self.teacher = self.teacher.to(device).eval()
        self.student = self.student.to(device)

        optimizer = optim.Adam(self.student.parameters(), lr=lr)
        criterion_hard = nn.CrossEntropyLoss()

        best_acc = 0.0
        history = []

        for epoch in range(epochs):
            self.student.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for inputs, targets in train_loader:
                inputs, targets = inputs.to(device), targets.to(device)

                with torch.no_grad():
                    teacher_logits = self.teacher(inputs)

                student_logits = self.student(inputs)

                loss_hard = criterion_hard(student_logits, targets)

                T = self.temperature
                loss_soft = F.kl_div(
                    F.log_softmax(student_logits / T, dim=1),
                    F.softmax(teacher_logits / T, dim=1),
                    reduction="batchmean",
                ) * (T * T)

                loss = self.alpha * loss_soft + (1 - self.alpha) * loss_hard

                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                _, predicted = student_logits.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

            train_acc = 100.0 * correct / total
            msg = (
                f"Distill Epoch {epoch+1}/{epochs}  "
                f"Loss: {running_loss/total:.4f}  "
                f"Train Acc: {train_acc:.2f}%"
            )

            test_acc = None
            if test_loader is not None:
                test_acc = self._evaluate(self.student, test_loader, device)
                msg += f"  Test Acc: {test_acc:.2f}%"
                if test_acc > best_acc:
                    best_acc = test_acc

            print(msg)
            history.append({
                "epoch": epoch + 1,
                "train_acc": train_acc,
                "test_acc": test_acc,
                "loss": running_loss / total,
            })

        return {"best_accuracy": best_acc, "history": history}

    @staticmethod
    def _evaluate(model, loader, device):
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for inputs, targets in loader:
                inputs, targets = inputs.to(device), targets.to(device)
                outputs = model(inputs)
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()
        return 100.0 * correct / total
