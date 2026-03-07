"""Quantization-Aware Training (QAT).

Inserts fake-quantization observers during training so the model
learns to compensate for quantization noise, then converts to a
truly quantized INT8 model.
"""

import torch
import torch.nn as nn
import torch.optim as optim
import copy


class QAT:
    """Quantization-Aware Training pipeline.

    Usage::

        qat = QAT()
        model = qat.prepare(model)
        model = qat.train(model, train_loader, test_loader, epochs=20)
        quantized = qat.convert(model)
    """

    def prepare(self, model, backend="fbgemm"):
        """Insert fake-quantization modules.

        Args:
            model: FP32 model (must be on CPU).
            backend: 'fbgemm' (x86) or 'qnnpack' (ARM).

        Returns:
            Model with fake-quant observers inserted.
        """
        model = model.cpu().train()
        model.qconfig = torch.quantization.get_default_qat_qconfig(backend)
        torch.quantization.prepare_qat(model, inplace=True)
        return model

    def train(
        self,
        model,
        train_loader,
        test_loader=None,
        epochs=20,
        lr=0.001,
        momentum=0.9,
        weight_decay=1e-4,
    ):
        """Fine-tune with fake-quantization enabled.

        Args:
            model: Model returned by prepare().
            train_loader: Training DataLoader.
            test_loader: Optional test DataLoader for logging.
            epochs: Number of QAT fine-tuning epochs.
            lr: Learning rate (lower than initial training).
            momentum: SGD momentum.
            weight_decay: L2 regularization.

        Returns:
            Fine-tuned model (still with fake-quant modules).
        """
        device = torch.device("cpu")  # QAT requires CPU
        model = model.to(device).train()

        criterion = nn.CrossEntropyLoss()
        optimizer = optim.SGD(
            model.parameters(), lr=lr, momentum=momentum, weight_decay=weight_decay
        )
        scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs)

        best_acc = 0.0
        best_state = None

        for epoch in range(epochs):
            model.train()
            running_loss = 0.0
            correct = 0
            total = 0

            for inputs, targets in train_loader:
                inputs, targets = inputs.to(device), targets.to(device)

                optimizer.zero_grad()
                outputs = model(inputs)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()

                running_loss += loss.item() * inputs.size(0)
                _, predicted = outputs.max(1)
                total += targets.size(0)
                correct += predicted.eq(targets).sum().item()

            train_acc = 100.0 * correct / total
            scheduler.step()

            msg = (
                f"QAT Epoch {epoch+1}/{epochs}  "
                f"Loss: {running_loss/total:.4f}  "
                f"Train Acc: {train_acc:.2f}%"
            )

            if test_loader is not None:
                test_acc = self._evaluate(model, test_loader, device)
                msg += f"  Test Acc: {test_acc:.2f}%"
                if test_acc > best_acc:
                    best_acc = test_acc
                    best_state = copy.deepcopy(model.state_dict())

            print(msg)

        # Restore best checkpoint if available
        if best_state is not None:
            model.load_state_dict(best_state)

        return model

    def convert(self, model):
        """Convert fake-quant model to real INT8.

        Args:
            model: Model returned by train().

        Returns:
            Fully quantized INT8 model.
        """
        model.eval()
        quantized = torch.quantization.convert(model)
        return quantized

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
