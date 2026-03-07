"""Magnitude and structured pruning via torch.nn.utils.prune."""

import torch
import torch.nn as nn
import torch.nn.utils.prune as prune
import torch.optim as optim


class MagnitudePruner:
    """Unstructured magnitude pruning.

    Zeroes out individual weights with the smallest absolute values.
    """

    def prune(self, model, amount=0.3):
        """Apply L1-unstructured pruning to all Conv2d and Linear layers.

        Args:
            model: PyTorch model.
            amount: Fraction of weights to prune (0.0 to 1.0).

        Returns:
            Pruned model (with pruning masks as forward hooks).
        """
        for _, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                prune.l1_unstructured(module, name="weight", amount=amount)
        return model

    def remove_masks(self, model):
        """Make pruning permanent by removing reparametrization hooks."""
        for _, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                try:
                    prune.remove(module, "weight")
                except ValueError:
                    pass
        return model

    def sparsity(self, model):
        """Return (nonzero_params, total_params, sparsity_fraction)."""
        total = 0
        nonzero = 0
        for param in model.parameters():
            total += param.numel()
            nonzero += torch.count_nonzero(param).item()
        sparsity_frac = 1.0 - (nonzero / total) if total > 0 else 0.0
        return nonzero, total, sparsity_frac


class StructuredPruner:
    """Structured pruning (filter-level for Conv2d, row-level for Linear)."""

    def prune(self, model, amount=0.3):
        """Apply structured L2-norm pruning.

        Args:
            model: PyTorch model.
            amount: Fraction of filters/neurons to prune.

        Returns:
            Pruned model.
        """
        for _, module in model.named_modules():
            if isinstance(module, nn.Conv2d):
                prune.ln_structured(
                    module, name="weight", amount=amount, n=2, dim=0
                )
            elif isinstance(module, nn.Linear):
                prune.l1_unstructured(module, name="weight", amount=amount)
        return model

    def remove_masks(self, model):
        """Make pruning permanent."""
        for _, module in model.named_modules():
            if isinstance(module, (nn.Conv2d, nn.Linear)):
                try:
                    prune.remove(module, "weight")
                except ValueError:
                    pass
        return model

    def sparsity(self, model):
        """Return (nonzero_params, total_params, sparsity_fraction)."""
        total = 0
        nonzero = 0
        for param in model.parameters():
            total += param.numel()
            nonzero += torch.count_nonzero(param).item()
        sparsity_frac = 1.0 - (nonzero / total) if total > 0 else 0.0
        return nonzero, total, sparsity_frac


def fine_tune(model, train_loader, device, epochs=10, lr=0.001):
    """Fine-tune a pruned model to recover accuracy.

    Args:
        model: Pruned model.
        train_loader: Training DataLoader.
        device: torch.device.
        epochs: Fine-tuning epochs.
        lr: Learning rate.

    Returns:
        Fine-tuned model.
    """
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=lr)

    model.train()
    for epoch in range(epochs):
        running_loss = 0.0
        for i, (images, labels) in enumerate(train_loader):
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

            if i % 100 == 99:
                print(
                    f"  Fine-tune Epoch [{epoch+1}/{epochs}], "
                    f"Step [{i+1}], Loss: {running_loss/100:.4f}"
                )
                running_loss = 0.0
    return model
