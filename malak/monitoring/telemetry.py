"""Per-layer latency profiling via forward hooks."""

import torch
import time
from collections import OrderedDict


class LayerProfiler:
    """Profile per-layer inference latency using PyTorch forward hooks.

    Usage::

        profiler = LayerProfiler(model)
        profiler.run(dummy_input, iterations=50)
        report = profiler.report()
    """

    def __init__(self, model):
        self.model = model.eval()
        self._timings = OrderedDict()
        self._hooks = []

    def run(self, sample_input, iterations=50):
        """Profile each layer using pre+post forward hooks.

        Args:
            sample_input: A single input tensor.
            iterations: Number of forward passes to average over.

        Returns:
            self (for chaining).
        """
        self._timings.clear()
        self._remove_hooks()

        starts = {}

        for name, module in self.model.named_modules():
            if len(list(module.children())) > 0:
                continue
            self._timings[name] = []

            def make_pre(n):
                def pre_hook(mod, inp):
                    starts[n] = time.perf_counter()
                return pre_hook

            def make_post(n):
                def post_hook(mod, inp, out):
                    if n in starts:
                        self._timings[n].append(time.perf_counter() - starts[n])
                return post_hook

            h1 = module.register_forward_pre_hook(make_pre(name))
            h2 = module.register_forward_hook(make_post(name))
            self._hooks.extend([h1, h2])

        with torch.no_grad():
            for _ in range(iterations):
                self.model(sample_input)

        self._remove_hooks()
        return self

    def report(self):
        """Return a list of dicts sorted by mean_ms descending."""
        results = []
        for name, times in self._timings.items():
            if not times:
                continue
            mean_ms = sum(times) / len(times) * 1000
            results.append({"layer": name, "mean_ms": mean_ms})

        total = sum(r["mean_ms"] for r in results) or 1.0
        for r in results:
            r["fraction"] = r["mean_ms"] / total

        results.sort(key=lambda x: x["mean_ms"], reverse=True)
        return results

    def _remove_hooks(self):
        for h in self._hooks:
            h.remove()
        self._hooks.clear()
