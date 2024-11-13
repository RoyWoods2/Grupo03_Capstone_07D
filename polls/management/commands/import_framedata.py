import requests
from django.core.management.base import BaseCommand
from polls.models import FrameData, Personaje

class Command(BaseCommand):
    help = 'Importa datos de frame data desde una API'

    def handle(self, *args, **kwargs):
        api_url = "https://github.com/ysmaelrequena/Fighting-game-API/"
        response = requests.get(api_url)
        
        if response.status_code == 200:
            frame_data = response.json()

            for data in frame_data:
                personaje_nombre = data.get("personaje")
                personaje, created = Personaje.objects.get_or_create(nombre=personaje_nombre)

                FrameData.objects.create(
                    personaje=personaje,
                    movimiento=data["movimiento"],
                    tipo=data["tipo"],
                    damage=data["damage"],
                    startup_frames=data["startup_frames"],
                    active_frames=data["active_frames"],
                    recovery_frames=data["recovery_frames"],
                    block_advantage=data["block_advantage"],
                    hit_advantage=data["hit_advantage"],
                    knockdown=data["knockdown"],
                    video_demo_url=data.get("video_demo_url")
                )

            self.stdout.write(self.style.SUCCESS("Datos de Frame Data importados con éxito"))
        else:
            self.stdout.write(self.style.ERROR("Error al conectar con la API"))
