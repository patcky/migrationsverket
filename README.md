# migrationsverket
Some chaotic scripts that scrape data from migrationsverket to see if there are any available times for the selected cities. This is intended to help people who need to book an appointment but can never find a free timeslot.

## How to use
1. Clone the repository
### Option 1 - Run on your local machine
2. Make sure you have Python (currently using 3.12.1)
3. Install the required packages
```bash
pip install -r requirements.txt
```
4. Install the required browser and webdriver for selenium
```bash
wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

wget https://storage.googleapis.com/chrome-for-testing-public/123.0.6312.122/linux64/chromedriver-linux64.zip
apt install unzip
unzip chromedriver-linux64.zip
mv mv chromedriver-linux64/chromedriver /usr/bin/chromedriver
```
5. Run the script
```bash
python3 check_all_cities.py
```
or
```bash
python3 check_specific_cities.py
```
### Option 2 - Run on a Docker container
(You need to have Docker installed. It's easier with Docker Desktop)
2. Build the Docker image
```bash
docker build -t migrationsverket .
```
3. Run the Docker container
```bash
docker run migrationsverket
```
