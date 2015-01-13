from appeus.content import MessageFactory as _
from bs4 import BeautifulSoup
from five import grok
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.directives import dexterity
from plone.directives import form
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.file import NamedBlobImage as NamedBlobImage_file
from plone.namedfile.interfaces import IImageScaleTraversable
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema

import urllib2
import requests

# Interface class; used to define content-type schema.
class IApp(form.Schema, IImageScaleTraversable):
    """
    App content-type
    """

    author = schema.TextLine(
        title=_(u"Author"),
        required=False,
    )

    form.widget(who=CheckBoxFieldWidget)
    who = schema.List(
        title=_(u"Who"),
        value_type=schema.Choice(
            vocabulary='appeus.content.who',
            required=True,
        ),
        required=True,
    )

    android_availability = schema.Bool(
        title=_(u"Android availability"),
        required=False,
    )

    android_googleplay_url = schema.TextLine(
        title=_(u"URL for Google Play"),
        required=False,
    )

    android_version_number = schema.TextLine(
        title=_(u"App version number for Android"),
        required=False,
    )

    android_min_version = schema.TextLine(
        title=_(u"Min version for Android"),
        required=False,
    )

    ios_availability = schema.Bool(
        title=_(u"IOS availability"),
        required=False,
    )

    ios_itunes_url = schema.TextLine(
        title=_(u"URL for Apple Store"),
        required=False,
    )

    ios_version_number = schema.TextLine(
        title=_(u"App version number for IOS"),
        required=False,
    )

    ios_min_version = schema.TextLine(
        title=_(u"Min version for IOS"),
        required=False,
    )

    language = schema.Choice(
        title=_(u"Language"),
        vocabulary='appeus.content.language',
        required=True,
    )

    price = schema.Choice(
        title=_(u"Price"),
        vocabulary='appeus.content.price',
        required=True,
    )

    image = NamedBlobImage(
        title=_(u"Please upload an image"),
        required=False,
    )

    subjects = schema.Tuple(
        title=_PMF(u'label_tags', default=u'Tags'),
        description=_PMF(
            u'help_tags',
            default=u'Tags are commonly used for ad-hoc organization of ' +
                    u'content.'
        ),
        value_type=schema.TextLine(),
        required=False,
        missing_value=(),
    )


class App(dexterity.Container):
    grok.implements(IApp)
    # Add your class methods and properties here

    def Subject(self):
        return self.subjects

grok.templatedir('templates')


# class AddForm(dexterity.AddForm):
#     grok.name('appeus.content.app')
#     grok.context(IApp)
#     grok.require('appeus.content.AddApp')


# class EditForm(dexterity.EditForm):
#     grok.context(IApp)
#     grok.name('edit')
#     grok.require('cmf.ModifyPortalContent')


class AppView(grok.View):
    grok.context(IApp)
    grok.require('zope2.View')
    grok.name('view')


class GooglePlayImport(grok.View):
    grok.context(IApp)
    grok.require('cmf.ModifyPortalContent')
    grok.name('googleplayimport')

    def render(self):
        sock = requests.get(self.context.android_googleplay_url)
        soup = BeautifulSoup(sock.text)
        title = soup.find('div', {'class': 'document-title'}).text.strip()
        desc = soup.find('div', {'class': 'id-app-orig-desc'}).text.strip()
        author = soup.find('div', itemprop='author').find('a').text.strip()
        version = soup.find('div', itemprop='softwareVersion').text.strip()
        osversion = soup.find('div', itemprop='operatingSystems').text.strip()
        images = soup.find_all('img', {'class': 'screenshot'})

        self.context.title = title
        self.context.description = desc
        self.context.author = author
        self.context.android_version_number = version
        self.context.android_min_version = osversion
        for image in images:
            imageurl = image.get('src')
            filename = unicode(imageurl.split('/')[-1], 'utf-8')
            sock = urllib2.urlopen(imageurl)
            imgdata = sock.read()
            try:
                imgobject = imgdata
                self.context.image = NamedBlobImage_file(imgobject,
                    contentType=sock.headers['content-type'],
                    filename=filename)
                break
            except:
                pass
            sock.close()

        messages = IStatusMessage(self.request)
        messages.add(_(u"Information imported from Google Play"), type=u"info")
        return self.request.response.redirect(self.context.absolute_url())


class ItunesImport(grok.View):
    grok.context(IApp)
    grok.require('cmf.ModifyPortalContent')
    grok.name('itunesimport')

    def render(self):

        messages = IStatusMessage(self.request)
        messages.add(_(u"Information imported from Itunes"), type=u"info")
        return self.request.response.redirect(self.context.absolute_url())
