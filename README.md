# seismic-detection

## Mission
Planetary seismology missions struggle with the power requirements necessary to send continuous seismic data back to Earth. But only a fraction of this data is scientifically useful. Therefore we created a solution which would allow the lander to distinguish signals from noise, and send back only the data which matters.

## Discarded solutions, why?
- Single Window Maeda-AIC (SWM-AIC) algorithm, did not fit our 1C data well since it is more sueful for 3C
- LTA/STA triggering, was found to be unrealiable at cutting through the noise in the raw data
- Machine Learning Model, considered unreliable by NASA and ourselves - which is why we went with a deterministic solution

## How to run the project 

### Prerequisites
- [Python 3.9 or higher](https://www.python.org/)
- [Jupyter Notebook](https://jupyter.org/)
- [Seismic data packages from NASA](https://wufs.wustl.edu/SpaceApps/data/space_apps_2024_seismic_detection.zip)

1. Clone the repo by running the following command in your terminal
```bash
git clone https://github.com/Adrian2901/seismic-detection.git
```
2. Cd into the project directory
```bash
cd seismic-detection
```
4. Unzip the seismic data packages into the project directory
4. Install the dependencies
```bash
# Optional: Create a virtual environment
pip install -r requirements.txt
```

### Project Structure
The project directory should look like this
// TODO: Fix this
```bash
C:.
├───discard
├───space_apps_2024_seismic_detection
│   ├───data
│   │   ├───lunar
│   │   └───mars
│   │       ├───test
│   │       └───training
│   │           ├───catalogs
│   │           ├───data
│   │           └───plot
│   ├───example_file_1.txt
│   ├───example_config.json
│   └───README.md
```

### Contributors
- [Adrian Hassa](//TODO: add email)
- [Marko Mojsov](//TODO: add email)
- [Ionel Pop](//TODO: add email)








