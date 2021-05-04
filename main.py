from tkinter import *
from tkinter import ttk
from ttkthemes import ThemedTk
from threading import Thread
from random import randint
import matplotlib.pyplot as plt

def thread_word(event=None):
    global s_rem, wpm
    s_rem = 0
    wpm = 0
    Thread(target=word_sel).start()

def view_perf():
    values = []
    with open('./res/log.txt') as file:
        for i in file:
            values.append(int(i.strip()))
    if len(values) == 1:
        values.append(values[0])
    attempts = [i+1 for i in range(len(values))]
    plt.subplots(1, 1, figsize=(7, 3))
    plt.plot(attempts, values, marker='o')
    plt.ylabel('WPM')
    plt.show()

def all_events():
    global temp_len, wpm
    body_txt.focus_set()
    text1 = body_txt.get(1.0, 'end-1c')
    text2 = model_txt.get(1.0, 'end-1c')
    count = 0
    errors = 0
    if len(text1) <= len(text2):
        model_txt.tag_delete('start', 'start1', 'start2', 'current')
        model_txt.tag_add('current', f'1.{len(text1)}', f'1.{len(text1)+1}')
        model_txt.tag_configure('current', foreground='green', underline=True)
        model_txt.see(f'1.{len(text1)}')
        for i in range(len(text1)):
            if text1[i] == text2[i]:
                count += 1
                model_txt.tag_add('start', f'1.{i}', f'1.{i+1}')
                model_txt.tag_configure('start', foreground='grey')
            else:
                if text2[i] == ' ':
                    model_txt.tag_add('start2', f'1.{i}', f'1.{i+1}')
                    model_txt.tag_configure('start2', foreground='red', underline=True)
                else:
                    model_txt.tag_add('start1', f'1.{i}', f'1.{i+1}')
                    model_txt.tag_configure('start1', foreground='red')
                errors += 1

    try:
        accuracy = round((count/len(text1))*100)
        wpm = round(((len(text1) - errors)/5) / ((61 - s_rem) / 60))
        lbl_wpm['text'] = 'WPM\n' + str(wpm) if wpm >= 0 else 'WPM\n0'
    except:
        accuracy = 0
    lbl_err['text'] = 'Errors\n' + str(errors) + '/' + str(len(text1))
    lbl_acc['text'] = 'Accuracy\n' + str(accuracy) + '%'
    model_txt.after(100, all_events)

def word_sel():
    global s_rem
    file_no = randint(0, 11)
    model_txt['state'] = 'normal'
    model_txt.delete(1.0, 'end-1c')
    model_txt.insert(INSERT, words[file_no])
    model_txt.tag_add('justify', 1.0, 'end')
    model_txt.tag_configure('justify', justify=CENTER)
    model_txt['state'] = 'disabled'
    lbl_wpm['text'] = 'WPM\n0'
    lbl_sec['text'] = 'Time\n60s'
    lbl_err['text'] = 'Errors\n0/0'
    lbl_acc['text'] = 'Accuracy\n0%'
    body_txt['state'] = 'normal'
    body_txt.delete(1.0, 'end-1c')
    model_txt['state'] = 'disabled'
    lbl_res.pack_forget()
    btn_rec.pack_forget()
    s_rem = 61

def thread_time():
    Thread(target=timer).start()

def thread_event():
    Thread(target=all_events).start()

def timer():
    global s_rem, wpm, temp
    text = body_txt.get(1.0, 1.1)
    if (len(text) == 1 or (len(text) == 0 and s_rem != 61)) and s_rem > 0:
        s_rem -= 1
        lbl_sec['text'] = 'Time\n' + str(s_rem) + 's'
    lbl_sec.after(1000, timer)
    temp = lbl_sec['text'][5:-1]
    if temp == '0':
        body_txt['state'] = 'disabled'
        lbl_res.pack(side=BOTTOM, pady=5)
        btn_rec.pack(side=RIGHT, padx=5)
        with open('./res/log.txt', 'a') as file:
            file.write(f'{wpm}\n')
        file.close()
        lbl_sec['text'] = 'Time\n00s'

root = ThemedTk(theme='yaru')
root.title('Touch Typing')
root.geometry('650x200+350+100')
root.config(bg='white')
root.resizable(0, 0)

s_rem = 61
temp_len = 0
wpm = 0
words = []

temp = None
with open('./res/word.txt') as f:
    for line in f:
        words.append(line.strip())
f.close()
result = 'Congrats! You have finished the test'

det_frame = Frame(root, bg='white')
det_frame.pack(padx=120, pady=10, fill='x')

lbl_acc = Label(det_frame, text='Accuracy\n0%', bg='white', font=('helvetica', 10, 'bold'))
lbl_acc.pack(side=LEFT, expand=True)

lbl_wpm = Label(det_frame, text='WPM\n0', bg='white', font=('helvetica', 10, 'bold'))
lbl_wpm.pack(side=LEFT, expand=True)

lbl_sec = Label(det_frame, text='Time\n60s', bg='white', font=('helvetica', 10, 'bold'))
lbl_sec.pack(side=LEFT, expand=True)

lbl_err = Label(det_frame, text='Errors\n0/0', bg='white', font=('helvetica', 10, 'bold'))
lbl_err.pack(side=LEFT, expand=True)

main_frame = Frame(root, bg='white')
main_frame.pack(padx=20, pady=10, fill='both')

model_txt = Text(main_frame, font=('helvetica', 15), fg='black', relief=FLAT, width=30, height=1, wrap=WORD)
model_txt.pack(pady=5, fill='x')

body_txt = Text(main_frame)
body_txt.place(x=1000, y=1000)

lbl_res = Label(root, text=result, font=('helvetica', 12, 'bold'), bg='white')

btn_frame = Frame(root, bg='white')
btn_frame.pack(side=BOTTOM, pady=10)

btn_res = ttk.Button(btn_frame, text='Reset', command=thread_word)
btn_res.pack(side=RIGHT, padx=5)

btn_rec = ttk.Button(btn_frame, text='View', command=view_perf)

word_sel()
thread_time()
thread_event()
root.bind('<F5>', thread_word)
root.mainloop()
