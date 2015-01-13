from Products.statusmessages.interfaces import IStatusMessage
from appeus.content import MessageFactory as _
from five import grok
from plone.app.dexterity import PloneMessageFactory as _PMF
from plone.app.textfield import RichText
from plone.directives import dexterity
from plone.directives import form
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.namedfile.field import NamedFile
from plone.namedfile.field import NamedImage
from plone.namedfile.interfaces import IImageScaleTraversable
from z3c.form import field
from z3c.form import group
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


# Interface class; used to define content-type schema.
class IApp(form.Schema, IImageScaleTraversable):
    """
    App content-type
    """

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
