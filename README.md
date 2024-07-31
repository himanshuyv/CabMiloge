# CabMiloge

**Visit the live website: [CabMiloge](https://osdg.iiit.ac.in/cabsharing)**

## HackIIIT 2024 Winner!

CabMiloge was crowned the winner of HackIIIT 2024 in the Design Category! The team members behind the idea were [@StarryBadger](https://www.github.com/StarryBadger),  [@himanshuyv](https://www.github.com/himanshuyv),  [@Jayeshs27](https://www.github.com/Jayeshs27) and  [@gitPROhan](https://www.github.com/gitPROhan). Following the hackathon, OSDG took the project under its wings. Since then, many contributions have been made to further develop and improve CabMiloge.

## About CabMiloge

CabMiloge is a cab-sharing platform designed exclusively for the IIIT Hyderabad community. Our mission is to simplify travel arrangements, reduce costs, and foster connections among students and faculty.

## For Developers

CabMiloge now runs as a Docker container! For help with Docker refer to [this](https://docs.docker.com/).

### Make venv and enter venv
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### Install requirements.txt
```bash
pip install -r requirements.txt
```

### Add env variables in .env
```bash
touch .env
```

### Run the docker container with the given bash script
```bash
./run.sh
```

### To gracefully terminate, run
```bash
./stop.sh
```



