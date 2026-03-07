"""KL-divergence based distribution drift detection."""

import torch
import torch.nn.functional as F


class DriftDetector:
    """Detect distribution drift between reference and new data
    by comparing model output distributions via KL-divergence.

    Usage::

        detector = DriftDetector(model)
        detector.set_reference(reference_loader)
        result = detector.check(new_loader)
        if result['drift_detected']:
            print("Drift detected!")
    """

    def __init__(self, model, threshold=0.1):
        self.model = model.eval()
        self.threshold = threshold
        self._reference_dist = None

    def set_reference(self, loader, device=None):
        """Compute reference output distribution."""
        device = device or torch.device("cpu")
        self.model = self.model.to(device)
        all_probs = []

        with torch.no_grad():
            for inputs, _ in loader:
                inputs = inputs.to(device)
                logits = self.model(inputs)
                probs = F.softmax(logits, dim=1)
                all_probs.append(probs.cpu())

        self._reference_dist = torch.cat(all_probs, dim=0).mean(dim=0)

    def check(self, loader, device=None):
        """Check for drift against the reference distribution.

        Returns:
            dict with kl_divergence, threshold, and drift_detected.
        """
        if self._reference_dist is None:
            raise RuntimeError("Call set_reference() first.")

        device = device or torch.device("cpu")
        self.model = self.model.to(device)
        all_probs = []

        with torch.no_grad():
            for inputs, _ in loader:
                inputs = inputs.to(device)
                logits = self.model(inputs)
                probs = F.softmax(logits, dim=1)
                all_probs.append(probs.cpu())

        new_dist = torch.cat(all_probs, dim=0).mean(dim=0)

        kl = F.kl_div(
            new_dist.log().unsqueeze(0),
            self._reference_dist.unsqueeze(0),
            reduction="batchmean",
            log_target=False,
        ).item()

        return {
            "kl_divergence": kl,
            "threshold": self.threshold,
            "drift_detected": kl > self.threshold,
        }
