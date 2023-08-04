import streamlit as st
import pandas as pd
import io
from io import StringIO
import os
import time

# Initialize connection.
conn = st.experimental_connection('test', type='sql')

def check_new_user():
    # check username
    print(5)
    query_user = "SELECT * FROM sys_user WHERE username='" + st.session_state["new_username"] + "';"
    user = conn.query(query_user, ttl=30)
    if (not user.empty):
        print(6)
        st.write("Existing username")
        return False
    else:
        print(7)
        return True

# def check_new_password():
#     # check new_password = confirm_password
#     if (new_password is not confirm_password):
#         st.write("check password")
#         return False
#     else:
#         return True

def create_user():
    print(1)
    if (not st.session_state["new_username"]) or (not st.session_state["new_password"]) or (not st.session_state["confirm_password"]):
        print(2)
    elif (not check_new_user()) or (not st.session_state["new_password"] == st.session_state["confirm_password"]):
        print(3)
        print(st.session_state["new_password"])
        print(st.session_state["confirm_password"])
    else:
        print(4)
        create_new_user = "INSERT INTO sys_user (username, password) VALUES ('" + st.session_state["new_username"] + "', '" + st.session_state["new_password"] + "');"
        print("create user = ", create_new_user)
        with conn.session as s:
            try:
                s.execute(
                    create_new_user
                )
                s.commit()
            except Exception as e:
                print(e)
        # del st.session_state["new_username"]
        # del st.session_state["new_password"]
        # del st.session_state["confirm_password"]
        st.session_state["user_state"] = 3

def return_to_login():
    if (st.session_state["user_state"] is 2) or (st.session_state["user_state"] is 3):
        del st.session_state["user_state"]
    else:
        pass

def goto_user_register():
    st.session_state["user_state"] = 2

# check password
def password_entered():
    query_user_password = "SELECT * FROM sys_user WHERE username='" + st.session_state.input_username + "'AND password='" + st.session_state.input_password + "';"
    # st.write(query_user_password)
    user = conn.query(query_user_password, ttl=30)
    if (not user.empty):
        st.session_state["user_state"] = 1
    else:
        st.session_state["user_state"] = 0

def user_management():
    # print("user_management")
    if "user_state" not in st.session_state: # init
        st.text_input('Username', on_change=password_entered, key="input_username")
        st.text_input('Password', on_change=password_entered, key="input_password")
        st.button('Register', on_click=goto_user_register)
    elif st.session_state["user_state"] is 0: # password not correct
        st.text_input('Username', on_change=password_entered, key="input_username")
        st.text_input('Password', on_change=password_entered, key="input_password")
        st.error("😕 User not known or password incorrect")
        st.button('Register', on_click=goto_user_register)
        return False
    elif st.session_state["user_state"] is 1: # password correct, login
        return True
    elif st.session_state["user_state"] is 2: # user register
        # st.write("user state: 2")
        new_username = st.text_input('Enter your username', key="new_username")
        if new_username and (not check_new_user()):
            st.error("User already exists")

        new_password = st.text_input('Enter your password', key="new_password")
        confirm_password = st.text_input('Confirm your password', key="confirm_password")
        if new_password and confirm_password and (not new_password == confirm_password):
            st.error("Check your password")

        st.button('Register', on_click=create_user)
        st.button('Back', on_click=return_to_login)
        # create_user = "SELECT * FROM sys_user WHERE username='" + st.session_state.input_username + "'AND password='" + st.session_state.input_password + "';"

        return False
    elif st.session_state["user_state"] is 3: # user registered successfully, login
        st.write("user state: 3")
        st.button('Back', on_click=return_to_login)
        return False
    else:
        pass
    

faascli_path = 'faas-cli'
user_docker_name = 'sarahha'
openfaas_ip = 'http://127.0.0.1:57478/'
def build_function(function_name, function_code):
    # create function
    if os.system(faascli_path + ' new ' + function_name + ' -lang python3 -p ' + user_docker_name) == 0:
        info_box = st.info('函数创建完成')
        time.sleep(1)
    else:
        info_box = st.info('函数创建失败')
    # import requirements
    if os.system('pipreqs ./' + function_name + ' --encoding=utf8 --force') == 0:
        info_box.info('函数依赖添加完成')
        time.sleep(1)
    else:
        info_box = st.info('函数依赖添加失败')
    # build image
    if os.system('faas-cli build -f ./' + function_name + '.yml') == 0:
        info_box.info('函数镜像创建成功')
        time.sleep(1)
    else:
        info_box = st.info('函数镜像创建失败')
    # push to docker registry
    if os.system('faas-cli push -f ./' + function_name + '.yml') == 0:
        info_box.info('函数成功上传')
        time.sleep(1)
    else:
        info_box = st.info('函数上传失败')
    # deploy to openfaas
    if os.system('faas-cli deploy -f ./'
                    + function_name + '.yml --gateway ' + openfaas_ip) == 0:
        info_box.info('函数成功部署')
        time.sleep(1)
    else:
        info_box = st.info('函数部署失败')



if (user_management()):
    
    with st.sidebar:
        device = st.radio(
            "Choose a device",
            ("Debot Magican", "Debot M1")
        )
    # device = st.sidebar.selectbox("", ['Debot Magican', 'Debot M1'])

    if (device == "Debot Magican"):
        with st.sidebar:
            purpose = st.radio(
                "What's your purpose",
                ("Use a function", "Design a function")
            )

        if (purpose == "Use a function"):
            st.header("Function name: Occupy and Release")

        elif (purpose == "Design a function"):
            st.header("Function Name: Occupy and Release")

            function_import = st.selectbox("How to write functions?", ("Handwriting", "Uploading", "Using Github repository"))

            if (function_import == "Handwriting"):
                function_name = st.text_input("Your function name:")
                # input code
                function_code = st.text_area("Text to write your functions or you can upload your code", 
                                            '''def handle(req):\n\nreturn req''')
                st.code(function_code, language="python")
                # click button
                build_func_button = st.button("Build function") 
                if (build_func_button):
                    build_function(function_name, function_code)

            elif (function_import == "Uploading"):
                function_name = st.text_input("Your function name:")
                # file uploading
                uploaded_code_file = st.file_uploader("Choose a file...")
                if uploaded_code_file is not None:
                    function_code_string = StringIO(uploaded_code_file.getvalue().decode("utf-8"))
                    function_code = function_code_string.read()
                    st.code(function_code, language="python")
                else:
                    st.info('☝️ Upload a code file')
                st.button("Build function")


    elif (device == "Debot M1"):
        st.write()
    else:
        pass
    