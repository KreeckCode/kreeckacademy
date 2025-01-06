from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UploadVideo
import os
import time
from .utils import unique_slug_generator


@receiver(post_save, sender=UploadVideo)
def video_post_save_receiver(sender, instance, **kwargs):
    # Set slug if not present
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)
        instance.save(update_fields=["slug"])  # Save the slug if it was updated

    video_path = instance.video.path
    print(f"Video path: {video_path}")  # Debug line

    # Retry logic
    retries = 5
    while retries > 0:
        if os.path.exists(video_path):
            try:
                pass
                """
                clip = mp.VideoFileClip(video_path)
                # Update the duration if it's not set
                if instance.duration is None:
                    duration = int(clip.duration)  # Duration in seconds
                    instance.duration = duration
                    instance.save(update_fields=['duration'])  # Save the duration if it's updated
                """
            except Exception as e:
                print(f"Error processing video file: {e}")  # Catch any exception
            break
        else:
            print(f"Video file not found. Retries left: {retries}")
            time.sleep(2)  # Wait before retrying
            retries -= 1


# Connect the post_save signal
post_save.connect(video_post_save_receiver, sender=UploadVideo)
