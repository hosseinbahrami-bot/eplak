import os
from PIL import Image

def generate_icons():
    logo_path = "/home/user/eplak/eplak-fixed/assets/img/logo.png"
    im = Image.open(logo_path).convert("RGBA")
    
    # Crop to content bbox
    bbox = im.getbbox()
    if bbox:
        cropped = im.crop(bbox)
    else:
        cropped = im

    # Base square size 1024x1024
    base_size = 1024
    bg_color = (13, 21, 39, 255) # #0d1527
    
    canvas = Image.new("RGBA", (base_size, base_size), bg_color)
    
    # Scale cropped logo to fit inside canvas with 15% margin
    max_dim = int(base_size * 0.72)
    aspect = cropped.width / cropped.height
    if aspect > 1:
        new_w = max_dim
        new_h = int(max_dim / aspect)
    else:
        new_h = max_dim
        new_w = int(max_dim * aspect)
        
    resized_logo = cropped.resize((new_w, new_h), Image.Resampling.LANCZOS)
    offset_x = (base_size - new_w) // 2
    offset_y = (base_size - new_h) // 2
    
    canvas.paste(resized_logo, (offset_x, offset_y), resized_logo)
    
    # iOS App Store requirement: NO alpha channel for final app icon
    rgb_icon_1024 = canvas.convert("RGB")
    
    output_dir_ios = "/home/user/eplak/ios-app/Eplak/Assets.xcassets/AppIcon.appiconset"
    os.makedirs(output_dir_ios, exist_ok=True)
    
    sizes = {
        "AppIcon-1024.png": 1024,
        "AppIcon-180.png": 180,
        "AppIcon-120.png": 120,
        "AppIcon-87.png": 87,
        "AppIcon-80.png": 80,
        "AppIcon-60.png": 60,
        "AppIcon-58.png": 58,
        "AppIcon-40.png": 40,
        "AppIcon-29.png": 29,
        "AppIcon-20.png": 20
    }
    
    for filename, sz in sizes.items():
        resized = rgb_icon_1024.resize((sz, sz), Image.Resampling.LANCZOS)
        resized.save(os.path.join(output_dir_ios, filename), "PNG")
        
    # Also save PWA icons and apple-touch-icon in assets/img/
    pwa_dir = "/home/user/eplak/eplak-fixed/assets/img"
    canvas.resize((180, 180), Image.Resampling.LANCZOS).convert("RGB").save(os.path.join(pwa_dir, "apple-touch-icon.png"), "PNG")
    canvas.resize((192, 192), Image.Resampling.LANCZOS).convert("RGB").save(os.path.join(pwa_dir, "pwa-icon-192.png"), "PNG")
    canvas.resize((512, 512), Image.Resampling.LANCZOS).convert("RGB").save(os.path.join(pwa_dir, "pwa-icon-512.png"), "PNG")
    
    print("All iOS & PWA icons generated successfully!")

if __name__ == "__main__":
    generate_icons()
