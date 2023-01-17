
import streamlit as st
import os
import sqlite3
import pandas as pd
import base64
from st_aggrid import GridOptionsBuilder, AgGrid
from st_aggrid.shared import JsCode

main_path = os.path.dirname(__file__)
img_path = os.path.join(main_path, 'images')
if not os.path.exists(img_path):
    os.mkdir(img_path)

con = sqlite3.connect(os.path.join(main_path, 'users.db'), check_same_thread=False)
cur = con.cursor()


def read_pic(pic):
    try:
        return base64.b64encode(open(pic, 'rb').read()).decode()
    except:
        return ""


st.subheader('학생 사진 촬영')

col1, col2 = st.columns(2)
hakbun = col1.text_input('학번')
name = col2.text_input('성명')

pic = st.camera_input('사진찍기')

if pic is not None:
    img_name = hakbun+name
    fname, ext = os.path.splitext(pic.name)

    cur.execute(f"INSERT INTO users (stu_hakbun, stu_name, stu_pic) "
                f"VALUES ('{hakbun}', '{name}', '{os.path.join(main_path, 'images', img_name+ext)}')")
    con.commit()
    with open(os.path.join(img_path, img_name+ext), 'wb') as f:
        f.write(pic.getbuffer())

data = pd.read_sql('SELECT * FROM users', con)
st.dataframe(data)
if data.shape[0] > 0:
    for i, row in data.iterrows():
        imgExtn = row.stu_pic[-4:]
        row.stu_pic = f'data:image/{imgExtn};base64,' + read_pic(row.stu_pic)

gb = GridOptionsBuilder.from_dataframe(data)
gb.configure_default_column(editable=False, groupable=True)
# Add pagination
gb.configure_pagination(paginationAutoPageSize=True)
# Add a sidebar
gb.configure_side_bar()
# Enable multi-row selection
gb.configure_selection(
    'single',
    use_checkbox=True,
    groupSelectsChildren=True
)
render_image = JsCode("""
function renderImage(params) {
    // Create a new image element
    var img = new Image();

    // Set the src property to the value of the cell (should be a URL pointing to an image)
    img.src = params.value;

    // Set the width and height of the image to 50 pixels
    img.width = 50;
    img.height = 50;

    // Return the image element
    return img;
    }
    """)
gb.configure_column('stu_pic', cellRenderer=render_image)
gb.configure_column('stu_name', editable=True)
# gb.configure_column('stu_pic', hide=True)
gridOptions = gb.build()

grid_response = AgGrid(
    data,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT',
    update_mode='MODEL_CHANGED',
    allow_unsafe_jscode=True,
    fit_columns_on_grid_load=True,
    height=350

)


# file_list = os.listdir(img_path)
#
# for fname in file_list:
#     st.write(fname)
#     with open(os.path.join(img_path, fname), "rb") as file:
#         btn = st.download_button(
#                 label="Download image",
#                 data=file,
#                 file_name=fname,
#                 mime="image/jpg"
#               )

