from PyQt5.QtWidgets import QApplication , QTextEdit , QLineEdit , QWidget , QMenuBar , QMenu , QAction , QMessageBox , QLabel , QPushButton , QInputDialog
from PyQt5.QtGui import QIcon, QFont , QPixmap
from sys import argv , exit
from webbrowser import open_new_tab
from json import load,dump
import openai as oa

with open("key.json","r") as file :
    oa.api_key = load(file)["key"].strip()

email_link = "https://mail.google.com/mail/u/0/?fs=1&to=social.sakshamjoshi@gmail.com&tf=cm"

class GUI :

    text_color = "rgba(239,239,249,255)"
    text_box_color = "rgba(63,65,78,255)"
    background_color_theme = "rgba(53,53,65,255)"
    menu_item_font = QFont("Times New Roman",pointSize=12,weight=87)
    text_box_font = QFont("Times New Roman",pointSize=13,weight=87)
    dashboard_font = QFont("Bahnschrift",pointSize=12)
    message_box_font = QFont("Bahnschrift",pointSize=10)

    about_text='''
    | Developed by : SAKSHAM JOSHI.
    | Github : https://github.com/saksham-joshi
    | Linkedin : https://www.linkedin.com/in/sakshamjoshi27/
    | Twitter : https://twitter.com/sakshamjoshi27/
    | Developed in : Python.
    | GUI Module : PyQT5.
    | Back-End Module : OpenAi.
    | Code Editor : Microsoft VS Code.
    '''

    def __init__(this) :

        this.app = QApplication(argv)
        this.icon = QIcon("icon.png")
        this.screen_size = this.app.primaryScreen().size()

        this.widget = QWidget()
        this.widget.setWindowIcon(this.icon)
        this.widget.setFixedSize(this.screen_size.width()//2 , this.screen_size.height()-130)
        this.widget.setWindowTitle("ChatGPT")
        this.widget.setStyleSheet(f'''
            background-color:{this.background_color_theme};
            color:white;
        ''')

        this.api_key_dashboard = QWidget()
        this.api_key_dashboard_setup()        # function to setup API Key Dashboard window

        
        # Menu bar and its components setup starts here ....🔽

        this.menubar = QMenuBar(this.widget)
        this.menubar.setGeometry(0,0,250 ,26)
        this.menubar.setFont(QFont("Acknowledgement",pointSize=12 ,weight=87))
        this.menubar.setStyleSheet('''
        QMenuBar{
            background-color:rgba(63,65,78,255);
            color:darkgray;
        }
        QMenuBar::hover{
            background-color:black;
            color:white;
        }
        ''')

        menu_stylesheet ='''
        QMenu::active{
            background-color:#071e26;
            color:white;
        }
        '''
        # chats menu setup ..........starts here
        this.chat_menu = QMenu("Chats",this.menubar)
        this.chat_menu.setStyleSheet(menu_stylesheet)

        this.new_chat = QAction("New Chat")
        this.new_chat.setFont(this.menu_item_font)

        this.load_chat = QAction("Load Chat")
        this.load_chat.setFont(this.menu_item_font)

        this.save_chat = QAction("Save Chat")
        this.save_chat.setFont(this.menu_item_font)

        this.delete_chat = QAction("Delete Chat")
        this.delete_chat.setFont(this.menu_item_font)

        this.chat_menu.addActions([this.new_chat , this.load_chat , this.save_chat , this.delete_chat])
        this.menubar.addMenu(this.chat_menu)
        this.chat_menu.triggered[QAction].connect(this.chat_menu_triggered)

        # option bar setup .................. starts here 
        this.options = QMenu("Options",this.menubar)
        this.options.setStyleSheet(menu_stylesheet)

        this.about_action = QAction("About")
        this.about_action.setFont(this.menu_item_font)
        
        this.feedback_action = QAction("Feedback")
        this.feedback_action.setFont(this.menu_item_font)

        this.change_api_key = QAction("Api-Key")
        this.change_api_key.setFont(this.menu_item_font)

        # adding QActions to the options Menu
        this.options.addActions([this.about_action, this.feedback_action, this.change_api_key])
        this.menubar.addMenu(this.options)
        this.options.triggered[QAction].connect(this.MenuItem_triggered)

        # Menu bar and its components setup ENDS here ....⬆️

        this.textbox = QTextEdit(this.widget)
        this.textbox.setFont(this.text_box_font)
        this.textbox.setMaximumWidth(this.screen_size.width()-50)
        this.textbox.setGeometry(5, this.widget.height()-100 , this.widget.width()-10 , 95)
        this.textbox.setStyleSheet("background-color:"+this.text_box_color+";border-radius:15px;color:"+this.text_color)
        this.textbox.setPlaceholderText("Send a message.")
        
        this.send_button = QPushButton(this.textbox,text="☑️")
        this.send_button.setGeometry(this.textbox.width()-50,this.textbox.height()-50,60,60)
        this.send_button.setFont(QFont("Acknowledgement",pointSize= 21,weight=87))
        this.send_button.pressed.connect(this.send_button_pressed)
        this.send_button.setStyleSheet('''
        QPushButton{
            border-radius:14px;
        }
        QPushButton::hover{
            background-color:rgba(0,0,0,50);
        }
        QPushButton::pressed{
            background-color:#071e26
        }
        ''')
        
        upper_line = QLabel(this.widget)
        upper_line.setGeometry(0,25,1280,5)
        upper_line.setPixmap(QPixmap("horizontal_line.png"))

        lower_line = QLabel(this.widget)
        lower_line.setGeometry(0,this.textbox.y()-10 ,1280,5)
        lower_line.setPixmap(QPixmap("horizontal_line.png"))

        this.main_box = QTextEdit(this.widget)
        this.main_box.setGeometry(0,upper_line.y()+5,this.widget.width(),lower_line.y()-upper_line.y()-5)
        this.main_box.setReadOnly(True)
        this.main_box.setStyleSheet("background-color:#303039;color:lightgray")
        this.main_box.setFont(this.text_box_font)

        this.widget.show()
        if oa.api_key.__len__() == 0 :
            this.api_key_dashboard.show()

        exit(this.app.exec())

    # function to setup API KEY Menu item in options menu of menubar ............ 👇
    def api_key_dashboard_setup(this) :
        this.api_key_dashboard.setFixedSize(640,230)
        this.api_key_dashboard.setStyleSheet("background-color:"+this.background_color_theme)
        this.api_key_dashboard.setWindowTitle("Api Key")
        this.api_key_dashboard.setWindowIcon(this.icon)

        label = QLabel(this.api_key_dashboard,text="\t          You can change & view your API Key from here.\n\n  Current Key : ")
        label.setGeometry(0,25,this.api_key_dashboard.width()-20,75)
        label.setFont(this.dashboard_font)
        label.setStyleSheet("color:white")

        textbox = QLineEdit(this.api_key_dashboard)
        textbox.setGeometry(10,110,620,40)
        textbox.setText(oa.api_key)
        textbox.setStyleSheet(f"border-radius:10px;background-color:{this.text_box_color};color:lightgray")
        textbox.setFont(QFont("Berlin Sans FB",pointSize=13))
        textbox.setDisabled(True)

        cancel_key : QPushButton

        def generate_key_pressed() :
            open_new_tab("https://platform.openai.com/account/api-keys")

        def change_key_pressed() :
            textbox.setEnabled(True)
            textbox.activateWindow()
            cancel_key.setHidden(False)

        def done_key_pressed() :
            oa.api_key = textbox.text()
            with open("key.json","w") as f :
                dump({"key" : oa.api_key} , f , indent=4)
            textbox.setDisabled(True)
            this.api_key_dashboard.hide()
            cancel_key.hide()
        def cancel_key_pressed() :
            textbox.setText(oa.api_key)
            textbox.setDisabled(True)
            cancel_key.hide()

        button_font = QFont("Bahnschrift",pointSize=10)
        button_stylesheet = '''
        QPushButton{
            background-color:#0a191e;
            color:white;
            border-radius:8px;
        }
        
        QPushButton::hover{
            background-color:rgba(0,0,0,50);
        }
        QPushButton::pressed{
            background-color:black;
        }
        '''
        cancel_key = QPushButton(this.api_key_dashboard,text="Cancel")
        cancel_key.setGeometry(this.api_key_dashboard.width()-100,75,65,25)
        cancel_key.setFont(this.dashboard_font)
        cancel_key.pressed.connect(cancel_key_pressed)
        cancel_key.hide()
        cancel_key.setStyleSheet('''
        QPushButton{
            background-color:#280a0a;
            color:white;
            border-radius:8px;
        }
        QPushButton::hover{
            background-color:#490e0e;
        }
        QPushButton::pressed{
            background-color:black;
        }
        ''')

        generate_key = QPushButton(this.api_key_dashboard,text="Generate-New")
        generate_key.setGeometry(90,170,130,30)
        generate_key.setFont(this.dashboard_font)
        generate_key.setStyleSheet(button_stylesheet)
        generate_key.pressed.connect(generate_key_pressed)

        change_key = QPushButton(this.api_key_dashboard,text= "Change-key")
        change_key.setGeometry(generate_key.x()+150,170,130,30)
        change_key.setFont(this.dashboard_font)
        change_key.setStyleSheet(button_stylesheet)
        change_key.pressed.connect(change_key_pressed)

        done_key = QPushButton(this.api_key_dashboard,text= "Done")
        done_key.setGeometry(change_key.x()+150,170,130,30)
        done_key.setFont(this.dashboard_font)
        done_key.setStyleSheet(button_stylesheet)
        done_key.pressed.connect(done_key_pressed)

    # API Key dashboard setup Ends here .............☝️
    def send_button_pressed(this) :
        text = this.textbox.toPlainText()
        if (not text.isspace()) and text.__len__() != 0 :
            this.main_box.append(" 👑You : "+text.strip().replace("\n" , "\n ")+"\n------------------------------------------------------------")
            this.textbox.setDisabled(True)
            this.send_button.setDisabled(True)
            this.textbox.clear()
            st = this.execute(text)
            if st != None :             # if a exception is caught on ChatGPT class in chatgpt.py file
                this.add_text_to_main_box(" 🤖ChatGPT : "+st.strip() ,False)
            this.textbox.setEnabled(True)
            this.send_button.setEnabled(True)

    # this function will be executed whenever a user sends a new text to the GPT or GPT replies to user
    def add_text_to_main_box(this , st : str,user : bool) :       #if user will send the text then it will be displayed in different color that's why user parameter is used 
        this.main_box.append(st.replace("\n","\n ") +"\n------------------------------------------------------------")

    def chat_menu_triggered(this,q : QAction) :
        if q.text() == "New Chat" :
            this.textbox.clear()
            this.main_box.clear()
            return
        elif q.text() == "Save Chat" :
            st  = this.main_box.toPlainText()
            if st.strip().__len__() == 0 :
                this.warning_displayer("Nothing is found to save your chat !","No chat found")
            else :
                file_name , valid = QInputDialog.getText(this.widget,"Save Chat", "Enter the Chat name to save :",echo= QLineEdit.Normal , text="")
                if valid :
                    chat_list = this.chat_list()
                    if chat_list == [None] : return
                    if file_name in chat_list :
                        this.warning_displayer("This Chat Name Already Exist. Choose a new one !","Chat Already exists")
                        this.chat_menu_triggered(QAction("Save Chat"))
                    else :
                        try :
                            this.chat_file_manipulate(file_name,"add")
                            this.warning_displayer("Chat saved succesfully","Saved")
                        except OSError : this.warning_displayer("Entered file name consists of some characters that are not allowed !\n e.g. < > / \ : | ","Invalid File Name")
                        #except Exception as e : print(e);this.warning_displayer("Something went wrong while saving your chat !","Error")
                return
        elif q.text() == "Load Chat" :
            chat_list = this.chat_list()
            if chat_list == [None] : return
            if chat_list == [] : this.warning_displayer("No Saved Chats found !","No chats") ; return
            item,valid = QInputDialog.getItem(this.widget, "Load Chat","Saved Chats" , tuple(chat_list) ,0,False)
            if valid :
                try :
                    this.main_box.clear()
                    with open("chats.json","r") as file :
                        chat = load(file)[item]
                        this.main_box.clear()
                        this.main_box.append(chat)
                except FileNotFoundError :
                    this.warning_displayer("The Choosen file doesn't exist !" , "File Not Found")
                except :
                    pass
        elif q.text() == "Delete Chat" :
            chat_list = this.chat_list()
            if chat_list == [None] : return
            if chat_list == [] : this.warning_displayer("No Saved Chats found !","No chats")
            item,valid = QInputDialog.getItem(this.widget , "Delete Chat","Saved Chats" , tuple(chat_list) ,0,False)
            if valid :
                try :
                    #remove(f"saved_chats/{item}.txt")
                    this.chat_file_manipulate(item,"delete")
                    this.warning_displayer("Chat Successfully deleted !","Deleted Chat")
                except :
                    this.warning_displayer("File not deleted !\n Something went wrong.","Failed to delete")

    # if menu items like about and feedback are pressed then this function will execute    
    def MenuItem_triggered(this,q : QAction) :
        if q.text() == "Api-Key" :
            this.api_key_dashboard.show()
        else :
            msg = QMessageBox(text=this.about_text)
            msg.setStandardButtons(QMessageBox.Ok)
            msg.setWindowIcon(this.icon)      
            msg.setStyleSheet("background-color:"+this.text_box_color+";color:white")
            msg.setWindowTitle(q.text())
            msg.setFont(this.message_box_font)
            match q.text() :
                case "About" : msg.setText(this.about_text)
                case "Feedback" :
                    def go_to_mail() :
                        open_new_tab(email_link)
                    msg.buttonClicked.connect(go_to_mail)
                    msg.setText("Namaste ,\n If you have any feedback to report then please click on Ok button.")
                case _: pass
            msg.exec()

    def warning_displayer(this,message : str,title : str) :
        qm = QMessageBox(this.widget , icon= this.icon , text=message)
        qm.setWindowTitle(title)
        qm.setStandardButtons(QMessageBox.Ok)
        qm.setStyleSheet("color:white")
        qm.setFont(this.message_box_font)
        qm.show()

    def execute(this,query : str) :
        try :
            c = oa.Completion.create(engine= "text-davinci-003" , prompt=query , max_tokens=512 , temperature=0.1)
            return c["choices"][0]["text"]
        except oa.error.APIConnectionError:
            this.warning_displayer("You are not connected to the Internet .","No Internet Connection.")
        except oa.error.AuthenticationError :
            this.api_key_dashboard.show()
            this.warning_displayer("The Entered API Key is not valid !","Wrong API Key")
        except oa.error.RateLimitError :
            this.warning_displayer("The Limit of tokens is exceeded !\n Enter a new valid API Key to fix it .","Token Limit Exceeded")
        except oa.error.Timeout :
            this.warning_displayer("Because your query took a long time to execute so our server closed the connection.\n Try again later","Request Timed Out")
        except oa.error.ServiceUnavailableError :
            this.warning_displayer("There is a problem found on our servers, please try after some time .","Server Problem")
        return None
    
    # function to get a tuple with filename on the old_chats directory
    def chat_list(this) :
        try : 
            with open("chats.json","r") as file :
                return list(load(file).keys())
        except : this.warning_displayer("We are Unable to find the chats , try to reinstall application to fix this !" , "Error") ; return [None]

    
    # function to add data and delete data from saved_chats_list.csv file
    def chat_file_manipulate(this,key : str , operation : str) :
        try :
            data : dict
            with open("chats.json","r") as file :
                data = load(file)
                if operation == "add" :
                    data[key] = this.main_box.toPlainText()
                elif operation == "delete" :
                    data.pop(key)
            with open("chats.json","w") as file :
                dump(data, file , indent=4)
        except : this.warning_displayer("Something went wrong while operating on your chat file","Error")

if __name__ == "__main__" :
    
    GUI()