import PIL.Image
from PIL import ImageDraw, ImageFont
import os

ASCII_CHARACTERS = ['@', '#', 'S', '%', '?', '*', '+', ';', ':', ',', '.']

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

def grayify(image):
    grayified_image = image.convert("L")
    return grayified_image

def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARACTERS[pixel // 25] for pixel in pixels])
    return characters

def pixels_to_ascii_with_color(gray_image, color_image):
    """Convert pixels to ASCII characters while preserving color information"""
    gray_pixels = gray_image.getdata()
    color_pixels = color_image.getdata()
    
    ascii_data = []
    for gray_pixel, color_pixel in zip(gray_pixels, color_pixels):
        char = ASCII_CHARACTERS[gray_pixel // 25]
        ascii_data.append((char, color_pixel))
    
    return ascii_data

def save_colorful_ascii_as_image(ascii_data, width, output_path="ascii_art_color.png", font_size=10):
    """Save colorful ASCII art as a PNG image"""
    # Calculate number of lines
    num_lines = len(ascii_data) // width
    
    # Try to use a monospace font
    try:
        font = ImageFont.truetype("consola.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("cour.ttf", font_size)
        except:
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", font_size)
            except:
                font = ImageFont.load_default()

    # Calculate character dimensions
    temp_img = PIL.Image.new('RGB', (1, 1))
    temp_draw = ImageDraw.Draw(temp_img)
    bbox = temp_draw.textbbox((0, 0), 'A', font=font)
    char_width = bbox[2] - bbox[0]
    char_height = bbox[3] - bbox[1]

    # Calculate image dimensions
    img_width = width * char_width + 20
    img_height = num_lines * char_height + 20

    # Create image with black background
    img = PIL.Image.new('RGB', (img_width, img_height), color='black')
    draw = ImageDraw.Draw(img)

    # Draw colorful ASCII art
    x_offset = 10
    y_offset = 10
    
    for i, (char, color) in enumerate(ascii_data):
        if i > 0 and i % width == 0:
            x_offset = 10
            y_offset += char_height
        
        draw.text((x_offset, y_offset), char, fill=color, font=font)
        x_offset += char_width

    img.save(output_path, 'PNG')
    print(f"Colorful ASCII art saved: {output_path}")

def save_ascii_as_html(ascii_data, width, output_path="ascii_art_color.html"):
    """Save colorful ASCII art as an HTML file"""
    num_lines = len(ascii_data) // width
    
    html_content = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: black;
            font-family: 'Courier New', monospace;
            font-size: 10px;
            line-height: 10px;
            white-space: pre;
            margin: 20px;
        }
        span {
            letter-spacing: 0;
        }
    </style>
</head>
<body>
"""
    
    for line_num in range(num_lines):
        start_idx = line_num * width
        end_idx = start_idx + width
        line_data = ascii_data[start_idx:end_idx]
        
        for char, color in line_data:
            r, g, b = color[:3] if len(color) >= 3 else (255, 255, 255)
            html_content += f'<span style="color:rgb({r},{g},{b})">{char}</span>'
        html_content += '\n'
    
    html_content += """</body>
</html>"""
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Colorful ASCII HTML saved: {output_path}")

def main(new_width=100):
    path = input("Enter image path: ")
    try:
        img = PIL.Image.open(path)
    except Exception as e:
        print(f"Error: {path} is invalid - {e}")
        return

    # Get filename without extension
    filename_without_ext = os.path.splitext(os.path.basename(path))[0]

    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)

    # Resize original color image
    color_img = resize_image(img.convert("RGB"), new_width)
    
    # Create grayscale version for ASCII character selection
    gray_img = grayify(color_img)

    # Get ASCII characters with color data
    ascii_data = pixels_to_ascii_with_color(gray_img, color_img)

    # Save as colorful PNG
    png_filename = os.path.join(output_dir, f"{filename_without_ext}_ascii_color.png")
    save_colorful_ascii_as_image(ascii_data, new_width, png_filename, font_size=10)

    # Save as colorful HTML (bonus - opens in browser!)
    html_filename = os.path.join(output_dir, f"{filename_without_ext}_ascii_color.html")
    save_ascii_as_html(ascii_data, new_width, html_filename)

    # Also save traditional grayscale version for comparison
    traditional_ascii = pixels_to_ascii(gray_img)
    pixel_count = len(traditional_ascii)
    ascii_image = "\n".join([traditional_ascii[index:(index+new_width)] 
                             for index in range(0, pixel_count, new_width)])
    
    txt_filename = os.path.join(output_dir, f"{filename_without_ext}_ascii_bw.txt")
    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(ascii_image)
    print(f"Traditional B&W ASCII saved: {txt_filename}")


if __name__ == "__main__":
    main()