# coding=utf-8
from zope.contentprovider.interfaces import IContentProvider
from zope.schema import TextLine, Choice, ASCIILine

class IOGNLogitudinalInfo(IContentProvider):
    pageTemplateFileName = ASCIILine(title=u"Page Template File Name",
        description=u'The name of the ZPT file that is used to '\
            u'render the status message.',
        required=False,
        default="browser/templates/tioucscript.pt")


