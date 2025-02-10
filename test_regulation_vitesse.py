import numpy as np
import matplotlib.pyplot as plt

def regulation_vitesse(distance, vmax=200, vmin=45, coef=1, middle=4):
    """
    Régulation de la vitesse en fonction de la distance
    """
    vitesse = (vmax-vmin) * (0.5 * (1 - np.tanh(coef * (middle - distance)))) + vmin
    return max(0, min(vmax, vitesse))

# Paramètres de la régulation:
vmax = 200
coef = 1 # Particie à l'écrasement de la tangente hyperbolique (en le résuisant)
middle = 4 # Distance à laquelle la vitesse est moyenne
vmin = 45
distances = np.linspace(0, 20, 500)
vitesses = [regulation_vitesse(d) for d in distances]

# Tracé de la courbe
plt.figure(figsize=(10, 6))
plt.plot(distances, vitesses, label=f"Vitesse de {vmin} à {vmax}" , color='dodgerblue')
plt.axvline(x=middle, color='orange', linestyle='--', label='Vitesse moyenne')
plt.xlabel("Distance (m)")
plt.ylabel(f"Vitesse de {vmin} à {vmax}")
plt.title("Regulation de la vitesse en fonction de la distance")
plt.legend()
plt.grid(True)
plt.show()
