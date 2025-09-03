# Mini Intruder in Pitchfork mode

Python tool inspired by Burp Intruder, mainly designed to measure **response times**. 

You can :
- Inject payloads in the body or headers
- Launch the attack in Pitchfrok mode

It means that each **placehoders** (`§1§`, `§2§`, ..) corresponds to a payload file. This mode iterate line by line **in parallel** across all payload files :

- The **first line** of each file is used together to generate the first request
- The **second line** of each file is used together to generate the second request 
- And so on ..

👉 The total number of requests is limited by the **shortest** payload file

### 🔧 Installation

Clone the repo and install the dependencies:

````bash
git clone https://.git
cd request-timer
pip install requests
chmod +x request_timer.py
````

### 🚀 Launch the attack

````bash
python3 request_timer.py <url> \
  -p <payload1.txt> <payload2.txt> ... \
  -b "exemple=§3§&exemple2=§4§" \
  -H "Header1: §1§" -H "Header2: §2§" \
  -X POST
````

-p: payload files (in placeholder order)

-b: request body, with placeholders §1§, §2§...

-H: headers (placeholders can also be used)

-X: HTTP method (GET, POST, PUT...)
