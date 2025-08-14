import streamlit as st
import numpy as np

# Set the page title and a fun emoji for the browser tab
st.set_page_config(page_title="Digital Art Generator", page_icon="🎨")

# --- App Title and Description ---
st.title("🎨 Digital Image Generator")
st.write(
    "Use the sliders to set the image dimensions and click the button to generate "
    "a unique piece of digital art using Python and NumPy!"
)

# --- User Inputs in the Sidebar ---
with st.sidebar:
    st.header("Image Controls")
    # Sliders for user to choose image dimensions
    img_width = st.slider("Select Image Width (px)", 100, 1000, 400)
    img_height = st.slider("Select Image Height (px)", 100, 1000, 400)
    
    # A slider to change the complexity of the pattern
    color_factor = st.slider("Color Complexity Factor", 1, 10, 2)


# --- Image Generation Logic ---
# This block runs only when the user clicks the button
if st.button("✨ Generate Image"):
    # Show a "spinner" message while the code is running
    with st.spinner("Creating your masterpiece..."):
        
        # 1. Create a blank 3D NumPy array (height, width, 3 channels for RGB)
        # The data type 'uint8' holds integers from 0-255, perfect for RGB colors.
        image_array = np.zeros((img_height, img_width, 3), dtype=np.uint8)

        # 2. Iterate over each pixel to calculate and set its color
        for y in range(img_height):
            for x in range(img_width):
                # 3. Generate RGB values based on pixel coordinates (x, y)
                # These mathematical formulas create interesting, complex patterns.
                # The modulo operator (%) ensures values wrap around to stay within the 0-255 color range.
                r = (x * y * color_factor) % 256
                g = ((x**2) + (y**2)) % 256
                b = (x + y + (color_factor * 10)) % 256
                
                # Assign the calculated [R, G, B] color to the current pixel
                image_array[y, x] = [r, g, b]

    # --- Display the Final Image ---
    st.success("Done! Here is your generated image.")
    # 
    st.image(
        image_array,
        caption=f"Generated Art ({img_width}x{img_height})",
        use_column_width=True
    )
    
else:
    # Initial message shown before the button is clicked
    st.info("Click the 'Generate Image' button to start.")