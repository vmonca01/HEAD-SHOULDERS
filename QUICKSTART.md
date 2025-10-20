# Quick Start Guide - Trading Bot with Pattern Recognition

## 🚀 Para Empezar Rápidamente

### 1. Instalación (5 minutos)

```bash
# Clonar el repositorio
git clone https://github.com/vmonca01/HEAD-SHOULDERS.git
cd HEAD-SHOULDERS

# Instalar dependencias
pip install -r requirements.txt

# Configurar credenciales
cp .env.example .env
# Editar .env con tus API keys de Binance
```

### 2. Probar sin API (Modo Demo)

```bash
# Ejecutar tests y demos sin necesidad de API
python test_patterns.py

# Ver ejemplos de uso
python example_usage.py

# Ejecutar tests unitarios
python test_unit.py
```

### 3. Usar con Binance API

Edita `.env`:
```bash
BINANCE_API_KEY=tu_api_key_aqui
BINANCE_API_SECRET=tu_api_secret_aqui
USE_TESTNET=True  # ¡Importante! Usa testnet primero
```

Ejecutar el bot:
```bash
python trading_bot.py
```

## 📊 Patrones Detectados

El bot reconoce automáticamente estos patrones:

| Patrón | Señal | Descripción |
|--------|-------|-------------|
| **Cabeza y Hombros** | 📉 Bajista | Hombro-Cabeza-Hombro |
| **Cabeza y Hombros Invertido** | 💹 Alcista | Patrón invertido |
| **Doble Techo** | 📉 Bajista | Dos picos iguales |
| **Doble Suelo** | 💹 Alcista | Dos valles iguales |
| **Cuña Ascendente** | 📉 Bajista | Converge hacia arriba |
| **Cuña Descendente** | 💹 Alcista | Converge hacia abajo |
| **Triángulo Ascendente** | 💹 Alcista | Soporte sube, resistencia plana |
| **Triángulo Descendente** | 📉 Bajista | Resistencia baja, soporte plano |
| **Triángulo Simétrico** | ⚖️ Neutral | Ambas líneas convergen |

## 🔧 Configuración Rápida

### Ajustar Sensibilidad
```bash
MIN_PATTERN_CONFIDENCE=0.7  # 0.5 = más patrones, 0.9 = más estricto
```

### Gestión de Riesgo
```bash
MAX_TRADE_AMOUNT=0.01        # Cantidad por trade
STOP_LOSS_PERCENTAGE=2.0     # Stop loss 2%
TAKE_PROFIT_PERCENTAGE=5.0   # Take profit 5%
```

### Seleccionar Patrones
```bash
ENABLE_HEAD_SHOULDERS=True
ENABLE_DOUBLE_TOP_BOTTOM=True
ENABLE_WEDGES=True
ENABLE_TRIANGLES=True
```

## 💡 Integración con Tu Bot Existente

Si ya tienes un bot de trading en Python, integra el reconocimiento de patrones así:

```python
from pattern_recognition import PatternRecognizer

# Inicializar una vez
recognizer = PatternRecognizer(min_confidence=0.70)

# En tu loop de trading
def tu_funcion_de_trading():
    # 1. Obtener datos (ya lo haces)
    df = obtener_datos_ohlcv()  # Tu función existente
    
    # 2. Analizar patrones (NUEVO)
    patterns = recognizer.analyze(df)
    
    # 3. Tomar decisiones
    if patterns:
        best = max(patterns, key=lambda x: x['confidence'])
        if best['confidence'] >= 0.75:
            if best['direction'] == 'bullish':
                tu_funcion_comprar()  # Tu función existente
            elif best['direction'] == 'bearish':
                tu_funcion_vender()  # Tu función existente
```

## 📝 Estructura del Código

```
HEAD-SHOULDERS/
├── pattern_recognition.py   # ⭐ Módulo principal de patrones
├── trading_bot.py           # 🤖 Bot completo con Binance
├── test_patterns.py         # 🧪 Tests sin API
├── test_unit.py            # ✅ Tests unitarios
├── example_usage.py        # 📚 Ejemplos de uso
├── requirements.txt        # 📦 Dependencias
├── .env.example           # ⚙️ Configuración ejemplo
└── README.md              # 📖 Documentación completa
```

## ⚠️ Checklist de Seguridad

Antes de ejecutar en REAL:

- [ ] ✅ Has probado en testnet (`USE_TESTNET=True`)
- [ ] ✅ API keys tienen permisos mínimos (solo trading, no retiros)
- [ ] ✅ Usas restricción de IP en Binance
- [ ] ✅ `MAX_TRADE_AMOUNT` es conservador
- [ ] ✅ Has entendido todos los patrones
- [ ] ✅ Tienes stop loss configurado
- [ ] ✅ Monitoreas el bot constantemente
- [ ] ✅ `.env` no está en git (verificar `.gitignore`)

## 🎯 Ejemplos de Uso Rápido

### Ver patrones en datos recientes
```bash
python test_patterns.py
```

### Probar con diferentes configuraciones
```python
# Alta precisión, pocas señales
recognizer = PatternRecognizer(min_confidence=0.85)

# Balance
recognizer = PatternRecognizer(min_confidence=0.70)

# Más señales, más ruido
recognizer = PatternRecognizer(min_confidence=0.55)
```

### Filtrar por tipo de patrón
```python
patterns = recognizer.analyze(df)

# Solo patrones alcistas
bullish = [p for p in patterns if p['direction'] == 'bullish']

# Solo cabeza y hombros
from pattern_recognition import PatternType
hs_patterns = recognizer.get_patterns_by_type(PatternType.HEAD_SHOULDERS)
```

## 📞 Soporte

- **Issues**: Reporta bugs en GitHub Issues
- **Documentación completa**: Ver `README.md`
- **Ejemplos**: Ejecutar `python example_usage.py`

## 🎓 Próximos Pasos

1. ✅ Ejecuta `python test_patterns.py` para ver demos
2. ✅ Lee `example_usage.py` para ver integraciones
3. ✅ Configura `.env` con tus credenciales
4. ✅ Prueba en testnet primero
5. ✅ Empieza con cantidades pequeñas
6. ✅ Monitorea y ajusta según resultados

---

**Recuerda**: El trading conlleva riesgos. Este bot es una herramienta educativa. 
Siempre haz tu propia investigación y nunca inviertas más de lo que puedes perder.
