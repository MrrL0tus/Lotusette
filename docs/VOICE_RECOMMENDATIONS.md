# 🎤 Guide des Voix pour Lotusette

## 🌸 Recommandations de Banques de Voix TTS (Text-to-Speech)

Ce document présente les meilleures options pour donner une voix à Lotusette, avec des recommandations adaptées selon vos besoins et budget.

---

## 🏆 Recommandations Prioritaires

### 1. **ElevenLabs** ⭐⭐⭐⭐⭐
**Meilleur choix pour la qualité professionnelle**

- **Prix**: À partir de 5$/mois (30k caractères gratuits/mois)
- **Qualité**: Exceptionnelle, très naturelle et expressive
- **Langues**: Multilingue incluant le français
- **Personnalisation**: 
  - Voix pré-faites de haute qualité
  - **Voice Cloning**: Créez une voix unique pour Lotusette à partir d'échantillons audio
  - Contrôle de l'émotion et du style
- **Latence**: Faible (~1-2 secondes)
- **Intégration**: API Python simple

```python
# Exemple d'utilisation
from elevenlabs import generate, set_api_key

set_api_key("votre_clé_api")
audio = generate(
    text="Bonjour! Je suis Lotusette 🌸",
    voice="Voix personnalisée",
    model="eleven_multilingual_v2"
)
```

**Voix recommandées pour Lotusette**:
- **Bella**: Jeune, enjouée, amicale
- **Rachel**: Claire, professionnelle mais chaleureuse
- **Créer une voix personnalisée**: Idéal pour un personnage unique!

---

### 2. **Coqui TTS (Open Source)** ⭐⭐⭐⭐
**Meilleur choix gratuit et local**

- **Prix**: **GRATUIT** et open-source
- **Qualité**: Très bonne, proche de la qualité commerciale
- **Langues**: Multilingue incluant le français
- **Personnalisation**: 
  - Modèles pré-entraînés disponibles
  - **Voice Cloning**: Possible avec XTTS-v2
  - Fine-tuning possible
- **Latence**: Moyenne (~2-4 secondes selon le hardware)
- **Intégration**: Python natif, fonctionne localement

```python
# Exemple d'utilisation
from TTS.api import TTS

tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
tts.tts_to_file(
    text="Bonjour! Je suis Lotusette 🌸",
    speaker_wav="votre_echantillon_vocal.wav",  # Pour le cloning
    language="fr",
    file_path="output.wav"
)
```

**Avantages**:
- ✅ Gratuit, pas de coûts récurrents
- ✅ Fonctionne offline
- ✅ Privacy-friendly (données locales)
- ✅ Voice cloning de qualité

---

### 3. **PlayHT** ⭐⭐⭐⭐
**Excellent compromis qualité/prix**

- **Prix**: À partir de 19$/mois (gratuit: 2500 mots/mois)
- **Qualité**: Excellente, naturelle
- **Langues**: 142+ langues incluant le français
- **Personnalisation**: 
  - 900+ voix disponibles
  - **Voice Cloning** ultra-réaliste
  - Contrôle d'émotions
- **Latence**: Très faible
- **Intégration**: API REST simple

**Voix françaises recommandées**:
- **Charlotte**: Jeune, dynamique
- **Amélie**: Douce, amicale
- **Léa**: Moderne, expressive

---

### 4. **Azure TTS (Microsoft)** ⭐⭐⭐⭐
**Solution professionnelle et fiable**

- **Prix**: 15$/million de caractères (500k gratuits/mois)
- **Qualité**: Excellente
- **Langues**: 119+ langues
- **Personnalisation**: 
  - Neural voices de haute qualité
  - **Custom Neural Voice** (création de voix unique)
  - SSML pour contrôle fin
- **Latence**: Faible
- **Intégration**: SDK Python

```python
# Exemple d'utilisation
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="votre_clé",
    region="votre_région"
)
speech_config.speech_synthesis_voice_name = "fr-FR-DeniseNeural"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
result = synthesizer.speak_text_async("Bonjour! 🌸").get()
```

**Voix françaises recommandées**:
- **DeniseNeural**: Jeune, amicale
- **EloiseNeural**: Douce, professionnelle
- **HenriNeural**: Pour variété (masculine)

---

### 5. **OpenAI TTS** ⭐⭐⭐
**Simple et efficace**

- **Prix**: 15$/million de caractères
- **Qualité**: Bonne
- **Langues**: Multilingue
- **Personnalisation**: 
  - 6 voix pré-définies
  - Pas de voice cloning
- **Latence**: Faible
- **Intégration**: Très simple si vous utilisez déjà OpenAI

```python
# Exemple d'utilisation
from openai import OpenAI

client = OpenAI()
response = client.audio.speech.create(
    model="tts-1-hd",
    voice="nova",  # ou alloy, echo, fable, onyx, shimmer
    input="Bonjour! Je suis Lotusette 🌸"
)
response.stream_to_file("output.mp3")
```

**Voix recommandées**:
- **Nova**: Jeune, énergique
- **Shimmer**: Douce, chaleureuse
- **Alloy**: Neutre, amicale

---

## 💡 Recommandation Personnalisée pour Lotusette

### Option Idéale: **ElevenLabs avec Voice Cloning**

**Pourquoi?**
1. **Voix unique**: Créez une voix vraiment distinctive pour Lotusette
2. **Qualité exceptionnelle**: Son naturel et expressif
3. **Contrôle émotionnel**: Peut varier l'expression selon le contexte
4. **Multilingue**: Français et autres langues

**Comment créer la voix de Lotusette:**
1. Enregistrez 1-2 minutes d'échantillons vocaux (ou trouvez un acteur vocal)
2. Uploadez sur ElevenLabs pour créer le clone
3. Ajustez les paramètres (stabilité, similarité, exagération)
4. Intégrez dans Lotusette via l'API

### Option Budget/Privacy: **Coqui TTS (XTTS-v2)**

**Pourquoi?**
1. **Gratuit et open-source**
2. **Voice cloning de qualité**
3. **Fonctionne localement** (pas de dépendance cloud)
4. **Privacy-friendly**

---

## 📊 Tableau Comparatif

| Solution | Prix/mois | Qualité | Voice Cloning | Latence | Offline |
|----------|-----------|---------|---------------|---------|---------|
| **ElevenLabs** | 5$+ | ⭐⭐⭐⭐⭐ | ✅ Excellent | Faible | ❌ |
| **Coqui TTS** | Gratuit | ⭐⭐⭐⭐ | ✅ Bon | Moyenne | ✅ |
| **PlayHT** | 19$+ | ⭐⭐⭐⭐ | ✅ Excellent | Faible | ❌ |
| **Azure TTS** | Variable | ⭐⭐⭐⭐ | ✅ Premium | Faible | ❌ |
| **OpenAI TTS** | Variable | ⭐⭐⭐ | ❌ | Faible | ❌ |

---

## 🎯 Plan d'Intégration dans Lotusette

Le code suivant est déjà préparé dans l'architecture:

```
lotusette/voice/
├── tts/
│   ├── elevenlabs_tts.py    # À implémenter
│   ├── coqui_tts.py          # À implémenter
│   ├── azure_tts.py          # À implémenter
│   └── openai_tts.py         # À implémenter
```

### Exemple d'implémentation (à ajouter):

```python
# lotusette/voice/tts/elevenlabs_tts.py
from elevenlabs import generate, set_api_key
import sounddevice as sd
import soundfile as sf

class ElevenLabsTTS:
    def __init__(self, api_key: str, voice_name: str = "Lotusette"):
        set_api_key(api_key)
        self.voice_name = voice_name
    
    def speak(self, text: str) -> None:
        """Generate and play speech."""
        audio = generate(
            text=text,
            voice=self.voice_name,
            model="eleven_multilingual_v2"
        )
        
        # Play audio
        data, samplerate = sf.read(io.BytesIO(audio))
        sd.play(data, samplerate)
        sd.wait()
```

---

## 🎤 Sources d'Échantillons Vocaux

Pour créer une voix unique pour Lotusette:

### 1. **Acteurs Vocaux Professionnels**
- **Fiverr**: 5-50$ pour enregistrements courts
- **Voices.com**: Professionnel mais plus cher
- **Upwork**: Freelancers vocaux

### 2. **Synthèse à partir d'autres TTS**
- Utilisez une voix ElevenLabs comme base
- Ajustez et personnalisez

### 3. **Banques d'Échantillons Libres**
- **LibriVox**: Livres audio du domaine public
- **Common Voice (Mozilla)**: Dataset multilingue
- **VoxForge**: Échantillons vocaux libres

---

## 🚀 Prochaines Étapes

1. **Choisir la solution TTS** (recommandation: ElevenLabs ou Coqui)
2. **Créer/Choisir la voix** de Lotusette
3. **Implémenter le module TTS** dans `lotusette/voice/tts/`
4. **Intégrer avec le CLI** pour des réponses vocales
5. **Ajouter STT** (Speech-to-Text) pour conversations vocales complètes

---

## 📝 Notes Importantes

- **Éthique**: Si vous utilisez voice cloning, assurez-vous d'avoir les droits sur la voix source
- **Stockage**: Les fichiers audio peuvent être volumineux, considérez le streaming
- **Latence**: Pour des conversations fluides, visez <2 secondes de latence totale
- **Multimodalité**: Lotusette peut mixer texte et voix selon le contexte

---

**Bon développement! 🌸**

Pour toute question sur l'intégration vocale, consultez la documentation des providers ou créez une issue sur le repo.
