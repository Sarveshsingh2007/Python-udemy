from flask import Flask, request, render_template, redirect, url_for, send_file
from PIL import Image
import io
import numpy as np
import os
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))

def get_top_colors(pil_img, top_n=10, quantize_colors=64, resize_max=800):
    """
    pil_img: Pillow Image (any mode)
    top_n: how many colours to return
    quantize_colors: number of colours to quantize down to (speed + sensible palette)
    resize_max: maximum dimension to resize to (keeps processing fast)
    returns list of dicts: [{'rgb': (r,g,b), 'hex': '#rrggbb', 'count': n, 'percent': p}, ...]
    """
    img = pil_img.convert('RGB')

    # Resize proportionally if image is large (speed)
    w, h = img.size
    max_dim = max(w, h)
    if resize_max and max_dim > resize_max:
        scale = resize_max / max_dim
        img = img.resize((int(w*scale), int(h*scale)), Image.LANCZOS)

    # Quantize to reduce number of unique colors (Image.quantize uses adaptive palette)
    # Save and convert back to RGB to get palette colours as real RGB tuples
    img_q = img.quantize(colors=quantize_colors, method=Image.MEDIANCUT)
    img_rgb = img_q.convert('RGB')

    # Convert to NumPy array and count unique rows (colors)
    arr = np.array(img_rgb)
    pixels = arr.reshape(-1, 3)

    # Use structured dtype to get unique rows
    pixels_view = pixels.view([('', pixels.dtype)] * 3)
    unique, counts = np.unique(pixels_view, return_counts=True)
    unique = unique.view(pixels.dtype).reshape(-1, 3)

    # Sort by counts descending
    order = np.argsort(counts)[::-1]
    unique = unique[order]
    counts = counts[order]

    total = counts.sum()
    results = []
    for i in range(min(top_n, len(counts))):
        rgb = tuple(int(x) for x in unique[i])
        cnt = int(counts[i])
        percent = float(cnt) / float(total) * 100.0
        results.append({
            'rgb': rgb,
            'hex': rgb_to_hex(rgb),
            'count': cnt,
            'percent': round(percent, 2)
        })
    return results

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)
        try:
            img = Image.open(file.stream)
        except Exception as e:
            return render_template('index.html', error='Could not open image: ' + str(e))

        # Parameters (you can expose these to the user if you want)
        top_n = int(request.form.get('top_n', 10))
        quantize_colors = int(request.form.get('quantize_colors', 64))
        resize_max = int(request.form.get('resize_max', 800))

        results = get_top_colors(img, top_n=top_n, quantize_colors=quantize_colors, resize_max=resize_max)

        # Prepare an image preview as data URL to render back (small thumbnail)
        thumb = img.copy()
        thumb.thumbnail((400, 400))
        buf = io.BytesIO()
        thumb.save(buf, format='PNG')
        buf.seek(0)
        data_uri = 'data:image/png;base64,' + (io.BytesIO(buf.read()).getvalue()).hex()  # placeholder; we'll use different method in template

        # We'll instead send the results and render the preview by saving temporarily to memory via BytesIO as base64 in template
        # But easier: re-generate base64 properly
        import base64
        buf = io.BytesIO()
        thumb.save(buf, format='PNG')
        buf.seek(0)
        b64 = base64.b64encode(buf.read()).decode('ascii')
        preview_data = 'data:image/png;base64,' + b64

        return render_template('index.html', results=results, preview=preview_data, top_n=top_n,
                               quantize_colors=quantize_colors, resize_max=resize_max)
    return render_template('index.html')

if __name__ == '__main__':
    # Use port 5000 by default
    app.run(debug=True, host='0.0.0.0', port=5000)
