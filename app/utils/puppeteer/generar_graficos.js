// utils/puppeteer/generar_graficos.js

/**
 * Script Puppeteer que:
 * - Abre una plantilla HTML con gráficos
 * - Inyecta los datos desde un archivo JSON
 * - Espera a que jQuery los procese y genere los gráficos
 * - Extrae todas las imágenes base64 desde el DOM
 * - Imprime por consola el array en formato JSON (stdout)
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  try {
    const args = process.argv.slice(2);
    if (args.length !== 2) {
      throw new Error('Debes proporcionar la ruta del HTML y del archivo JSON con los datos.');
    }

    const htmlPath = path.resolve(args[0]);
    const jsonPath = path.resolve(args[1]);
    const rawData = fs.readFileSync(jsonPath, 'utf-8');
    const datos = JSON.parse(rawData);
    const htmlContent = fs.readFileSync(htmlPath, 'utf-8');

    const browser = await puppeteer.launch({ headless: 'new' });
    const page = await browser.newPage();

    await page.setContent(htmlContent, { waitUntil: 'load' });

    // Inyectar datos en el navegador y renderizar los gráficos
    await page.evaluate((datos) => {
      window.renderCharts && window.renderCharts(datos);
    }, datos);

    // Esperar que los gráficos estén listos
    await page.waitForFunction('window.renderComplete === true', { timeout: 10000 });

    // Extraer imágenes base64 desde los canvas
    const imagenes = await page.evaluate(() => {
      return Array.from(document.querySelectorAll('canvas')).map(canvas => canvas.toDataURL('image/png'));
    });

    await browser.close();

    // Imprimir como salida JSON para ser capturado por Python
    console.log(JSON.stringify(imagenes));
  } catch (error) {
    console.error('Error generando los gráficos:', error);
    process.exit(1);
  }
})();
