import os
import planet
import json
import datetime
import requests
from requests.auth import HTTPBasicAuth

class apiConnect:
    def apiDownload(self):
        apikey = '7f2d08550c1c4d03a0f133827f1e0190'

        c = 0

        vreme = datetime.datetime.now()
        item_type = "PSScene4Band"

        x1 = 20.456714630126953
        y1 = 44.798464385462914

        x2 = 20.470619201660156
        y2 = 44.798464385462914

        x3 = 20.470619201660156
        y3 = 44.806685916025835

        x4 = 20.456714630126953
        y4 = 44.806685916025835

        x5 = 20.456714630126953
        y5 = 44.798464385462914

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
                "gte": "{}-{}-{}T00:00:00.000Z".format(vreme.year,vreme.month,vreme.day-5),
                "lte": "{}-{}-{}T00:00:00.000Z".format(vreme.year,vreme.month,vreme.day-2)
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

        image_ids = [feature['id'] for feature in search_result.json()['features']]


        id0 = image_ids[0]
        id0_url = 'https://api.planet.com/data/v1/item-types/{}/items/{}/assets'.format(item_type, id0)

        result = \
            requests.get(
                id0_url,
                auth=HTTPBasicAuth("7f2d08550c1c4d03a0f133827f1e0190", '')
            )

        links = result.json()[u"analytic"]["_links"]
        self_link = links["_self"]
        activation_link = links["activate"]

        activate_result = \
            requests.get(
                activation_link,
                auth=HTTPBasicAuth(apikey, '')
            )

        activation_status_result = \
            requests.get(
              self_link,
              auth=HTTPBasicAuth(apikey, '')
          )
        if (activation_status_result.json()["status"] != 'active'):
            while activation_status_result.json()["status"] != 'active':
                activation_status_result = \
                    requests.get(
                        self_link,
                        auth=HTTPBasicAuth("7f2d08550c1c4d03a0f133827f1e0190", '')
                    )
                print(activation_status_result.json()["status"])

        download_link = activation_status_result.json()["location"]
        print("activated")
        picture = requests.get(download_link, allow_redirects = True)
        open('{}-{}-{}.tif'.format(vreme.year,vreme.month,vreme.day-1), 'wb').write(picture.content)