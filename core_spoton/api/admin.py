from django.contrib import admin

from core_spoton.api.models import Spot, StatusReport, Review, ClassFreeRooms, LectureHall


# Register your models here.

class ClassFreeRoomsAdmin(admin.TabularInline):
    model = ClassFreeRooms
    extra = 1


class LectureHallAdmin(admin.ModelAdmin):
    model = LectureHall
    inlines = [ClassFreeRoomsAdmin]
    list_display = ['name', 'is_approved']


class SpotAdmin(admin.ModelAdmin):
    model = Spot
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Spot, SpotAdmin)
admin.site.register(StatusReport)
admin.site.register(Review)
admin.site.register(LectureHall, LectureHallAdmin)
admin.site.register(ClassFreeRooms)
