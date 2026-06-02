# 🤖 FaceGen AI — Setup & Deploy Guide

## Kya hai yeh?
Flask website jisme aap apna photo + prompt dete ho aur AI aapka chehra preserve karke naya scene generate karta hai (InstantID technology use karke).

---

## STEP 1: Replicate API Token (FREE)

1. **https://replicate.com** pe jaao
2. **Sign Up** karo (GitHub se bhi ho sakta hai — bilkul free)
3. Account banne ke baad → **Settings → API Tokens**
4. **"Create token"** click karo
5. Token copy karo (r8_xxxxx... jaisa dikhega)

> 💡 Replicate free tier mein ~$5 credit milta hai new account pe — kaafi saari images ban sakti hain!

---

## STEP 2: GitHub pe Upload

1. **https://github.com** pe free account banao
2. **"New Repository"** banao — naam: `facegen-ai`
3. **"uploading an existing file"** click karo
4. Yeh saari files upload karo:
   - `app.py`
   - `requirements.txt`
   - `render.yaml`
   - `templates/index.html`
5. **Commit changes** click karo

---

## STEP 3: Render.com pe Deploy (FREE)

1. **https://render.com** pe jaao → free account banao
2. **"New Web Service"** click karo
3. **GitHub** se connect karo → apna `facegen-ai` repo select karo
4. Yeh settings rakho:
   - **Runtime**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 180`
5. **Environment Variables** section mein:
   - Key: `REPLICATE_API_TOKEN`
   - Value: aapka r8_xxxx token paste karo
6. **"Create Web Service"** click karo
7. 2-3 minute mein deploy ho jaayega!
8. Aapko ek URL milega jaise: `https://facegen-ai.onrender.com`

**Bas! Yahi URL share karo — kahin se bhi access karo!** 🎉

---

## Local Testing (Optional)

```bash
# Python install hona chahiye
pip install -r requirements.txt

# .env file banao
cp .env.example .env
# .env mein apna Replicate token paste karo

# Run karo
python app.py
```
Browser mein jaao: http://localhost:5000

---

## Important Notes

- **Face preservation**: InstantID model best results deta hai clear, front-facing photos se
- **Time**: Har image ~30-60 seconds mein banti hai
- **Free limits**: Replicate ka free credit khatam hone par pay karna padega (~$0.05 per image)
- **Render free tier**: App 15 minute idle rehe toh "sleep" ho jaata hai, pehli request slow hoti hai

---

## Files Structure

```
facegen-ai/
├── app.py              ← Flask backend
├── requirements.txt    ← Python packages
├── render.yaml         ← Render config
├── .env.example        ← Environment variables template
└── templates/
    └── index.html      ← Website UI
```
