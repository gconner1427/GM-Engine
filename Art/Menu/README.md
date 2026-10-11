# Menu backdrop

`Menu Backdrop.png` is the painted vault plate, exported at **3840 × 2160**. It was generated with the built-in image tool, then resized from its 1672 × 941 output for the requested delivery size.

The existing `/backdrop` route loads this file behind the light shafts, ring, die and dust. The menu's scrim stays above it. If the image is absent or cannot load, the procedural vault remains. The slot also accepts `Menu Backdrop.webp` or `Menu Backdrop.jpg`, in that order after PNG.

[Preview.png](Preview.png) shows the plate in the menu at 1920 × 1080. The image was also checked at 1366 × 768, 900 × 600 and 3440 × 1440, along with the 800 ms fade and absent/corrupt image fallbacks.

## Generation prompt

Use case: stylized-concept.

Asset type: final painted environment backdrop for a dark fantasy game's main menu, full-bleed 3840×2160 pixels, 16:9 landscape. This is the background plate only; the game overlays its own die, light effects and UI.

Primary request: Wide cinematic establishing shot of an empty ancient vault hall at night. Tall dark basalt pillars recede into black fog. A high circular oculus in the ceiling casts one soft shaft of warm golden light down the right of centre onto a polished black stone floor. Floating dust motes in the light. No characters, no text, no UI, no logo, no props or objects in the lit area (a 3D object will be placed there). The left third of the frame is very dark, for UI. Palette: obsidian black #0b0907, deep umber #1d1409, gold #c9a25b light. Painterly-realistic, AAA game key art, shallow haze, 16:9.

Composition: keep the open illuminated negative space centred near 66% of the frame width, extending through the middle of the frame and down onto the polished floor. Pillars frame the hall at its edges and recede into the background. The entire left third is near-black and visually quiet, retaining extremely subtle architectural detail. The single shaft is soft and restrained; the hall stays predominantly dark with warm umber shadows and muted gold light, preserving high contrast for overlaid menu text.

Constraints: environment only. No people, silhouettes, creatures, statues, readable writing, symbols, lettering, signage, watermarks, logos, menus, interface, dice, rune rings, treasure, furniture, pedestals, altars, or other props in the open centre-right area. Preserve empty floor and air for the separate 3D object. Output a polished final background painting, not a mockup.
