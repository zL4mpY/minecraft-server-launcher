from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import pickle, configparser, os, sys, subprocess

window = Tk()
window.geometry('400x150')
window.title('Server Launcher')

try:
        window.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.ico'))
except Exception:
        pass

def on_closing():
	window.destroy()
	exit()

window.protocol("WM_DELETE_WINDOW", on_closing)

program_font = ('Calibri', 13)
button_font = ('Calibri', 9)

file = 'server.jar'
ram = '1G'
cmd = f'java -Xmx{ram} -Dfile.encoding=UTF-8 -jar {file}'

class ErrorWin:
	def __init__(self, error_message):
		from pyperclip import copy

		self.error_message = error_message
		self.error_win = Tk()
		self.error_win.geometry('300x300')
		self.error_win.title('Error!')
		
		try:
			self.error_win.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.ico'))
		except Exception:
			pass
		
		self.error_win.protocol("WM_DELETE_WINDOW", self.exit_prog)
		
		self.label = Label(master=self.error_win,
						text='Report this to developer!')
		
		self.errorbox = Text(master=self.error_win,
						width=275,
						height=250)
		
		self.copyerror_btn = Button(master=self.error_win,
						text='Copy error message',
						font=('Verdana', 8),
						command=lambda error_message=self.error_message: copy(error_message))
		
		self.exit_btn = Button(master=self.error_win,
						text='Exit',
						font=('Verdana', 8),
						command=self.exit_prog)
		
		self.errorbox.insert(0.0, self.error_message)
		self.errorbox.config(state=DISABLED)
		
		self.label.pack()
		self.errorbox.pack(pady=10)
		self.copyerror_btn.place(x=5, y=270)
		self.exit_btn.place(x=135, y=270)
		
		self.error_win.mainloop()
	
	def exit_prog(self):
		try:
			self.error_win.destroy()
			window.destroy()
			ngrok_menu.window.destroy()
			memory_win.destroy()
			sys.exit()
		except Exception:
			sys.exit()

def choose_jar_file():
	global file, cmd
	
	file = filedialog.askopenfilename(filetypes=(("Server File (.jar)", "*.jar"),("All files", "*.*")))
	if file == '':
		messagebox.showerror("Error", "You didn't choose the file!")
	else:
		if not file.endswith('.jar'):
			messagebox.showerror("Error", "Not valid server file!")
			file = ''
		else:
			cmd = f'java -Xmx{ram} -Dfile.encoding=UTF-8 -jar "{file}"'
			jar_file.delete(0, "end")
			jar_file.insert(0, file)
			cmd_text.delete(0,"end")
			cmd_text.insert(0, cmd)

def memory_window():
	memory_win = Tk()
	memory_win.geometry('225x125')
	memory_win.title('Choose RAM')
	
	try:
		memory_win.iconbitmap(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'icon.ico'))
	except Exception:
		pass
	
	memory_units = ['K (kilobyte)', 'M (megabyte)', 'G (gigabyte)']
	
	memory_label = Label(master=memory_win,
					text='Choose RAM for server: ',
					font=('Verdana', 9),
					fg='black',
					bg='white')
	
	memory_unit_label = Label(master=memory_win,
					text='Memory unit: ',
					font=('Verdana', 9),
					fg='black',
					bg='white')
	
	memory_entry = Entry(master=memory_win)
	
	combobox = ttk.Combobox(master=memory_win,
					values=memory_units,
					state="readonly")
	
	def destroy_win():
		global ram, cmd
		
		try:
			selected_unit = combobox.get()[0]
			ram = memory_entry.get()
			ram += selected_unit
			cmd = f'java -Xmx{ram} -Dfile.encoding=UTF-8 -jar {file}'
			cmd_text.delete(0,"end")
			cmd_text.insert(0, cmd)
			
			memory_win.destroy()
		except Exception:
			messagebox.showerror('Error', 'You have not chosen anything!')
	
	ok_btn = Button(master=memory_win,
					text='OK',
					font=('Verdana', 7),
					command=destroy_win)
	
	memory_label.pack()
	memory_entry.pack(pady=5)
	memory_unit_label.pack()
	combobox.pack()
	ok_btn.pack()
	
	memory_win.mainloop()

def save_settings():
	try:
		config = configparser.ConfigParser()
		
		config.add_section('global')
		config.set('global', 'launch_cmd', cmd)
		config.set('global', 'server_file', file)
		with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'), 'w') as configfile:
			config.write(configfile)
		messagebox.showinfo('Success', 'Saved your settings!')
	except Exception as error:
		messagebox.showerror('Error', 'An error occured while saving settings.')
		ErrorWin(str(type(error).__name__) + ': ' + str(error))

label = Label(master=window,
					text='Minecraft Server Launcher',
					font=program_font,
					fg='black',
					bg='white')

label_2 = Label(master=window,
					text='Server JAR file:',
					font=program_font,
					fg='black',
					bg='white')

label_3 = Label(master=window,
					text='Launch command: ',
					font=program_font,
					fg='black',
					bg='white')

jar_file = Entry(master=window,
					width = 33)

choose_jar_btn = Button(master=window,
					text='Choose',
					font=button_font,
					command=choose_jar_file)

choose_memory_btn = Button(master=window,
					text='RAM',
					font=button_font,
					command=memory_window)
					

cmd_text = Entry(master=window,
					width = 33)

cmd_text.insert(0, cmd)

save_settings_btn = Button(master=window,
					text='Save settings',
					font=button_font,
					command=save_settings)

def launch_server():
	try:
		cmd = cmd_text.get()
		window.destroy()
		
		subprocess.run(cmd, cwd=os.path.dirname(file))
	except Exception as error:
		messagebox.showerror('Error', 'An error occured while launching the server.')
		ErrorWin(str(type(error).__name__) + ': ' + str(error))

launch_server_btn = Button(master=window,
					text='Launch server!',
					font=button_font,
					command=launch_server)

label.pack()
label_2.place(x=5, y=30)
label_3.place(x=5, y=70)
jar_file.place(x=115, y=35)
choose_jar_btn.place(x=325, y=35)
cmd_text.place(x=140, y=75)
choose_memory_btn.place(x=350, y=75)
save_settings_btn.place(x=5, y=120)
launch_server_btn.place(x=160, y=120)

if os.path.exists(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')):
	config = configparser.ConfigParser()
	
	config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini'))
	
	cmd = config['global']['launch_cmd']
	file = config['global']['server_file']
	cmd_text.delete(0, "end")
	cmd_text.insert(0, cmd)
	jar_file.delete(0, "end")
	jar_file.insert(0, file)

window.mainloop()
