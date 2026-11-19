import os
from PIL import Image, ImageDraw, ImageFilter
import numpy as np

src_path = "C:/Users/waula/.gemini/antigravity/brain/93cfd25b-8ff3-4256-ad4c-c713db50b566/.user_uploaded/media_1795113478738_d3075e55.jpg"
img = Image.open(src_path).convert("RGBA")
arr = np.array(img)

# Isolate Bigfoot:
# White background is [255, 255, 255]
r = arr[:, :, 0].astype(float)
g = arr[:, :, 1].astype(float)
b = arr[:, :, 2].astype(float)
is_bg = (r > 235) & (g > 235) & (b > 238)
alpha = np.where(is_bg, 0, 255).astype(np.uint8)

clean_arr = arr.copy()
clean_arr[:, :, 3] = alpha
cutout = Image.fromarray(clean_arr, mode="RGBA")

# Extract bust portrait (head, shoulders, chest)
# Bounding x: 305 to 720, y: 65 to 565
bust = cutout.crop((305, 65, 720, 565))

# Composite at 1024x1024 for supersampled anti-aliasing
size = 1024
radius = 210

# 1. Background gradient (Rich Deep Space Navy / Cyber Blue)
grad = Image.new("RGBA", (size, size))
for y in range(size):
    t = y / float(size)
    r_val = int(18 + 14 * t)
    g_val = int(28 + 26 * t)
    b_val = int(52 + 42 * t)
    for x in range(size):
        grad.putpixel((x, y), (r_val, g_val, b_val, 255))

# 2. Rounded badge mask
mask_1024 = Image.new("L", (size, size), 0)
d_mask = ImageDraw.Draw(mask_1024)
margin = 24
d_mask.rounded_rectangle(
    [margin, margin, size - margin, size - margin],
    radius=radius,
    fill=255
)

# Base background: Gradient clipped by rounded squircle
base_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
base_layer.paste(grad, (0, 0), mask_1024)

# 3. Outer Neon Cyan Rim & Inner Gold Accent
border_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
d_border = ImageDraw.Draw(border_layer)

# Neon Cyan Outer Rim (14px wide)
d_border.rounded_rectangle(
    [margin - 4, margin - 4, size - margin + 4, size - margin + 4],
    radius=radius + 4,
    outline=(0, 220, 255, 240),
    width=14
)

# Subtle Gold Inner Accent Line
d_border.rounded_rectangle(
    [margin + 12, margin + 12, size - margin - 12, size - margin - 12],
    radius=radius - 12,
    outline=(255, 215, 0, 160),
    width=4
)

# 4. Scale and position Bigfoot bust inside badge
target_h = int(size * 0.83) # ~850px tall
scale = target_h / float(bust.height)
target_w = int(bust.width * scale)

scaled_bust = bust.resize((target_w, target_h), Image.Resampling.LANCZOS)
bust_x = (size - target_w) // 2
bust_y = int(size * 0.12) # 120px from top

# 5. Drop shadow for Bigfoot
shadow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
shadow_mask = scaled_bust.split()[3].point(lambda a: int(a * 0.65))
shadow_layer.paste((0, 0, 0, 255), (bust_x + 8, bust_y + 16), mask=shadow_mask)
shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(radius=18))

# 6. Composite Bigfoot + shadow
char_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
char_layer = Image.alpha_composite(char_layer, shadow_layer)
char_layer.paste(scaled_bust, (bust_x, bust_y), scaled_bust)

# Clip char_layer to rounded mask
char_alpha = char_layer.split()[3]
combined_alpha = Image.fromarray(
    (np.array(char_alpha).astype(float) * np.array(mask_1024).astype(float) / 255.0).astype(np.uint8)
)
char_layer.putalpha(combined_alpha)

# Alpha composite: base_layer -> char_layer -> border_layer
final_badge = Image.alpha_composite(base_layer, char_layer)
final_badge = Image.alpha_composite(final_badge, border_layer)

# 7. Downscale with Lanczos for crystal-clear icons
resolutions = [256, 128, 64, 48, 32, 16]
icon_images = []

for res in resolutions:
    resized = final_badge.resize((res, res), Image.Resampling.LANCZOS)
    icon_images.append(resized)

# Save high-res master PNG
master_256 = icon_images[0]
master_256.save("assets/icon.png", format="PNG")
master_256.save("C:/Users/waula/.gemini/antigravity/brain/93cfd25b-8ff3-4256-ad4c-c713db50b566/icon.png", format="PNG")

# Save multi-size .ICO
master_256.save(
    "assets/icon.ico",
    format="ICO",
    sizes=[(r, r) for r in resolutions]
)
master_256.save(
    "C:/Users/waula/.gemini/antigravity/brain/93cfd25b-8ff3-4256-ad4c-c713db50b566/icon.ico",
    format="ICO",
    sizes=[(r, r) for r in resolutions]
)

print(f"Icon successfully generated at assets/icon.ico with sizes: {resolutions}")
print(f"Master PNG saved at assets/icon.png (256x256)")
