import os
import planet
import json
import datetime
import main
import datetime
import time
import requests
from requests.auth import HTTPBasicAuth


class ApiConnect:
    def check_status(orderID):
        activation_status_result = \
            requests.get(
                'https://api.planet.com/compute/ops/orders/v2/{}'.format(orderID),
                auth=HTTPBasicAuth('7f2d08550c1c4d03a0f133827f1e0190', '')
            )
        return activation_status_result


    def api_download(self):
        apikey = '7f2d08550c1c4d03a0f133827f1e0190'

        cords = main.CoordinatesManager.get_current_coordinates(0)
        cordsArray = cords.split()

        today = datetime.date.today()
        vreme = today - datetime.timedelta(days=1)

        item_type = "PSScene3Band"

        x1 = float(cordsArray[0])
        y1 = float(cordsArray[3])

        x2 = float(cordsArray[2])  # x2
        y2 = float(cordsArray[3])  # y2

        x3 = float(cordsArray[2])
        y3 = float(cordsArray[1])

        x4 = float(cordsArray[0])  # x1
        y4 = float(cordsArray[1])  # y1

        x5 = x1
        y5 = y1

        geojson_geometry = {
            "type": "Polygon",
            "coordinates": [
                [
                    [
                        x1,
                        y1
                    ],
                    [
                        x2,
                        y2
                    ],
                    [
                        x3,
                        y3
                    ],
                    [
                        x4,
                        y4
                    ],
                    [
                        x5,
                        y5
                    ]
                ]
            ]
        }

        geometry_filter = {
            "type": "GeometryFilter",
            "field_name": "geometry",
            "config": geojson_geometry
        }
        date_range_filter = {
            "type": "DateRangeFilter",
            "field_name": "acquired",
            "config": {
                "gte": "{}-{}-{}T00:00:00.000Z".format(vreme.year, vreme.month, vreme.day-3),
                "lte": "{}-{}-{}T23:59:59.000Z".format(vreme.year, vreme.month, vreme.day-2)
            }
        }
        cloud_cover_filter = {
            "type": "RangeFilter",
            "field_name": "cloud_cover",
            "config": {
                "lte": 0.5
            }
        }
        combined_filter = {
            "type": "AndFilter",
            "config": [geometry_filter, date_range_filter, cloud_cover_filter]
        }
        search_request = {
            "item_types": [item_type],
            "filter": combined_filter
        }
        search_result = \
            requests.post(
                'https://api.planet.com/data/v1/quick-search',
                auth=HTTPBasicAuth("7f2d08550c1c4d03a0f133827f1e0190", ''),
                json=search_request)

        try:
            image_ids = [feature['id'] for feature in search_result.json()['features']]
            print(image_ids)
        except:
            print("There are no pictures")
            print(search_result.json())
            return

        h = 1
        c = 0


        for x in image_ids:
            image_id = x

            orders_json = {
                "name": "{}-{}-{}-{}".format(vreme.year, vreme.month, vreme.day,h),
                "subscription_id": 0,
                "products": [{
                    "item_ids":[ "{}".format(image_id)],
                    "item_type": "{}".format(item_type),
                    "product_bundle": "visual"
                }],
                "delivery":{
                    "single-archive": "true"
                },
                "tools":[{
                    "clip":{
                        "aoi": geojson_geometry
                    }
                }
                ]
                }



            create_order = \
                requests.post(
                    'https://api.planet.com/compute/ops/orders/v2',
                    auth=HTTPBasicAuth("7f2d08550c1c4d03a0f133827f1e0190", ''),
                    json=orders_json
                )
            print(create_order.json())
            order_id = create_order.json()['id']

            check_status = ApiConnect.check_status(order_id).json()['state']
            print(check_status)
            t_end = time.time() + 15*60
            while check_status != 'success' or check_status !='failed' or time.time() < t_end:
                start = time.time()
                if(check_status == "success") or(check_status == "failed"):
                    break
                while time.time() < start + 5:
                    a = 3
                check_status = ApiConnect.check_status(order_id).json()['state']
                print(check_status)
            if check_status == 'failed':
                print("Order failed")
                return

            brojac = 0
            p = ApiConnect.check_status(order_id).json()
            for x in p['_links']["results"]:
                split_parts = x['name'].split("_")
                if "udm" in split_parts:
                    brojac = brojac + 1
                    continue
                if "clip.tif" in split_parts:
                    break
                brojac = brojac + 1

            download_link = p['_links']["results"][brojac]["location"]
            print(download_link)
            print(p['_links']["results"][brojac]["name"])
            print("activated")
            print("Downloading...")
            picture = requests.get(download_link, allow_redirects=True)
            open('{}-{}-{}-{}.tif'.format(vreme.year, vreme.month, vreme.day, h), 'wb').write(picture.content)
            print("Download Successful")
            h = h + 1
            c = c + 1

    def api_weather(self):
        cords = main.CoordinatesManager.get_current_coordinates(0)
        cordsArray = cords.split()
        apikey = 'cb67ecffe5d436dee22c58f613ea7332'
        c = 0
        x1 = float(cordsArray[0])
        y1 = float(cordsArray[1])
        x2 = float(cordsArray[2])
        y2 = float(cordsArray[3])
        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        apiLink = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude=current,minutely,hourly,' \
                  'alerts&appid={}'.format(y, x, apikey)

        weatherStatus = \
            requests.get(
                apiLink
            )
        # print(weatherStatus.json())
        #  h = 0
        #  for x in weatherStatus.json()['daily']:
        #      if(x['weather'][0]['main'] == 'Clouds'):
        #         c = c+1
        #     h = h + 1
        # print(h)
        # print(c)


ApiConnect.api_download(0)
