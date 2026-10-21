# 🔬 Batch Reactor Simulate - Backend
(VER CODIGO EN BRACH: simulate-BR-dev)
Backend desarrollado en Python para simular el comportamiento de un reactor batch (Tanque Agitado Discontinuo - TAD) en modo isotérmico y no isotérmico. Expone una API con FastAPI para recibir parámetros de simulación y devolver resultados numéricos y gráficos.

## 📦 Funcionalidades

- Simulación de reactores batch isotérmicos y no isotérmicos
- Reacciones reversibles e irreversibles
- Soporte para reactivo en exceso o sin B inicial
- Balance de energía para modo no isotérmico (adiabático, no adiabático, con camisa - ICQ)
- Estimación de volumen de reactor
- Detección automática del equilibrio químico
- API REST para comunicación con el frontend

## 🗂️ Estructura del repositorio

simulateBR/
├── main.py # API principal (FastAPI)
├── SimulateBatchReactor.py #Inicio de Simulacion 
├── IsothermalSimulate.py / IsothermalReactor.py # Simulación isotérmica
├── NonIsothermalSimulate.py  / NonIsothermalReactor.py # Simulación no isotérmica
├── ReactionUtils.py # Balance de materia y velocidad de reacción
├── Equilibrium.py # Cálculo de constante de equilibrio (Keq)
├── RateConstant.py # Cálculo de constante de velocidad (Arrhenius)
├── Stoichiometry.py # Cálculo de concentraciones a partir de conversión
├── EnergyBalance.py # Balance de energía (modo ICQ)
├── VolumeCalculation.py # Cálculo de volumen del reactor (Modo Isotermico)
├── requirements.txt # Dependencias del proyecto


## ⚙️ Instalación

1. Cloná el repositorio:

```bash
git clone https://github.com/RodrigoM10/Batch-Reactor-Simulate.git
cd SimulateBR
```
2. Instalá las dependencias:
  ```bash
pip install -r requirements.txt
``` 
3. Ejecutá el servidor de desarrollo:
  ```bash
uvicorn main:app --reload
``` 
La API estará disponible en http://localhost:8000/simulate #Simula Reactor Batch Completo

📊 Respuesta esperada
La respuesta incluye:

* Vectores de tiempo, conversión, concentraciones, temperatura (modo no isotérmico)
* Parámetros calculados (tiempo total, volumen si se solicita, conversión alcanzada)
* Datos listos para graficar en frontend

🌐 Integración con Frontend
Este backend está preparado para funcionar junto con una interfaz gráfica desarrollada en React.
Podés usarla desde el siguiente repositorio:

🔗 Frontend: Batch-Reactor-Front

La interfaz permite seleccionar el tipo de simulación, ingresar parámetros, enviar peticiones al backend y visualizar los resultados mediante gráficos interactivos.
Para conectarla:
Cloná y ejecutá el backend (uvicorn main:app --reload)
Cloná y ejecutá el frontend (npm run dev)
Asegurate de que el frontend apunte a http://localhost:8000 u otra URL donde tengas corriendo el backend.

📖 Documentación completa
La lógica interna y fundamentos del simulador se explican en el Trabajo Final de Rodrigo Mendoza:
"Modelado y Simulación de un Reactor Batch en Python" (2025).

👨‍💻 Autor
Rodrigo Mendoza
Estudiante de Ingeniería Química
📧 rodrigomendozar10@gmail.com
🔗 LinkedIn( https://www.linkedin.com/in/rodrigo-mendoza-b8b6931a4/ )
