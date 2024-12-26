# CabMiloge  

**Visit the live website: [CabMiloge](https://osdg.iiit.ac.in/cabsharing/)**  

## About CabMiloge  

[**CabMiloge**](https://github.com/OSDG-IIITH/CabMiloge) is a user-friendly platform developed during the hackathon **HackIIIT 2024**, where it won **1st prize in the design category**.  
The team members behind this project are:  
- [Himanshu Yadav](https://www.github.com/himanshuyv)  
- [Shaunak Biswas](https://www.github.com/StarryBadger)  
- [Jayesh Sutar](https://www.github.com/Jayeshs27)  
- [Rohan Shridhar](https://www.github.com/gitPROhan)  

Following the hackathon, the project has been improved and is now maintained by the [**Open Source Developers Group (OSDG) at IIIT Hyderabad**](https://osdg.iiit.ac.in/). The current list of code contributors includes the following people in addition to the original authors:
- [Abhiram Tilak](https://github.com/abhiramtilakiiit)
- [Adithya Kishor](https://github.com/The-Coder-Kishor)
- [Ankith Pai](https://github.com/ankith26)
- [Anushka Sharma](https://github.com/anushkasharma2005)
- [Manit Roy](https://github.com/manit2004)
- [Praneeth Jain](https://github.com/PraneethJain)
- [Vyakhya Gupta](https://github.com/vcnk4v)

The primary goal of [**CabMiloge**](https://osdg.iiit.ac.in/cabsharing/) is to simplify the process of connecting students with peers traveling in the same direction. By doing so, the platform:  
- Streamlines the coordination of rides and travel plans.  
- Reduces travel costs.  
- Offers a convenient and hassle-free way for students to arrange their journeys.  

## For Developers  

CabMiloge runs as a Docker container for easy setup and deployment.  

### Clone the Repository  

Clone the repository to your local system:  
```bash
git clone https://github.com/OSDG-IIITH/CabMiloge.git
cd CabMiloge
```

### Set Environment Variables  

Create a `.env` file in the project directory and add the required environment variables:  
```bash
touch .env
```

### Run the Docker Container  

Use the provided script to build and run the Docker container:  
```bash
./run.sh
```

### To access the website go to:

```bash
http://172.22.0.2
```

### To Gracefully Terminate  

Stop the Docker container with the following script:  
```bash
./stop.sh
```


## Resources  

- **Docker Documentation**: Refer to [Docker Docs](https://docs.docker.com/) for more help.  
- **Contributing**: Contributions are welcome! Please submit a PR or create an issue to improve the platform.  
