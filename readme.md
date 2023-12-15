#### roject Story

With the announcement of OpenAI, GPT's performance was further improved, and the GPT-4-Vision model for image capturing was introduced. Recently, many attempts have been made with the vision model, so I gave it a try. I thought it would be interesting to do a project utilizing my knowledge of AI and Prompt, and I was curious to see how well it could perform tasks that may be somewhat subjective, such as cooking meat.

#### Project flow

![img](https://maker.wiznet.io/upload/ckeditor5/453286645%5F1702631979.png)

**Recognize and store images with descriptions of meat (using GPT-4-vision)**

- Recognize an image with a description of meat using GPT-4-vision.
  Store the recognized information in context.


**Executability on the Streamlit web server**

- The image recognition and storage process mentioned above can be executed on the Streamlit web server. User submission and recognition of images via Streamlit
- A user submits a photo through Streamlit.
  The submitted photo is recognized with GPT-4-vision, referring to the context and few-shot prompt created in the first step of the process.


**Using Raspberry Pi and W5100S-EVB-PICO**

- The above process runs on a Raspberry Pi.
- The W6100-EVB-PICO is used as a temperature sensor to measure the actual temperature of the meat and send this data to the Raspberry Pi. TCP Client server is used in this process. 
- Based on the temperature data, the Raspberry Pi displays the programmed degree of doneness of the meat.


**User questions and meat status checks**

- The user can inquire about the doneness of the meat by asking a question.
  After the system answers the user's question and confirms that the meat is cooked, the user can consume the meat.

#### Source Code(S/W)

I've uploaded the code based on the code I studied to use Vision, but since there is a langchain library for LLM, I've also uploaded the langchain method for more efficient code refactoring.

![img](https://maker.wiznet.io/upload/ckeditor5/453286645%5F1702630883.png)

function.py is the source code that defines the functions used and is written as a library, while app.py contains the code that runs Streamlit and uses the UI GPT.

```plaintext
!git clone <project>
streamlit run app.py
```

file and run it. Make sure to set the openAI api key to your own.

**Prompt** 

mainprompt.txt

```plaintext
[instruction]
- You're a meat connoisseur, you're the best chef to know when meat is done, you're like Gordon Ramsay.
- {base64_image} to tell me when the meat is done.
- Make sure to take note of the {context}.
[output]
- doneness = "well done", "medium rare" , "rare", "raw"
- You should use your own judgment for the doneness of the meat. Make sure to output
- output the overall condition of the meat. In short
- Output format: 
ex) "I'm Gordon Ramsay Simon, a meat expert from the USA". According to your photo, the doneness of the meat is {meat doneness}. Enjoy your meal. 

Be sure to follow [instruction], [output] to output in Korean.
```

Systemprompt.txt

```plaintext
[instruction]
You recognize the doneness of the meat and related information from the image the other person sends you.

[output]
You describe the information you analyzed as best you can in text.
```

#### Source Code(H/W)

The above SW code is executed on Raspberry Pi, and we built an independent server by building a web server and separating the server from pico to ensure reliability.

**W6100-evb-pico <-> main webserver(Streamlit)**

![img](https://maker.wiznet.io/upload/ckeditor5/453286885%5F1702637840.png)