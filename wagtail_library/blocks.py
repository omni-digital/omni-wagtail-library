from wagtail.wagtailcore.blocks import PageChooserBlock


class LibraryItemBlock(PageChooserBlock):
    """Library Item chooser block for streamfield."""
    def __init__(
        self,
        target_model='wagtail_library.LibraryItemDetailPage',
        **kwargs
    ):
        """
        Initialization code

        :param target_model: default selection model - can be overriden in model
        :param kwargs: default block kwargs
        """
        super(LibraryItemBlock, self).__init__(target_model, **kwargs)

    class Meta(object):
        """Block meta."""
        template = 'wagtail_library/library_item_block.html'
