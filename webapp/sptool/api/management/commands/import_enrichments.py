from urllib.request import urlopen
import codecs

import json
from pathlib import Path

from django.core.management.base import BaseCommand
from ...models import Enrichment
from ...models import Video, VideoEnrichments


class Command(BaseCommand):
    def handle(self, *args, **options):

        self.import_enrichments()

        self.get_position_of_enrichments_on_videos()

    def import_enrichments(self):

        my_file = Path("/srv/sptool/api/management/commands/data_files/enrichments.json")

        if my_file.is_file():
            print("Parsing content from enrichments.json file")

        else:
            print("Creating enrichments.json file")

            uri = 'http://mecanex.noterik.com/tools/unique_enrichments.php'

            response = urlopen(uri)

            reader = codecs.getreader("utf-8")
            data = json.load(reader(response))

            with my_file.open('w+') as outfile:
                json.dump(data, outfile)

        with my_file.open('r') as data_file:
            data = json.load(data_file)

        for key in data:

            enrichment_id = key

            enrichment_class = "Unknown"
            name = data[key]["longName"]

            wikipediaURL = data[key]["wikipediaUrl"] if "wikipediaUrl" in data[key] else ""

            dbpediaURL = data[key]["dbpediaUrl"] if "dbpediaUrl" in data[key] else ""

            overlay_text_description = data[key]["description"] if "description" in data[key] else ""
            thumbnail = data[key]["thumbnail"] if "thumbnail" in data[key] else ""

            enrichment = Enrichment.objects.filter(enrichment_id=enrichment_id)

            if not enrichment.exists():

                enrichment = Enrichment(
                    enrichment_id=enrichment_id,
                    enrichment_class=enrichment_class,
                    name=name,
                    wikipediaURL=wikipediaURL,
                    dbpediaURL=dbpediaURL,
                    overlay_text_description=overlay_text_description,
                    thumbnail=thumbnail
                )

                enrichment.save()

            else:
                enrichment.update(
                    enrichment_id=enrichment_id,
                    enrichment_class=enrichment_class,
                    name=name,
                    wikipediaURL=wikipediaURL,
                    dbpediaURL=dbpediaURL,
                    overlay_text_description=overlay_text_description,
                    thumbnail=thumbnail
                )

        print("Done with importing enrichments")

    def get_position_of_enrichments_on_videos(self):

        my_file = Path("/srv/sptool/api/management/commands/data_files/enrichments_on_videos.json")

        if my_file.is_file():
            print("Parsing content from enrichments_on_videos.json file")

        else:
            print("Creating enrichments_on_videos.json file")

            uri = 'http://mecanex.noterik.com/tools/video_enrichments.php'

            response = urlopen(uri)

            reader = codecs.getreader("utf-8")
            data = json.load(reader(response))

            with my_file.open('w+') as outfile:
                json.dump(data, outfile)

        with my_file.open('r') as data_file:
            data = json.load(data_file)

        for item in data:

            euscreen = item["id"]
            video = Video.objects.filter(euscreen=euscreen)
            if not video.exists():
                continue

            else:
                video = video[0]

            for enrichment in item["enrichment"]:

                enrichment_id = Enrichment.objects.get(enrichment_id=enrichment)

                # Will not update existing entries of video-enrichment pairs
                if not VideoEnrichments.objects.filter(video_id=video.id).filter(enrichment_id=enrichment_id).exists():

                    enrichment_id = enrichment_id.id
                    video_id = video.id

                    for localization in item["enrichment"][enrichment]["localization"]:
                        for time_position in item["enrichment"][enrichment]["localization"][localization]:
                            y_min = item["enrichment"][enrichment]["localization"][localization][time_position]["y_min"]
                            x_min = item["enrichment"][enrichment]["localization"][localization][time_position]["x_min"]
                            width = item["enrichment"][enrichment]["localization"][localization][time_position]["width"]
                            height = item["enrichment"][enrichment]["localization"][localization][time_position][
                                "height"]

                            time = int(time_position[1:])

                            video_enrichment = VideoEnrichments(
                                enrichment_id=enrichment_id,
                                video_id=video_id,
                                time=time,
                                y_min=y_min,
                                x_min=x_min,
                                width=width,
                                height=height
                            )

                            video_enrichment.save()

        print("Done importing position of enrichments on videos")
