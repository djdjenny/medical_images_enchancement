import logging
from typing import Optional
import torch
from torchvision import transforms
from PIL import Image

from model import UNetGenerator, UNetSkipConnectionLayer

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

MODEL_DIRS = {
    "ct": "ct_model/",
    "us": "us_model/",
    "mixed": "mixed_model/"
}

MODEL_FILES = {
    "enhancement": "GAN_QD_to_FD/GAN.pt",
    "blur": "GAN_FD_to_QD/GAN.pt"
}


logger = logging.getLogger(__name__)

MODEL_PATH = "/app/GAN.pt"


def load_model(model_type: str, task: Optional[str] = 'enhancement') -> torch.nn.Module:
    torch.serialization.add_safe_globals({"UNetGenerator": UNetGenerator})
    model = torch.load(MODEL_PATH, map_location=DEVICE, weights_only=False)
    model.eval()
    logger.debug(f"Uploaded model from {MODEL_PATH}")
    return model.to(DEVICE)


def process_image(input_path: str, model_type: Optional[str] = 'ct', task: Optional[str] = 'enhancement') -> str:
    model = load_model(model_type)
    image = Image.open(input_path).convert("L")
    logger.debug(f"Image was loaded from {input_path}")
    transform = transforms.Compose([
        transforms.Resize((512, 512)),
        transforms.ToTensor(),
    ])
    input_tensor = transform(image).unsqueeze(0).to(DEVICE)
    logger.debug("Image preprocessing done")
    with torch.no_grad():
        output = model(input_tensor)
    logger.info(f"Image {input_path} was successfully transformed")
    output_tensor = output.squeeze().clamp(0, 1).cpu()
    to_pil = transforms.ToPILImage()
    output_image = to_pil(output_tensor)
    result_path = input_path.replace(".jpg", "_processed.jpg")
    logger.info(f"Writing output to {result_path}")
    output_image.save(result_path)
    return result_path