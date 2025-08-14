import streamlit as st

st.set_page_config(page_title="HTML + JS Tools", layout="centered")

st.title("🧩 HTML + JavaScript Tools")

st.write("This tool lets you embed and preview custom HTML and JavaScript snippets directly within Streamlit.")

html_code = st.text_area("Enter your HTML code:", height=250, placeholder="<h1>Hello, world!</h1>")
js_code = st.text_area("Enter your JavaScript code:", height=200, placeholder="console.log('Hello from JS');")

if st.button("Render"):
    st.components.v1.html(f"""
        <html>
        <body>
            {html_code}
            <script>
                {js_code}
            </script>
        </body>
        </html>
    """, height=500)
