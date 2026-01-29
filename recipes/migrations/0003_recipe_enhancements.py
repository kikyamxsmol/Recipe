# Generated migration for recipe model enhancements

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_userprofile_followers'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='dietary_restriction',
            field=models.CharField(
                choices=[('vegan', 'Vegan'), ('vegetarian', 'Vegetarian'), ('gluten-free', 'Gluten-Free'), ('dairy-free', 'Dairy-Free'), ('keto', 'Keto'), ('paleo', 'Paleo'), ('none', 'None')],
                default='none',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.CharField(blank=True, help_text='Comma-separated tags', max_length=500),
        ),
        migrations.AddField(
            model_name='recipe',
            name='view_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-created_at']},
        ),
    ]
