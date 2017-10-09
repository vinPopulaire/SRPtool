from urllib.request import urlopen

import xmltodict
import json
from pathlib import Path

from django.core.management.base import BaseCommand
from api.models import Video

class Command(BaseCommand):

    def handle(self, *args, **options):
        my_file = Path("srv/sptool/api/management/commands/data_files/videos.json")

        if my_file.is_file():
            print("Parsing content from videos.json file")

        else:
            print("Creating videos.json file")

            uri = 'http://a1.noterik.com:8081/smithers2/domain/espace/user/luce/video'

            file = urlopen(uri)
            data = file.read()
            file.close()

            json_data = xmltodict.parse(data)

            with my_file.open('w+') as outfile:
                json.dump(json_data, outfile)


        with my_file.open('r') as data_file:
            data = json.load(data_file)


        for i in data['fsxml']['video']:
            euscreen = i.get('@id')


            genre = i['properties'].get('genre')
            topic = i['properties'].get('topic')
            title = i['properties'].get('TitleSet_TitleSetInEnglish_title')
            geographical_coverage = i['properties'].get('SpatioTemporalInformation_SpatialInformation_GeographicalCoverage')
            summary = i['properties'].get('summaryInEnglish')
            thesaurus_terms = i['properties'].get('ThesaurusTerm')

            geographical_coverage = geographical_coverage if geographical_coverage != None else 'Unknown'
            thesaurus_terms = thesaurus_terms if thesaurus_terms != None else "Unknown"

            item_duration = i['properties'].get('TechnicalInformation_itemDuration').split(":")

            # Metadata should have duration
            # duration = int(item_duration[0])*60*60 + int(item_duration[1])*60 + int(item_duration[2])
            # print(duration)

            video = Video.objects.filter(euscreen=euscreen)
            if not video.exists():
                video = Video(
                        euscreen=euscreen,
                        genre=genre,
                        topic=topic,
                        title=title,
                        geographical_coverage=geographical_coverage,
                        thesaurus_terms=thesaurus_terms,
                        summary=summary
                        # duration=duration
                    )
                video.save()

            else:
                video.update(
                        genre=genre,
                        topic=topic,
                        title=title,
                        geographical_coverage=geographical_coverage,
                        thesaurus_terms=thesaurus_terms,
                        summary=summary
                        # duration=duration
                    )

        print("Done with importing videos")
