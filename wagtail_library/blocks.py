from wagtail.core.blocks import PageChooserBlock


class LibraryDetailBlock(PageChooserBlock):
    """Library detail chooser block for streamfield."""

    def __init__(self, target_model="wagtail_library.LibraryDetail", **kwargs):
        """
        Initialization code

        :param target_model: default selection model - can be overriden in model
        :param kwargs: default block kwargs
        """
        super(LibraryDetailBlock, self).__init__(target_model, **kwargs)

    class Meta(object):
        """Block meta."""

        template = "wagtail_library/library_detail_block.html"
