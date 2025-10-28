"""
Create Restaurant Icon for Desktop Shortcut
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGB', (size, size), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Draw a fork and knife icon (simplified restaurant symbol)
    # Draw a plate (circle)
    plate_center = (size // 2, size // 2)
    plate_radius = 80
    draw.ellipse(
        [plate_center[0] - plate_radius, plate_center[1] - plate_radius,
         plate_center[0] + plate_radius, plate_center[1] + plate_radius],
        fill='#34495e', outline='#fff', width=3
    )
    
    # Draw fork (left side)
    fork_x = plate_center[0] - 40
    fork_y1 = plate_center[1] - 30
    fork_y2 = plate_center[1] + 30
    draw.rectangle([fork_x-3, fork_y1, fork_x+3, fork_y2], fill='#fff')
    # Fork tines
    for i in range(4):
        tine_x = fork_x - 8 + (i * 5)
        draw.rectangle([tine_x, fork_y2-15, tine_x+3, fork_y2], fill='#fff')
    
    # Draw knife (right side)
    knife_x = plate_center[0] + 40
    knife_y1 = plate_center[1] - 30
    knife_y2 = plate_center[1] + 30
    draw.rectangle([knife_x-3, knife_y1, knife_x+3, knife_y2], fill='#fff')
    # Knife blade
    draw.polygon(
        [knife_x-3, knife_y1, knife_x+8, knife_y1+20, knife_x-3, knife_y1+20],
        fill='#fff'
    )
    
    # Add text at bottom
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = "HUNGER"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = size - 40
    draw.text((text_x, text_y), text, fill='#3498db', font=font)
    
    # Save as ICO
    img.save('restaurant_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("[OK] Icon created: restaurant_icon.ico")
    print("Icon includes multiple sizes for different display contexts")
    
except ImportError:
    print("PIL/Pillow not found. Installing...")
    import subprocess
    subprocess.run(["pip", "install", "pillow"])
    
    from PIL import Image, ImageDraw, ImageFont
    
    # Create a 256x256 icon
    size = 256
    img = Image.new('RGB', (size, size), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Draw a fork and knife icon
    plate_center = (size // 2, size // 2)
    plate_radius = 80
    draw.ellipse(
        [plate_center[0] - plate_radius, plate_center[1] - plate_radius,
         plate_center[0] + plate_radius, plate_center[1] + plate_radius],
        fill='#34495e', outline='#fff', width=3
    )
    
    # Draw fork
    fork_x = plate_center[0] - 40
    fork_y1 = plate_center[1] - 30
    fork_y2 = plate_center[1] + 30
    draw.rectangle([fork_x-3, fork_y1, fork_x+3, fork_y2], fill='#fff')
    for i in range(4):
        tine_x = fork_x - 8 + (i * 5)
        draw.rectangle([tine_x, fork_y2-15, tine_x+3, fork_y2], fill='#fff')
    
    # Draw knife
    knife_x = plate_center[0] + 40
    knife_y1 = plate_center[1] - 30
    knife_y2 = plate_center[1] + 30
    draw.rectangle([knife_x-3, knife_y1, knife_x+3, knife_y2], fill='#fff')
    draw.polygon(
        [knife_x-3, knife_y1, knife_x+8, knife_y1+20, knife_x-3, knife_y1+20],
        fill='#fff'
    )
    
    # Add text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
    
    text = "HUNGER"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = (size - text_width) // 2
    text_y = size - 40
    draw.text((text_x, text_y), text, fill='#3498db', font=font)
    
    img.save('restaurant_icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    
    print("[OK] Icon created: restaurant_icon.ico")

except Exception as e:
    print(f"Error creating icon: {e}")

