
# 👨‍🎓 SABE - Sistema de Asignación de Becas Educativas

Sistema web que permite seleccionar a los estudiantes más adecuados para becas educativas, aplicando algoritmos como **Programación Dinámica** y **Greedy**, bajo principios **SOLID**, el patrón de diseño **Strategy** y una arquitectura **MVC** limpia y escalable.

Incluye generación de informes PDF con visualizaciones gráficas y uso de inteligencia artificial.

---

## 🚀 Tecnologías utilizadas

- **Python 3.13.5** – Backend principal con Flask  
- **Flask** – Microframework para construir la aplicación web  
- **HTML5 + CSS3** – Maquetación y estilos base  
- **JavaScript** – Interactividad en el frontend  
- **jQuery** – Manipulación del DOM y AJAX  
- **Bootstrap 5** – Diseño responsivo  
- **DataTables** – Tablas dinámicas e interactivas  
- **noUiSlider** – Sliders para filtros personalizables  
- **SweetAlert2** – Alertas visuales modernas  
- **Chart.js** – Visualización de datos en gráficos  
- **Puppeteer + Node.js** – Renderizado headless para generación de gráficos en imágenes  
- **pdfkit + wkhtmltopdf** – Generación de PDFs del informe final  
- **pandas + openpyxl** – Procesamiento de archivos Excel  
- **Google Gemini AI** – Generación de texto automatizado con IA  

---

## 🛠️ Instalación

### 1. Clona el repositorio

```bash
git clone https://github.com/soyeduardo01/SabeProject.git
cd SabeProject
```

---

### 2. Crea y activa un entorno virtual en Python

```bash
# Windows
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
python -m venv .venv
.venv\Scriptsctivate
```

---

### 3. Instala las dependencias de Python

```bash
pip install -r requirements.txt
```

---

### 4. Instala Node.js y Puppeteer

Asegúrate de tener [Node.js](https://nodejs.org/) instalado, luego ejecuta:

```bash
cd utils/puppeteer
npm install
```

Esto instalará Puppeteer y sus dependencias para renderizar los gráficos en imágenes base64.

---

### 5. Ejecuta la aplicación

```bash
python main.py
```


## 📌 Funcionalidades principales

- 📥 Carga de archivos Excel con encabezado personalizado (fila 5)  
- 🎯 Aplicación de filtros configurables con sliders dinámicos  
- 🧠 Algoritmo de selección configurable: Programación Dinámica o Greedy  
- 🧾 Generación de reportes detallados en Excel  
- 🤖 Generación de informe final en PDF (Google Gemini AI) y con gráficos incluidos  
- 💻 Interfaz moderna, responsiva y con validaciones en tiempo real  

---


## 🧠 Inteligencia Artificial

Se utiliza **Google Gemini AI** para generar un informe en base a los datos obtenidos de los postulantes que fueron o no seleccionados en la convocatoria. 

---

## ✅ Requisitos previos

- Python 3.13.5  
- Node.js v18+ (para Puppeteer)  
- wkhtmltopdf instalado y agregado al PATH del sistema  

---

## 👨‍💻 Autores

**Eduardo Vicente**  
[LinkedIn](https://www.linkedin.com/in/eduardo-antonio-vicente-herrera/)  
INTEC · ITLA

**Diego Rodríguez**  
[LinkedIn](https://www.linkedin.com/in/diego-manuel-rodriguez-arredondo-51b6a1290)  
INTEC · ITLA
