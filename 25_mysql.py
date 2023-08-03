import streamlit as st

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
    

if (user_management()):
    device = st.sidebar.selectbox("Choose a device", ['Debot Magican', 'Debot M1'])





# # v2
# st.session_state["user_state"] = False

# if (not st.session_state["user_state"]):
#     input_username = st.text_input('Username')
#     input_password = st.text_input('Password')

#     try:
#         query_user = "SELECT * FROM sys_user WHERE username='" + input_username + "'AND password='" + input_password + "';"
#         st.write(query_user)
#         user = conn.query(query_user, ttl=30)
#     except Exception as e:
#         st.write(e)

#     st.write(user)
#     st.session_state["user_state"] = True


# if (not user.empty):
#     work_content = st.sidebar.selectbox("Choose a device", ['Debot Magican', 'Debot M1'])


# v1
# st.session_state["user_state"] = False

# if st.session_state["user_state"]:
#     work_content = st.sidebar.selectbox("Choose a device", ['Debot Magican', 'Debot M1'])

# else:
#     input_username = st.text_input('Username')
#     input_password = st.text_input('Password')

#     try:
#         query_user = "SELECT * FROM sys_user WHERE username='" + input_username + "'AND password='" + input_password + "';"
#         st.write(query_user)
#         user = conn.query(query_user, ttl=30)
#     except Exception as e:
#         st.write(e)

#     st.write(user)
#     if (not user.empty):
#         st.session_state["user_state"] = True