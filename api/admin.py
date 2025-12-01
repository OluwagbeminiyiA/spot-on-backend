from django.contrib import admin

from api.models import Spot, StatusReport, Review, ClassFreeRooms, LectureHall


# Register your models here.

class ClassFreeRoomsAdmin(admin.TabularInline):
    model = ClassFreeRooms
    extra = 1


class LectureHallAdmin(admin.ModelAdmin):
    model = LectureHall
    inlines = [ClassFreeRoomsAdmin]
    list_display = ['name', 'is_approved']


admin.site.register(Spot)
admin.site.register(StatusReport)
admin.site.register(Review)
admin.site.register(LectureHall, LectureHallAdmin)
admin.site.register(ClassFreeRooms)
