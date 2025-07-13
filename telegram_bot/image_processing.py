import torch
from torchvision import transforms
from PIL import Image
import time


def load_model(model_path='model.pt', device=None):
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
    model = torch.load(model_path, map_location=device)
    model.eval()
    return model.to(device)


def preprocess_image(image: Image.Image, size=(256, 256)):
    transform = transforms.Compose([
        transforms.Resize(size),
        transforms.ToTensor(),            
    ])
    return transform(image).unsqueeze(0)

def process_image(model, image: Image.Image, device=None, verbose=True):
    if device is None:
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        
    input_tensor = preprocess_image(image).to(device)

    start_time = time.time()

    with torch.no_grad():
        output_tensor = model(input_tensor).cpu().squeeze(0)

    end_time = time.time()
    elapsed_time = end_time - start_time

    output_image = transforms.ToPILImage()(output_tensor.clamp(0, 1))

    if verbose:
        print(f" Время обработки: {elapsed_time:.3f} сек")

    return output_image, elapsed_time
