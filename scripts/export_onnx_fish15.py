# scripts/export_onnx_fish15.py
import argparse
import os
import torch
import torch.nn as nn

# --- Inline model definitions (minimal required) ---
class DualARTransformer(nn.Module):
    def __init__(self, num_layers=24, dim=2048, heads=16, vocab_size=1029, max_seq_len=4096, segment_size=10):
        super().__init__()
        from torch.nn import Embedding, Linear, LayerNorm, ModuleList
        self.token_embed = Embedding(vocab_size, dim)
        self.ref_embed = Linear(256, dim)
        self.layers = ModuleList([nn.TransformerEncoderLayer(d_model=dim, nhead=heads, batch_first=True) for _ in range(num_layers)])
        self.norm = LayerNorm(dim)
        self.head = Linear(dim, vocab_size)

    def forward(self, text_tokens, ref_audio_feat):
        x = self.token_embed(text_tokens)
        ref_proj = self.ref_embed(ref_audio_feat)
        x = torch.cat([ref_proj, x], dim=1)
        for layer in self.layers:
            x = layer(x)
        x = self.norm(x)
        return self.head(x[:, ref_audio_feat.size(1):, :])  # logits

class FireflyGAN(nn.Module):
    def __init__(self):
        super().__init__()
        # Simplified placeholder — actual implementation needed for export
        # But since we only need to load state_dict and trace, we use the real one if available.
        # For CI, we assume fish-speech is NOT installed → fallback to minimal stub won't work.
        # So we require fish-speech to be installed OR copy real module.
        try:
            from fish_speech.models.vqgan.modules.firefly import FireflyGAN as RealFirefly
            self.model = RealFirefly()
        except ImportError:
            raise ImportError("Please install fish-speech or provide real FireflyGAN implementation.")

    def forward(self, codes):
        return self.model(codes)

class DenseFeatureExtractor(nn.Module):
    def __init__(self):
        super().__init__()
        try:
            from fish_speech.feature_extractor import DenseFeatureExtractor as RealExtractor
            self.extractor = RealExtractor()
        except ImportError:
            raise ImportError("DenseFeatureExtractor requires fish-speech package.")

    def forward(self, audio):
        feats = self.extractor(audio)
        return feats.permute(0, 2, 1)
# ----------------------------------------------------

def export_text2sem(output_dir: str):
    print("📦 Exporting Text-to-Semantic...")
    model = DualARTransformer()
    ckpt = torch.load(f"{output_dir}/model.pth", map_location="cpu")
    model.load_state_dict(ckpt, strict=False)
    model.eval()

    text_tokens = torch.randint(0, 1024, (1, 100), dtype=torch.long)
    ref_audio_feat = torch.randn(1, 50, 256, dtype=torch.float32)

    torch.onnx.export(
        model, (text_tokens, ref_audio_feat),
        f"{output_dir}/fish_speech_text2sem.onnx",
        input_names=["text_tokens", "reference_audio"],
        output_names=["logits"],
        dynamic_axes={"text_tokens": {1: "T"}, "reference_audio": {1: "N"}},
        opset_version=17,
    )

def export_vocoder(output_dir: str):
    print("🔊 Exporting Vocoder...")
    model = FireflyGAN().model  # unwrap
    ckpt = torch.load(f"{output_dir}/firefly-gan-vq-fsq-8x1024-21hz-generator.pth", map_location="cpu")
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    codes = torch.randint(0, 1024, (1, 100), dtype=torch.long)
    torch.onnx.export(
        model, codes,
        f"{output_dir}/firefly_gan.onnx",
        input_names=["codes"],
        output_names=["waveform"],
        dynamic_axes={"codes": {1: "T"}},
        opset_version=17,
    )

def export_feature_extractor(output_dir: str):
    print("🎤 Exporting Feature Extractor...")
    extractor = DenseFeatureExtractor().eval()
    audio = torch.randn(1, 24000 * 3, dtype=torch.float32)
    torch.onnx.export(
        extractor, audio,
        f"{output_dir}/ref_audio_encoder.onnx",
        input_names=["audio_waveform"],
        output_names=["reference_features"],
        dynamic_axes={"audio_waveform": {1: "L"}},
        opset_version=17,
    )

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="models")
    args = parser.parse_args()

    # Ensure fish-speech is available for FireflyGAN & DenseFeatureExtractor
    try:
        import fish_speech
    except ImportError:
        raise RuntimeError("fish-speech must be installed: pip install git+https://github.com/fishaudio/fish-speech.git")

    export_text2sem(args.output_dir)
    export_vocoder(args.output_dir)
    export_feature_extractor(args.output_dir)
    print("🎉 Export completed!")

if __name__ == "__main__":
    main()
