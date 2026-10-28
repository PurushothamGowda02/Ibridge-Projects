# 🎨 Design Quick Reference Guide

Quick reference for the Car Insurance Premium Calculator design system.

---

## 🎨 Color Palette

### Primary Colors
```css
--hot-pink:        #ff006e
--electric-purple: #8338ec
--bright-blue:     #3a86ff
--neon-green:      #06ffa5
```

### Background Gradient
```css
--coral: #ee7752
--pink:  #e73c7e
--blue:  #23a6d5
--teal:  #23d5ab
```

### Usage
- **Hot Pink:** Primary buttons, accents, highlights
- **Electric Purple:** Secondary elements, gradients
- **Bright Blue:** Tertiary accents, links
- **Neon Green:** Success states, positive indicators

---

## 📝 Typography

### Font Family
```css
font-family: 'Poppins', sans-serif;
```

### Font Weights
- **300** - Light (subtle text)
- **400** - Regular (body text)
- **600** - SemiBold (labels)
- **700** - Bold (subheadings)
- **900** - Black (main headings)

### Font Sizes
- **Title:** 3.5rem (56px)
- **Section Header:** 2.5rem (40px)
- **Subheader:** 1.8rem (29px)
- **Premium Amount:** 4.5rem (72px)
- **Body:** 1.05rem (17px)
- **Small:** 0.9rem (14px)

---

## ✨ Animations

### Keyframes
```css
@keyframes gradientBG { /* 15s - Background color shift */ }
@keyframes float { /* 3s - Vertical motion */ }
@keyframes pulse { /* 1s - Glow pulsing */ }
@keyframes shine { /* 3s - Light sweep */ }
@keyframes glow { /* 2s - Text glow */ }
@keyframes gradientText { /* 5s - Text color shift */ }
```

### Timing Functions
- **ease** - Default smooth
- **ease-in-out** - Smooth start and end
- **infinite** - Loop forever

---

## 💎 Glassmorphism

### Standard Card
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
border-radius: 20px;
border: 2px solid rgba(255, 255, 255, 0.3);
box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
```

### Enhanced Card
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(20px);
border-radius: 20px;
border: 2px solid rgba(255, 255, 255, 0.3);
```

---

## ⚡ Neon Glow

### Button Glow
```css
box-shadow: 
  0 0 20px rgba(255, 0, 110, 0.5),
  0 0 40px rgba(131, 56, 236, 0.3),
  0 0 60px rgba(58, 134, 255, 0.2);
```

### Hover Enhancement
```css
box-shadow: 
  0 0 30px rgba(255, 0, 110, 0.8),
  0 0 60px rgba(131, 56, 236, 0.6),
  0 0 90px rgba(58, 134, 255, 0.4);
```

---

## 🔮 3D Effects

### Premium Box
```css
transform: perspective(1000px) rotateX(5deg);
```

### Hover State
```css
transform: perspective(1000px) rotateX(0deg) scale(1.05);
```

---

## 🎯 Gradients

### Button Gradient
```css
background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
```

### Premium Box Gradient
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
```

### Text Gradient
```css
background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff, #06ffa5);
background-size: 300% 300%;
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
background-clip: text;
```

---

## 🎨 Hover Effects

### Card Hover
```css
transform: translateY(-10px) scale(1.02);
border-color: rgba(255, 255, 255, 0.6);
box-shadow: 0 15px 45px rgba(31, 38, 135, 0.5);
```

### Button Hover
```css
transform: scale(1.05) translateY(-5px);
animation: pulse 1s infinite;
```

---

## 📏 Spacing

### Padding
- **Small:** 1rem (16px)
- **Medium:** 1.5rem (24px)
- **Large:** 2rem (32px)
- **XLarge:** 3rem (48px)

### Margin
- **Small:** 0.5rem (8px)
- **Medium:** 1rem (16px)
- **Large:** 2rem (32px)

### Border Radius
- **Small:** 10px
- **Medium:** 15px
- **Large:** 20px
- **XLarge:** 30px
- **Pill:** 50px

---

## 🎭 Component Styles

### Section Header
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
padding: 2rem;
border-radius: 20px;
text-align: center;
```

### Info Card
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(20px);
padding: 2rem;
border-radius: 20px;
border: 2px solid rgba(255, 255, 255, 0.3);
transition: all 0.3s ease;
```

### Premium Display
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
padding: 3rem;
border-radius: 30px;
box-shadow: 0 20px 60px rgba(0,0,0,0.3);
transform: perspective(1000px) rotateX(5deg);
animation: float 3s ease-in-out infinite;
```

---

## 🌈 Emoji Usage

### Section Icons
- 🚗 - Car/Vehicle related
- 💰 - Money/Premium
- 📊 - Data/Analytics
- 👤 - Personal/User
- 🔮 - Prediction/AI
- ⚡ - Speed/Power
- ✨ - Special/Premium
- 💎 - Quality/Value
- 🎯 - Accuracy/Target
- 🌈 - Colorful/Visual

---

## 🔧 Transitions

### Standard
```css
transition: all 0.3s ease;
```

### Slow
```css
transition: all 0.5s ease;
```

### Fast
```css
transition: all 0.2s ease;
```

---

## 📱 Responsive Breakpoints

```css
/* Mobile */
@media (max-width: 768px) { }

/* Tablet */
@media (min-width: 769px) and (max-width: 1024px) { }

/* Desktop */
@media (min-width: 1025px) { }
```

---

## 🎨 Text Effects

### Shadow
```css
text-shadow: 0 2px 10px rgba(0,0,0,0.3);
```

### Glow
```css
text-shadow: 0 0 20px rgba(255,255,255,0.5);
```

### Strong Glow
```css
text-shadow: 
  0 0 20px rgba(255,255,255,0.5),
  0 0 40px rgba(255,255,255,0.3);
```

---

## 🎯 Quick Copy-Paste

### Glassmorphism Container
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(10px);
border-radius: 20px;
padding: 2rem;
border: 2px solid rgba(255, 255, 255, 0.3);
box-shadow: 0 8px 32px rgba(31, 38, 135, 0.37);
```

### Neon Button
```css
background: linear-gradient(45deg, #ff006e, #8338ec, #3a86ff);
color: white;
font-weight: 900;
padding: 1.2rem;
border-radius: 50px;
border: none;
box-shadow: 0 0 20px rgba(255, 0, 110, 0.5);
transition: all 0.3s ease;
```

### Floating Animation
```css
animation: float 3s ease-in-out infinite;

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
}
```

---

## 📚 Resources

### Fonts
- [Google Fonts - Poppins](https://fonts.google.com/specimen/Poppins)

### Color Tools
- [Coolors.co](https://coolors.co) - Color palette generator
- [Adobe Color](https://color.adobe.com) - Color wheel

### Inspiration
- [Dribbble](https://dribbble.com) - Design inspiration
- [Awwwards](https://awwwards.com) - Web design awards

### CSS References
- [MDN Web Docs](https://developer.mozilla.org) - CSS documentation
- [CSS-Tricks](https://css-tricks.com) - CSS tutorials

---

**Last Updated:** May 2026  
**Version:** 1.0  
**Design System:** Cyberpunk Glassmorphism

---

*Keep this guide handy for quick reference when working with the design!* 🎨✨
