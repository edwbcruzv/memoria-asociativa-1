import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

# Función para binarizar imágenes (negro=1, blanco=0)
def binarize_image(image, threshold=0.5):
    """
    Convierte una imagen en escala de grises a binario (negro=1, blanco=0).
    - image: Arreglo de NumPy (ej., alto x ancho).
    - threshold: Umbral normalizado (0 a 1). Para imágenes de 0-255, 0.5 equivale a 128.
    """
    # Si la imagen no está normalizada, la dividimos por 255
    if image.max() > 1:
        image = image / 255.0
    # Invertimos la lógica: valores <= threshold (negro) son 1, > threshold (blanco) son 0
    binary_image = (image <= threshold).astype(int)
    return binary_image

# Función para agregar ruido (aditivo, sustractivo, mixto)
def add_noise(pattern, percentage, noise_type='additive'):
    noisy = pattern.copy().flatten()
    n_pixels = len(noisy)
    n_change = int(n_pixels * percentage / 100)
    indices = np.random.choice(n_pixels, n_change, replace=False)
    
    if noise_type == 'additive':
        noisy[indices] = np.random.choice([0, 1], n_change)
    elif noise_type == 'subtractive':
        noisy[indices] = 0
    elif noise_type == 'mixed':
        half = n_change // 2
        noisy[indices[:half]] = np.random.choice([0, 1], half)
        noisy[indices[half:]] = 0
    
    return noisy.reshape(pattern.shape)

# Clase para Memoria Morfológica Autoasociativa (Máx y Mín)
class MorphologicalMemory:
    def __init__(self, n):
        self.n = n
        self.W = None
        self.M = None
    
    def train(self, patterns):
        p = len(patterns)
        self.W = np.zeros((self.n, self.n))
        self.M = np.zeros((self.n, self.n))
        
        for i in range(self.n):
            for j in range(self.n):
                self.W[i, j] = max([patterns[mu][i] - patterns[mu][j] for mu in range(p)])
                self.M[i, j] = min([patterns[mu][i] - patterns[mu][j] for mu in range(p)])
    
    def recall_max(self, pattern):
        pattern = pattern.flatten()
        y = np.zeros(self.n)
        for i in range(self.n):
            y[i] = min([self.W[i, j] + pattern[j] for j in range(self.n)])
        y = (y >= 0.5).astype(int)
        height = int(np.sqrt(self.n))
        return y.reshape(height, height)
    
    def recall_min(self, pattern):
        pattern = pattern.flatten()
        y = np.zeros(self.n)
        for i in range(self.n):
            y[i] = max([self.M[i, j] + pattern[j] for j in range(self.n)])
        y = (y >= 0.5).astype(int)
        height = int(np.sqrt(self.n))
        return y.reshape(height, height)

# Función para visualizar patrones (solo imagen ruidosa/prueba y recuperadas)
def plot_patterns(noisy, recovered_max, recovered_min, noise_type, percentage, category, idx, phase, filename=None):
    fig, axes = plt.subplots(1, 3, figsize=(9, 3))  # 3 subplots: ruidosa/prueba y recuperadas
    axes[0].imshow(noisy, cmap='binary')
    if noisy is not None and noise_type is not None:
        axes[0].set_title(f'Ruidoso ({noise_type}, {percentage}%)')
    else:
        axes[0].set_title(f'Prueba: {filename or f"Patrón {idx}"}')
    axes[1].imshow(recovered_max, cmap='binary')
    axes[1].set_title('Recuperado (Máx)')
    axes[2].imshow(recovered_min, cmap='binary')
    axes[2].set_title('Recuperado (Mín)')
    for ax in axes:
        ax.axis('off')
    # if noisy is not None and noise_type is not None:
    #     plt.savefig(f"resultado_{category}_{filename or f'patron{idx}'}_{noise_type}_{percentage}_fase{phase}.png")
    # else:
    #     plt.savefig(f"resultado_{category}_{filename or f'patron{idx}'}_fase{phase}.png")
    plt.show()

# Función principal para ejecutar el programa
def main():
    # Parámetros configurables
    training_folder = "train_chica/"  # Carpeta con imágenes de entrenamiento (CFP)
    testing_folder = "test/"         # Carpeta con imágenes de prueba

    # Fase 1: Lectura y preparación de imágenes de entrenamiento (CFP)
    train_images = []
    train_filenames = []
    for filename in sorted(os.listdir(training_folder)):
        if filename.endswith(".bmp"):
            filepath = os.path.join(training_folder, filename)
            img = Image.open(filepath).convert('L')
            img_array = np.array(img)
            train_images.append(img_array)
            train_filenames.append(filename)

    train_sets = {"numeros": train_images}
    for category in train_sets:
        train_sets[category] = [binarize_image(img) for img in train_sets[category]]

    # Validación de tamaños de entrenamiento
    for category in train_sets:
        shapes = [p.shape for p in train_sets[category]]
        if len(set(shapes)) > 1:
            raise ValueError(f"Los patrones en '{category}' tienen diferentes tamaños: {shapes}")

    # Fase 2: Lectura y preparación de imágenes de prueba
    test_images = []
    test_filenames = []
    for filename in sorted(os.listdir(testing_folder)):
        if filename.endswith(".bmp"):
            filepath = os.path.join(testing_folder, filename)
            img = Image.open(filepath).convert('L')
            img_array = np.array(img)
            test_images.append(img_array)
            test_filenames.append(filename)

    test_sets = {"numeros": test_images}
    for category in test_sets:
        test_sets[category] = [binarize_image(img) for img in test_sets[category]]

    # Validación de tamaños de prueba
    for category in test_sets:
        shapes = [p.shape for p in test_sets[category]]
        if len(set(shapes)) > 1:
            raise ValueError(f"Los patrones de prueba en '{category}' tienen diferentes tamaños: {shapes}")

    # Entrenamiento de la memoria con el CFP
    category = "numeros"
    train_patterns = train_sets[category]
    n = train_patterns[0].size
    height = train_patterns[0].shape[0]
    patterns_flat = [p.flatten() for p in train_patterns]
    memory = MorphologicalMemory(n=n)
    memory.train(patterns_flat)

    # Fase 1: Prueba de recuperación con el CFP original con ruido
    print("\nFase 1: Recuperación del CFP con ruido")
    noise_types = ['additive', 'subtractive', 'mixed']
    percentages = [1, 25, 50, 90]
    for idx, (train_image, filename) in enumerate(zip(train_patterns, train_filenames)):
        print(f"Probando patrón {filename}:")
        for noise_type in noise_types:
            for percentage in percentages:
                print(f"  Ruido {noise_type}, {percentage}%:")
                noisy_image = add_noise(train_image, percentage, noise_type)
                recovered_max = memory.recall_max(noisy_image)
                recovered_min = memory.recall_min(noisy_image)
                plot_patterns(noisy_image, recovered_max, recovered_min, noise_type, 
                              percentage, category, idx, 1, filename)

    # Fase 2: Prueba con patrones de prueba sin ruido
    print("\nFase 2: Prueba con patrones de prueba sin ruido")
    for idx, (test_image, test_filename) in enumerate(zip(test_sets[category], test_filenames)):
        print(f"Probando patrón de prueba {test_filename}:")
        recovered_max = memory.recall_max(test_image)
        recovered_min = memory.recall_min(test_image)
        plot_patterns(test_image, recovered_max, recovered_min, None, None, category, idx, 2, test_filename)

if __name__ == "__main__":
    main()