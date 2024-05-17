import drivers
from time import sleep
import RPi.GPIO as GPIO
from openai import OpenAI
import re
key = "YOUR KEY"

client = OpenAI(api_key=key)
scale = ['easy level', 'medium level', 'hard level', 'hardest level']
display = drivers.Lcd()

RED_PIN = 21
YELLOW_PIN = 16
GREEN_PIN = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(YELLOW_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

def light_on(pin):
    GPIO.output(pin, GPIO.HIGH)

def light_off(pin):
    GPIO.output(pin, GPIO.LOW)

def generate_math_question(level):
    
    prompt = f'Generate {scale[level]} Addition, Subtraction and Multiplication math questions with basic objects. Example questions include "1 apple + 1 apple" or "5 balls - 2 balls" or "5 balls * 2 balls". The questions should be straightforward and suitable for kids learning basic arithmetic operations.numbers should be below 100. Avoid complex scenarios and focus on simple, relatable objects to make the math game fun and engaging for children. Output each question as a string in the format "<number> <object> <operation> <number> <object>" and enclose them in a python list, such as ["3 pencils + 2 pencils","4 oranges - 1 orange","6 cookies * 3 cookies"].'
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": prompt},
        ],
        max_tokens=100,
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def check_answer(question, answer):
    try:
        return eval(question) == int(answer)
    except Exception as e:
        print("Error evaluating answer:", e)
        return False

def main():
    
    try:
        display.lcd_clear()       
        score = 0
        level = 1
        
        long_string("Welcome to Math GPT", 1)
        display.lcd_clear()
        display.lcd_display_string('Your Game starts',1)
        sleep(.5) 
        display.lcd_display_string('1',2)
        sleep(.5) 
        display.lcd_display_string('2',2)
        sleep(.5) 
        display.lcd_display_string('3',2)
        sleep(.5) 

        while True:
            
            questions_str = generate_math_question(level)
            try:
                questions = eval(questions_str)
            except Exception as e:
                print("Error parsing questions:", e)
            
            for question in questions:
                display.lcd_clear()
                print(question)
                question_string(question,1)
                display.lcd_display_string(question,1)
                while True:
                    display.lcd_display_string('   ',2) 
                    while True:
                        answer = input("Your Answer: ")
                        
                        if answer and answer.isdigit():
                            break
                    display.lcd_display_string(str(answer),2)    
                    question = re.sub(r'[^0-9\+\-x*]', '', question)
                    if check_answer(question, answer):
                        light_on(GREEN_PIN)
                        sleep(2)
                        light_off(GREEN_PIN)
                        display.lcd_clear() 
                        score+=10
                        
                        break
                    else:

                        light_on(RED_PIN)
                        sleep(1)
                        light_off(RED_PIN)
                         
            
            if level<3:
                level+=1
            display.lcd_clear()
            print('Level up!')
            display.lcd_display_string('Level up!', 1)
            print('Score:', str(score))
            display.lcd_display_string('Score '+ str(score), 2)
            light_on(YELLOW_PIN)
            sleep(2)
            light_off(YELLOW_PIN)
    except KeyboardInterrupt:
        print('Game stopped.')
        display.lcd_clear()
        GPIO.cleanup()
        

def long_string(text='', num_line=1, num_cols=16):
    if len(text) > num_cols:
        display.lcd_display_string(text[:num_cols], num_line)
        sleep(.5)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print, num_line)
            sleep(0.5)
    else:
        display.lcd_display_string(text, num_line)
        
def question_string(text='', num_line=1, num_cols=16):
    if len(text) > num_cols:
        display.lcd_display_string(text[:num_cols], num_line)
        for i in range(len(text) - num_cols + 1):
            text_to_print = text[i:i+num_cols]
            display.lcd_display_string(text_to_print, num_line)
            sleep(0.4)
    else:
        display.lcd_display_string(text, num_line)
        
if __name__ == "__main__":
    main()






