# Trading Bot with Pattern Recognition

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Un bot de trading avanzado para Binance que identifica patrones clásicos de trading e ejecuta operaciones automáticamente.

## 🎯 Características

### Patrones Reconocidos

El bot identifica los siguientes patrones clásicos de trading:

1. **Head and Shoulders (Cabeza y Hombros)** - Patrón de reversión bajista
2. **Inverse Head and Shoulders (Cabeza y Hombros Invertido)** - Patrón de reversión alcista
3. **Double Top (Doble Techo)** - Patrón de reversión bajista
4. **Double Bottom (Doble Suelo)** - Patrón de reversión alcista
5. **Rising Wedge (Cuña Ascendente)** - Patrón bajista
6. **Falling Wedge (Cuña Descendente)** - Patrón alcista
7. **Ascending Triangle (Triángulo Ascendente)** - Patrón alcista
8. **Descending Triangle (Triángulo Descendente)** - Patrón bajista
9. **Symmetrical Triangle (Triángulo Simétrico)** - Patrón neutral

### Funcionalidades

- ✅ Conexión a Binance API (Real y Testnet)
- ✅ Análisis de patrones en tiempo real
- ✅ Ejecución automática de operaciones
- ✅ Gestión de riesgo (Stop Loss y Take Profit)
- ✅ Sistema de confianza para cada patrón detectado
- ✅ Logging completo de operaciones
- ✅ Modo demo sin API (para pruebas)

## 📋 Requisitos

- Python 3.8 o superior
- Cuenta de Binance con API keys
- Fondos en la cuenta (para trading real)

## 🚀 Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/vmonca01/HEAD-SHOULDERS.git
cd HEAD-SHOULDERS
```

2. **Crear entorno virtual (recomendado)**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
cp .env.example .env
```

Edita el archivo `.env` con tus credenciales:
```bash
# Binance API Configuration
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui

# Trading Configuration
TRADING_SYMBOL=BTCUSDT
TIMEFRAME=1h
LOOKBACK_PERIODS=100
MIN_PATTERN_CONFIDENCE=0.7

# Risk Management
MAX_TRADE_AMOUNT=0.01
STOP_LOSS_PERCENTAGE=2.0
TAKE_PROFIT_PERCENTAGE=5.0

# Pattern Recognition Settings
ENABLE_HEAD_SHOULDERS=True
ENABLE_DOUBLE_TOP_BOTTOM=True
ENABLE_WEDGES=True
ENABLE_TRIANGLES=True

# Testnet Mode (establecer a False para trading real)
USE_TESTNET=True
```

## 📖 Uso

### 1. Probar el reconocimiento de patrones (sin API)

```bash
python test_patterns.py
```

Este script:
- Genera datos sintéticos con diferentes patrones
- Demuestra la detección de cada tipo de patrón
- Crea gráficos visuales de los patrones detectados
- No requiere credenciales de API

### 2. Ejecutar el bot de trading

```bash
python trading_bot.py
```

El bot:
- Se conecta a Binance (testnet o producción según configuración)
- Analiza datos históricos del símbolo configurado
- Detecta patrones en tiempo real
- Ejecuta operaciones basadas en los patrones detectados

### 3. Modo continuo

Para ejecutar el bot continuamente, modifica en `trading_bot.py`:
```python
# Cambiar de:
bot.run(continuous=False, interval=300)

# A:
bot.run(continuous=True, interval=300)  # Revisa cada 300 segundos (5 min)
```

## 🔧 Configuración Avanzada

### Ajustar sensibilidad de patrones

En `.env`, ajusta `MIN_PATTERN_CONFIDENCE`:
- `0.5` - Más sensible (detecta más patrones, más falsos positivos)
- `0.7` - Balanceado (recomendado)
- `0.9` - Muy estricto (solo patrones muy claros)

### Habilitar/Deshabilitar patrones

Puedes controlar qué patrones buscar:
```bash
ENABLE_HEAD_SHOULDERS=True
ENABLE_DOUBLE_TOP_BOTTOM=True
ENABLE_WEDGES=False  # Deshabilitar cuñas
ENABLE_TRIANGLES=True
```

### Gestión de riesgo

Ajusta los porcentajes según tu estrategia:
```bash
STOP_LOSS_PERCENTAGE=2.0      # Stop loss al 2%
TAKE_PROFIT_PERCENTAGE=5.0    # Take profit al 5%
MAX_TRADE_AMOUNT=0.01         # Cantidad máxima por operación
```

## 📊 Estructura del Proyecto

```
HEAD-SHOULDERS/
├── trading_bot.py              # Script principal del bot
├── pattern_recognition.py      # Módulo de reconocimiento de patrones
├── test_patterns.py           # Script de pruebas y demostración
├── requirements.txt           # Dependencias del proyecto
├── .env.example              # Ejemplo de configuración
├── .gitignore               # Archivos ignorados por git
└── README.md                # Este archivo
```

## 🔍 Cómo funcionan los patrones

### Head and Shoulders (Cabeza y Hombros)
- **Señal**: Bajista (vender)
- **Estructura**: Hombro izquierdo - Cabeza - Hombro derecho
- **Confirmación**: Ruptura de la línea del cuello

### Double Top (Doble Techo)
- **Señal**: Bajista (vender)
- **Estructura**: Dos picos aproximadamente al mismo nivel
- **Confirmación**: Ruptura del soporte entre picos

### Rising Wedge (Cuña Ascendente)
- **Señal**: Bajista (vender)
- **Estructura**: Máximos y mínimos ascendentes que convergen
- **Confirmación**: Ruptura a la baja

### Falling Wedge (Cuña Descendente)
- **Señal**: Alcista (comprar)
- **Estructura**: Máximos y mínimos descendentes que convergen
- **Confirmación**: Ruptura al alza

### Triangles (Triángulos)
- **Ascendente**: Alcista - Resistencia plana, soporte ascendente
- **Descendente**: Bajista - Soporte plano, resistencia descendente
- **Simétrico**: Neutral - Ambas líneas convergen

## ⚠️ Advertencias Importantes

### Riesgos del Trading

- **El trading conlleva riesgos**: Puedes perder tu capital
- **Prueba en testnet primero**: Siempre usa `USE_TESTNET=True` inicialmente
- **Empieza con cantidades pequeñas**: Usa `MAX_TRADE_AMOUNT` conservador
- **No es asesoramiento financiero**: Este bot es para fines educativos
- **Monitorea constantemente**: No dejes el bot sin supervisión

### Seguridad

- **Nunca compartas tus API keys**
- **Usa restricciones de IP en Binance**: Limita el acceso a tu IP
- **Permisos mínimos**: Solo habilita trading spot (no retiros)
- **Revisa el archivo `.gitignore`**: Asegura que `.env` no se suba a git

## 🐛 Troubleshooting

### Error: "API credentials not found"
- Verifica que el archivo `.env` existe
- Confirma que `BINANCE_API_KEY` y `BINANCE_API_SECRET` están configurados

### Error: "Insufficient data for pattern analysis"
- Aumenta `LOOKBACK_PERIODS` en `.env`
- Verifica que el símbolo tiene suficiente historial

### No se detectan patrones
- Reduce `MIN_PATTERN_CONFIDENCE` para ser más permisivo
- Verifica que los patrones están habilitados en `.env`
- Algunos mercados/timeframes pueden no tener patrones claros

### Error de conexión a Binance
- Verifica tus credenciales API
- Confirma que tu IP no está bloqueada
- Revisa el status de Binance: https://www.binance.com/en/support/announcement

## 📝 Logs

El bot genera logs en:
- **Consola**: Salida en tiempo real
- **trading_bot.log**: Archivo con historial completo

## 🤝 Contribuciones

Las contribuciones son bienvenidas:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 📧 Contacto

Para preguntas o soporte, abre un issue en GitHub.

## 🙏 Agradecimientos

- Binance API por proporcionar acceso programático al exchange
- Comunidad de trading algorítmico
- Contribuidores del proyecto

---

**Disclaimer**: Este software se proporciona "tal cual", sin garantías de ningún tipo. El trading de criptomonedas es de alto riesgo y puedes perder todo tu capital. Usa este bot bajo tu propio riesgo.
