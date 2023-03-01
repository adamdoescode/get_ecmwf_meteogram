#%%
import requests
import datetime
import argparse

PERTH_LOC = {
    'latitude': '-31.95',
    'longitude': '115.85'
}
BROCKMAN_LOC = {
    'latitude': '-22.34',
    'longitude': '117.16'
}
LOCATIONS = {
    'Perth': PERTH_LOC,
    'Brockman': BROCKMAN_LOC
}
#%%

# read in CLI arguments
def parse_args():
    parser = argparse.ArgumentParser()
    #add argument to take in locations instead of lat lon
    parser.add_argument('--location', type=str, help='location', default=None)
    parser.add_argument('--lat', type=float, help='latitude', default='-31.95')
    parser.add_argument('--lon', type=float, help='longitude', default='115.85')
    parser.add_argument('--outputFormat', type=str, help='valid options are pdf or png', default='pdf')
    return parser.parse_args()
#%%
class meteogram():
    def __init__(
            self, location = None, lat = None, lon = None, outputFormat = 'pdf'
    ) -> None:
        self.api_url = "https://charts.ecmwf.int/opencharts-api/v1/"
        self.product = 'opencharts_meteogram'
        self.epsgram='classical_15d'
        self.location = location
        self.lat = lat
        self.lon = lon
        self.get_location() #changes lat and lon if location provided
        self.outputFormat = outputFormat
    
    def get_location(self):
        ''' 
        get lat lon from LOC object if location parameter passed to meteogram object
        '''
        if self.location is not None:
            self.lat = LOCATIONS[self.location]['latitude']
            self.lon = LOCATIONS[self.location]['longitude']
        else:
            pass
    
    def meteogram_request(self, printOutput = False):
        self.today = datetime.date.today()
        #subtract some hours off current AWST time so that we 
        # are not too far in the future
        # apparently about 24 hrs required for a forecast... 
        delayedDate = self.today - datetime.timedelta(hours=24)
        base_time = delayedDate.strftime('%Y-%m-%dT%H:%M:%SZ')
        get = (
            f'{self.api_url}products/{self.product}/?epsgram={self.epsgram}'
            f'&base_time={base_time}&lat={self.lat}&lon={self.lon}&format={self.outputFormat}'
        )
        self.result = requests.get(get)
        self.data = self.result.json()
    
    def meteogram_image(self):
        '''
        writes meteogram image to file
        '''
        image_api = self.data["data"]["link"]["href"]
        self.image = requests.get(image_api)
        self.fileName = (
            f"output/{self.today}_{self.location}_{self.lat}."
            f"{self.lon}_{self.product}.{self.outputFormat}"
        ).replace('-', '_')
        with open(self.fileName, "wb") as img:
            img.write(self.image.content)
    
    def run(self):
        '''
        Coordination function that runs functions to get an image
        '''
        self.meteogram_request()
        self.meteogram_image()

# main run code
if __name__ == "__main__":
    inputArgs = parse_args()
    meteogram = meteogram(inputArgs.location, inputArgs.lat, inputArgs.lon, inputArgs.outputFormat)
    meteogram.run()


# %%
