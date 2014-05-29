# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HeadphonesIndexPage'
        db.create_table(u'app_backend_headphonesindexpage', (
            (u'page_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['wagtailcore.Page'], unique=True, primary_key=True)),
            ('intro', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'app_backend', ['HeadphonesIndexPage'])

        # Adding model 'Equipments'
        db.create_table(u'app_backend_equipments', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True)),
            ('blog', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='equipment', null=True, on_delete=models.SET_NULL, to=orm['app_backend.BlogPage'])),
        ))
        db.send_create_signal(u'app_backend', ['Equipments'])

        # Deleting field 'HeadphonesCarouselItem.caption'
        db.delete_column(u'app_backend_headphonescarouselitem', 'caption')

        # Deleting field 'HeadphonesCarouselItem.embed_url'
        db.delete_column(u'app_backend_headphonescarouselitem', 'embed_url')

        # Deleting field 'Headphones.blog'
        db.delete_column(u'app_backend_headphones', 'blog_id')

        # Deleting field 'Headphones.description'
        db.delete_column(u'app_backend_headphones', 'description')

        # Deleting field 'Headphones.name'
        db.delete_column(u'app_backend_headphones', 'name')

        # Adding field 'Headphones.equipments_ptr'
        db.add_column(u'app_backend_headphones', u'equipments_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['app_backend.Equipments'], unique=True),
                      keep_default=False)


        # Changing field 'BlogIndexPage.intro'
        db.alter_column(u'app_backend_blogindexpage', 'intro', self.gf('django.db.models.fields.CharField')(max_length=255))

    def backwards(self, orm):
        # Deleting model 'HeadphonesIndexPage'
        db.delete_table(u'app_backend_headphonesindexpage')

        # Deleting model 'Equipments'
        db.delete_table(u'app_backend_equipments')

        # Adding field 'HeadphonesCarouselItem.caption'
        db.add_column(u'app_backend_headphonescarouselitem', 'caption',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Adding field 'HeadphonesCarouselItem.embed_url'
        db.add_column(u'app_backend_headphonescarouselitem', 'embed_url',
                      self.gf('django.db.models.fields.URLField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Headphones.blog'
        db.add_column(u'app_backend_headphones', 'blog',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='equipment', null=True, to=orm['app_backend.BlogPage'], on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Headphones.description'
        db.add_column(u'app_backend_headphones', 'description',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=1024),
                      keep_default=False)

        # Adding field 'Headphones.name'
        db.add_column(u'app_backend_headphones', 'name',
                      self.gf('django.db.models.fields.CharField')(default='test', max_length=255, unique=True),
                      keep_default=False)

        # Deleting field 'Headphones.equipments_ptr'
        db.delete_column(u'app_backend_headphones', u'equipments_ptr_id')


        # Changing field 'BlogIndexPage.intro'
        db.alter_column(u'app_backend_blogindexpage', 'intro', self.gf('wagtail.wagtailcore.fields.RichTextField')())

    models = {
        u'app_backend.blogindexpage': {
            'Meta': {'object_name': 'BlogIndexPage', '_ormbases': [u'wagtailcore.Page']},
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'app_backend.blogindexpagerelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'BlogIndexPageRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['app_backend.BlogIndexPage']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app_backend.blogpage': {
            'Meta': {'object_name': 'BlogPage', '_ormbases': [u'wagtailcore.Page']},
            'body': ('wagtail.wagtailcore.fields.RichTextField', [], {}),
            'date': ('django.db.models.fields.DateField', [], {}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'head_image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'head_image'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'app_backend.blogpagerelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'BlogPageRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['app_backend.BlogPage']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'app_backend.comment': {
            'Meta': {'object_name': 'Comment'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'comment'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['app_backend.BlogPage']"}),
            'body': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 5, 29, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_comment'", 'to': u"orm['auth.User']"})
        },
        u'app_backend.equipments': {
            'Meta': {'object_name': 'Equipments'},
            'blog': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'equipment'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['app_backend.BlogPage']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'app_backend.headphones': {
            'Meta': {'object_name': 'Headphones', '_ormbases': [u'wagtailcore.Page', u'app_backend.Equipments']},
            u'equipments_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['app_backend.Equipments']", 'unique': 'True'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'}),
            'size': ('django.db.models.fields.CharField', [], {'max_length': '127'}),
            'transducer': ('django.db.models.fields.CharField', [], {'default': "'MC'", 'max_length': '2'}),
            'wear_type': ('django.db.models.fields.CharField', [], {'default': "'CI'", 'max_length': '2'}),
            'weight': ('django.db.models.fields.FloatField', [], {}),
            'wire_length': ('django.db.models.fields.FloatField', [], {})
        },
        u'app_backend.headphonescarouselitem': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'HeadphonesCarouselItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['wagtailimages.Image']"}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'carousel_items'", 'to': u"orm['app_backend.Headphones']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'app_backend.headphonesindexpage': {
            'Meta': {'object_name': 'HeadphonesIndexPage', '_ormbases': [u'wagtailcore.Page']},
            'intro': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'page_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['wagtailcore.Page']", 'unique': 'True', 'primary_key': 'True'})
        },
        u'app_backend.headphonesrelatedlink': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'HeadphonesRelatedLink'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_document': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtaildocs.Document']"}),
            'link_external': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'link_page': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['wagtailcore.Page']"}),
            'page': ('modelcluster.fields.ParentalKey', [], {'related_name': "'related_links'", 'to': u"orm['app_backend.Headphones']"}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'wagtailcore.page': {
            'Meta': {'object_name': 'Page'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pages'", 'to': u"orm['contenttypes.ContentType']"}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'has_unpublished_changes': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'numchild': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'owned_pages'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'search_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'seo_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'show_in_menus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'url_path': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'wagtaildocs.document': {
            'Meta': {'object_name': 'Document'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'})
        },
        u'wagtailimages.image': {
            'Meta': {'object_name': 'Image'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'file': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'height': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'uploaded_by_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['app_backend']