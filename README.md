<p align="center">
  <h1 style="text-align: center;">inerG Flask Server Demo</h1>
</p>

****

---

## **Overview**

Flask server to calculate annual production data and provide an API for oil, gas, and brine data

---

## **Installation**

To install this project, follow these steps:

Make sure git, python and pip are installed

Installation steps:
```bash
# Clone the repository
git clone https://github.com/Jerryj1127/inerG-Flask-demo.git 

cd inerG-demo/ 

# Install the dependencies
pip install -r requirements.txt

# Start the server
python3 main.py

```

## **Demo**

Demo deployment of this github repo (Flask server) can be found at :


https://annual-prod-api.onrender.com/data?well=34059242540000

<br>

---
---

### **Miscellaneous**

A more detailed and complex implementation of the same can be found here:
    https://github.com/Jerryj1127/inerG-demo.git

I have accidently loaded the full excel sheet data into sperate normalized tables and did rest of the operations on that. Instead of loading the pre-calulated anual sum, it gets the sum from the table data using SQL's SUM() operation. It even emloyes a built in downloader and a proper WSGI server.

>How complex is it with respect to this current repo ? <br>
Well, to simply put it this repo took <15 mins to build whereas the other one took 4+ hours.

>So...Whats the big difference? <br>
Since the flask app in this current repo access the precaluculated data from a single table, an average local get call takes 5 ms. In case of the other repo, it accesses data from multiple tables, calculates sum on the go and therefore a local get call takes 7 ms on average. The end data provided by both the repos are exaclty the same.