import random
import time

import torch


class RandomLatentOrientation:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "latent": ("LATENT",),
                "swap_probability": (
                    "INT",
                    {"default": 50, "min": 0, "max": 100, "step": 1},
                ),
            }
        }

    RETURN_TYPES = ("LATENT",)
    RETURN_NAMES = ("latent",)
    FUNCTION = "orient"
    CATEGORY = "latent"

    @classmethod
    def IS_CHANGED(cls, latent, swap_probability):
        """Ensure that each queue submission makes a fresh random decision."""
        return time.time_ns()

    @staticmethod
    def _validate_latent(latent):
        if not isinstance(latent, dict):
            raise ValueError("latent must be a dictionary containing a 'samples' tensor")

        samples = latent.get("samples")
        if not torch.is_tensor(samples):
            raise ValueError("latent['samples'] must be a PyTorch tensor")
        if samples.ndim != 4:
            raise ValueError(
                "latent['samples'] must have shape [B, C, H, W]; "
                f"received {tuple(samples.shape)}"
            )

        noise_mask = latent.get("noise_mask")
        if noise_mask is not None:
            if not torch.is_tensor(noise_mask):
                raise ValueError("latent['noise_mask'] must be a PyTorch tensor when present")
            if noise_mask.ndim < 2:
                raise ValueError(
                    "latent['noise_mask'] must have at least two spatial dimensions; "
                    f"received {tuple(noise_mask.shape)}"
                )

        return samples, noise_mask

    def orient(self, latent, swap_probability):
        samples, noise_mask = self._validate_latent(latent)
        probability = int(swap_probability)

        if not 0 <= probability <= 100:
            raise ValueError(f"swap_probability must be between 0 and 100; received {probability}")

        height, width = samples.shape[-2:]
        should_swap = (
            height != width and random.randrange(100) < probability
        )
        if not should_swap:
            return (latent,)

        output = latent.copy()
        output["samples"] = samples.transpose(-2, -1)
        if noise_mask is not None:
            output["noise_mask"] = noise_mask.transpose(-2, -1)
        return (output,)


NODE_CLASS_MAPPINGS = {
    "RandomLatentOrientation": RandomLatentOrientation,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "RandomLatentOrientation": "Random Latent Orientation",
}
